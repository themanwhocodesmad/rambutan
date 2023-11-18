from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

import math

from game_engine.models import Fleet, Planet
from game_engine.serializers import FleetSerializer
from game_engine.utilities_functions import process_attack


class FleetAttackView(generics.UpdateAPIView):

    """
    To launch an attack using the FleetAttackView, you need to send a PUT request to the /fleets/{fleet_id}/attack/
    endpoint with the fleet ID in the URL and the defender planet ID in the request data.

        data = {
            'defender_planet_id': '{defender_planet_id}',
        }

    """
    permission_classes = [IsAuthenticated]
    queryset = Fleet.objects.all()
    serializer_class = FleetSerializer
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        attacker_fleet = self.get_object()
        defender_planet_id = request.data.get('defender_planet_id')

        if not defender_planet_id:
            return Response({'error': 'Defender planet ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        attacker_planet = attacker_fleet.planet
        defender_planet = get_object_or_404(Planet, id=defender_planet_id)

        # TODO:Calculate the distance between planets

        distance = math.sqrt((defender_planet.x - attacker_planet.x) ** 2 + (defender_planet.y - attacker_planet.y) ** 2)
        travel_time = distance / attacker_fleet.speed

        # Schedule the Celery task to process the attack
        process_attack.apply_async((attacker_fleet.id, defender_planet.id), countdown=travel_time)

        serializer = self.get_serializer(attacker_fleet)
        return Response(serializer.data)

