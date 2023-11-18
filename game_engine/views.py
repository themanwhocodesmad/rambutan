from itertools import chain

from django.http import JsonResponse
from rest_framework import generics
from rest_framework import status
from rest_framework import viewsets
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .constants.game_constrants import TROOPS_DATA, TROOP_CHOICES, TROOP_COSTS
from .serializers import *
from .serializers import UserProfileSerializer
from .utilities_functions.change_player_class import change_player_class


# Get all the current player's planet ids:
class PlayerPlanetIdsView(generics.ListAPIView):
    """
    Returns a list of all planet IDs for the authenticated user.
    """
    serializer_class = PlanetIdSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Planet.objects.filter(owner=user)


class UserProfileView(generics.RetrieveAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user.profile


class UserProfileSearchView(generics.ListAPIView):
    serializer_class = UserProfileSearchSerializer

    def get_queryset(self):
        username = self.kwargs.get("username")
        return UserProfile.objects.filter(user__username__icontains=username)


class ChangePlayerClassView(APIView):
    """
        Change Player Class
        """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        new_class = request.data.get("class", None)
        if not new_class:
            return Response({"error": "No class provided"}, status=status.HTTP_400_BAD_REQUEST)

        user_profile = UserProfile.objects.get(user=request.user)
        success, message = change_player_class(user_profile, new_class)
        if success:
            return Response({"message": message}, status=status.HTTP_200_OK)
        else:
            return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)


class PlayerPlanetsView(APIView):
    """
    Retrieve all planets owned by the authenticated user
    """

    def get(self, request):
        user = request.user
        if user.is_authenticated:
            planets = user.planet_set.all()
            serializer = PlanetSerializer(planets, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class PlanetViewSet(viewsets.ModelViewSet):
    queryset = Planet.objects.all()
    serializer_class = PlanetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SpecificBuildingViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        building_type = self.kwargs.get('building_type', None)
        if building_type is not None:
            building_class = self.get_building_class(building_type)
            if building_class is None:
                raise NotFound("Building type not found")

            self.queryset = building_class.objects.all()
            self.serializer_class = self.get_building_serializer(building_type)

            planet_id = self.kwargs.get('planet_id', None)
            if planet_id is not None:
                try:
                    planet = Planet.objects.get(id=planet_id, owner=self.request.user)
                except Planet.DoesNotExist:
                    raise NotFound("Planet not found")

                return self.queryset.filter(planet=planet)
            else:
                return self.queryset.filter(planet__owner=self.request.user)
        else:
            raise NotFound("Building type not specified")

    def get_building_class(self, building_type):
        building_classes = {
            'mine': Mine,
            'silo': Silo,
            'forge': Forge,
            'map': Map,
        }
        return building_classes.get(building_type.lower(), None)

    def get_building_serializer(self, building_type):
        serializers = {
            'mine': MineSerializer,
            'silo': SiloSerializer,
            'forge': ForgeSerializer,
            'map': MapSerializer,
        }
        return serializers.get(building_type.lower(), None)


class BuildingViewSet(viewsets.ModelViewSet):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        planet_id = self.kwargs['planet_id']
        user = self.request.user

        mine_queryset = Mine.objects.filter(planet_id=planet_id, planet__owner=user)
        silo_queryset = Silo.objects.filter(planet_id=planet_id, planet__owner=user)
        map_queryset = Map.objects.filter(planet_id=planet_id, planet__owner=user)
        forge_queryset = Forge.objects.filter(planet_id=planet_id, planet__owner=user)

        return sorted(
            chain(mine_queryset, silo_queryset, map_queryset, forge_queryset),
            key=lambda building: building.id
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        building_data = {
            "Mine": MineSerializer([building for building in queryset if isinstance(building, Mine)], many=True).data,
            "Silo": SiloSerializer([building for building in queryset if isinstance(building, Silo)], many=True).data,
            "Map": MapSerializer([building for building in queryset if isinstance(building, Map)], many=True).data,
            "Forge": ForgeSerializer([building for building in queryset if isinstance(building, Forge)], many=True).data
        }

        return Response(building_data)


class ForgeWithTroopsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, planet_id, *args, **kwargs):
        try:
            planet = Planet.objects.get(id=planet_id, owner=request.user)
        except Planet.DoesNotExist:
            return Response({"error": "Planet not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            forge = Forge.objects.get(planet=planet)
        except Forge.DoesNotExist:
            return Response({"error": "Forge not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            army = Army.objects.get(planet=planet)
        except Army.DoesNotExist:
            return Response({"error": "Army not found"}, status=status.HTTP_404_NOT_FOUND)

        forge_serializer = ForgeSerializer(forge)
        army_serializer = ArmySerializer(army)

        return Response({
            "forge": forge_serializer.data,
            "troops": army_serializer.data["troops"]
        }, status=status.HTTP_200_OK)


class TroopDetailsView(APIView):
    def get(self, request, *args, **kwargs):
        data = {}
        for troop_name, display_name in TROOP_CHOICES:
            troop_data = TROOPS_DATA[display_name]
            troop_costs = TROOP_COSTS[display_name]
            data[troop_name] = {
                'attributes': troop_data,
                'costs': troop_costs,
            }

        return JsonResponse(data)


from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.response import Response

from .models import Planet, UserProfile, Silo

from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Planet, UserProfile, Silo
from django.shortcuts import get_object_or_404


class CurrentPlanetDetailsView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        planet_id = self.kwargs.get('planet_id')
        planet = get_object_or_404(Planet, id=planet_id, owner=request.user)
        silo = get_object_or_404(Silo, planet=planet)

        user_profile = get_object_or_404(UserProfile, user=request.user)
        orion_credits = user_profile.orion_credits

        data = {
            'planet_name': f'{planet.name} | {planet_id}',
            'silo_resource_amounts': silo.stored_resources,
            'orion_credits': orion_credits
        }

        return Response(data)


class UserPlanetsView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = self.request.user
        planets = Planet.objects.filter(owner=user)
        planet_ids = [planet.id for planet in planets]
        return Response(planet_ids)
