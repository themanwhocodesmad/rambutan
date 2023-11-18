from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from game_engine.constants.game_constrants import TROOP_CHOICES
from game_engine.models import Fleet, Forge
from game_engine.serializers import FleetSerializer


# TODO: Error Handling for trying to make fleets with invalid amounts
class FleetCreateView(generics.CreateAPIView):
    """
    Now, players can create new fleets by sending a POST request to the '/fleets/create/' endpoint with the planet ID and
    a list of troop counts. The list should have the same length as TROOP_CHOICES, and the counts should be in the same
    order as TROOP_CHOICES.
    For example, if TROOP_CHOICES is:

    TROOP_CHOICES = [
    ('Infantry', 'Infantry units'),
    ('AssaultTanks', 'Assault Tanks'),
    ('DroneTroopers', 'Drone Troopers'),
    # ...]

    {
    "planet": "some-planet-id",
    "troops": [10, 5, 20]
    }



    """

    permission_classes = (IsAuthenticated,)
    queryset = Fleet.objects.all()
    serializer_class = FleetSerializer

    def perform_create(self, serializer):
        planet_id = self.request.data.get('planet')
        forge = get_object_or_404(Forge, planet_id=planet_id)
        fleet_number = Fleet.objects.filter(planet_id=planet_id).count() + 1
        fleet_name = f'Fleet #{fleet_number:02d}'

        # Get troop counts from the request data
        troop_counts = self.request.data.get('troops', [])

        # Transfer troops from the Forge to the new fleet
        for (troop_name, _), count in zip(TROOP_CHOICES, troop_counts):
            forge.army.troops[troop_name] -= count
            serializer.validated_data['troops'][troop_name] = count

        forge.army.save()

        serializer.save(name=fleet_name, planet_id=planet_id)


class FleetCreateWithAllTroopsView(generics.CreateAPIView):
    """
    Now, players can create a new fleet with all available troops from the Forge by sending a POST request to the
    '/fleets/create-all/' endpoint with the planet ID.

    For example, if the Forge has 10 Infantry units, 5 Assault Tanks, and 20 Drone Troopers, the request data should
    look like this:
        {
            "planet": "some-planet-id"
        }

    """

    permission_classes = (IsAuthenticated,)
    queryset = Fleet.objects.all()
    serializer_class = FleetSerializer

    def perform_create(self, serializer):
        planet_id = self.request.data.get('planet')
        forge = get_object_or_404(Forge, planet_id=planet_id)
        fleet_number = Fleet.objects.filter(planet_id=planet_id).count() + 1
        fleet_name = f'Fleet #{fleet_number:02d}'

        # Transfer all available troops from the Forge to the new fleet
        for troop_name in forge.army.troops:
            serializer.validated_data['troops'][troop_name] = forge.army.troops[troop_name]
            forge.army.troops[troop_name] = 0

        forge.army.save()

        serializer.save(name=fleet_name, planet_id=planet_id)


class FleetRemoveUnitsView(generics.UpdateAPIView):
    """
    Now, players can remove units from a fleet by sending a PUT request to the '/fleets/{fleet_id}/remove-units/'
    endpoint with the fleet ID and the troops they want to remove. The removed troops will be returned to the Forge.

    For example, if a fleet has 10 Infantry units, 5 Assault Tanks, and 20 Drone Troopers, the request data should
    look like this:

        {
            "troops": {
                "Infantry": 5,
                "AssaultTanks": 2
            }
        }
    This request will remove 5 Infantry units and 2 Assault Tanks from the fleet and return them to the Forge.
    """

    permission_classes = [IsAuthenticated]
    queryset = Fleet.objects.all()
    serializer_class = FleetSerializer
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        fleet = self.get_object()
        planet_id = fleet.planet_id
        forge = get_object_or_404(Forge, planet_id=planet_id)

        troops_to_remove = request.data.get('troops', {})

        # Remove troops from the fleet and return them to the Forge
        for troop_name, count in troops_to_remove.items():
            if count <= 0 or count > fleet.troops.get(troop_name, 0):
                return Response({'error': 'Invalid troop count'}, status=status.HTTP_400_BAD_REQUEST)

            fleet.troops[troop_name] -= count
            forge.army.troops[troop_name] += count

        fleet.save()
        forge.army.save()

        serializer = self.get_serializer(fleet)
        return Response(serializer.data)


class FleetRemoveAllUnitsView(generics.UpdateAPIView):

    """
    Now, players can remove all units from a fleet by sending a PUT request to the '/fleets/{fleet_id}/remove-all-units/'
    endpoint with the fleet ID. All units in the fleet will be returned to the Forge.
    """

    permission_classes = [IsAuthenticated]
    queryset = Fleet.objects.all()
    serializer_class = FleetSerializer
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        fleet = self.get_object()
        planet_id = fleet.planet_id
        forge = get_object_or_404(Forge, planet_id=planet_id)

        # Remove all troops from the fleet and return them to the Forge
        for troop_name in fleet.troops:
            forge.army.troops[troop_name] += fleet.troops[troop_name]
            fleet.troops[troop_name] = 0

        fleet.save()
        forge.army.save()

        serializer = self.get_serializer(fleet)
        return Response(serializer.data)


class FleetDisbandView(generics.DestroyAPIView):

    """
    Players can disband a fleet by sending a DELETE request to the '/fleets/{fleet_id}/disband/' endpoint with the fleet
     ID. All units in the fleet will be returned to the Forge, and the fleet will be deleted.
    """

    permission_classes = [IsAuthenticated]
    queryset = Fleet.objects.all()
    serializer_class = FleetSerializer
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        planet_id = instance.planet_id
        forge = get_object_or_404(Forge, planet_id=planet_id)

        # Return all troops from the fleet to the Forge before deleting the fleet
        for troop_name in instance.troops:
            forge.army.troops[troop_name] += instance.troops[troop_name]

        forge.army.save()
        instance.delete()
