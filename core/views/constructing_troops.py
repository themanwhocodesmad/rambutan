from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from game_engine.constants.game_constrants import TROOP_COSTS, TROOPS_DATA
from game_engine.models import Forge, Army, Silo


class ConstructInfantryView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, forge_id, count, add_infantry_units=None):
        # Get the Forge and Army instances
        try:
            forge = Forge.objects.get(pk=forge_id)
            army = forge.army
        except (Forge.DoesNotExist, Army.DoesNotExist):
            return Response({"error": "Forge or Army not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if enough resources are available
        planet = forge.planet
        silo = Silo.objects.get(planet=planet, name="Silo")

        # Check if there are enough resources in the Silo
        required_resources = {}
        for resource, cost in TROOP_COSTS['Infantry_units'].items():
            required_resources[resource] = cost * count

        for resource_type, required_amount in required_resources.items():
            if silo.stored_resources.get(resource_type, 0) < required_amount:
                return Response({"error": f"Not enough {resource_type} in the Silo."},
                                status=status.HTTP_400_BAD_REQUEST)

        # Deduct the resources from the Silo
        for resource_type, required_amount in required_resources.items():
            silo.stored_resources[resource_type] -= required_amount
        silo.save()

        # Schedule the construction of Infantry units
        construction_time = TROOPS_DATA['Infantry_units']['construction_time']
        for _ in range(count):
            add_infantry_units.apply_async(args=[army.pk], countdown=construction_time)
            construction_time += TROOPS_DATA['Infantry_units']['construction_time']

        return Response({"message": f"Started constructing {count} Infantry units."}, status=status.HTTP_200_OK)


class ConstructAssaultTanksView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, forge_id, count, add_assault_tanks=None):
        # Get the Forge and Army instances
        try:
            forge = Forge.objects.get(pk=forge_id)
            army = forge.army
        except (Forge.DoesNotExist, Army.DoesNotExist):
            return Response({"error": "Forge or Army not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if enough resources are available
        planet = forge.planet
        silo = Silo.objects.get(planet=planet, name="Silo")

        # Check if there are enough resources in the Silo
        required_resources = {}
        for resource, cost in TROOP_COSTS['Assault_Tanks'].items():
            required_resources[resource] = cost * count

        for resource_type, required_amount in required_resources.items():
            if silo.stored_resources.get(resource_type, 0) < required_amount:
                return Response({"error": f"Not enough {resource_type} in the Silo."},
                                status=status.HTTP_400_BAD_REQUEST)

        # Deduct the resources from the Silo
        for resource_type, required_amount in required_resources.items():
            silo.stored_resources[resource_type] -= required_amount
        silo.save()

        # Schedule the construction of Assault Tanks
        construction_time = TROOPS_DATA['Assault_Tanks']['construction_time']
        for _ in range(count):
            add_assault_tanks.apply_async(args=[army.pk], countdown=construction_time)
            construction_time += TROOPS_DATA['Assault_Tanks']['construction_time']

        return Response({"message": f"Started constructing {count} Assault Tanks."}, status=status.HTTP_200_OK)


class ConstructSentinelsView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, forge_id, count, add_sentinels=None):
        # Get the Forge and Army instances
        try:
            forge = Forge.objects.get(pk=forge_id)
            army = forge.army
        except (Forge.DoesNotExist, Army.DoesNotExist):
            return Response({"error": "Forge or Army not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if enough resources are available
        planet = forge.planet
        silo = Silo.objects.get(planet=planet, name="Silo")

        # Check if there are enough resources in the Silo
        required_resources = {}
        for resource, cost in TROOP_COSTS['Sentinels'].items():
            required_resources[resource] = cost * count

        for resource_type, required_amount in required_resources.items():
            if silo.stored_resources.get(resource_type, 0) < required_amount:
                return Response({"error": f"Not enough {resource_type} in the Silo."},
                                status=status.HTTP_400_BAD_REQUEST)

        # Deduct the resources from the Silo
        for resource_type, required_amount in required_resources.items():
            silo.stored_resources[resource_type] -= required_amount
        silo.save()

        # Schedule the construction of Sentinels
        construction_time = TROOPS_DATA['Sentinels']['construction_time']
        for _ in range(count):
            add_sentinels.apply_async(args=[army.pk], countdown=construction_time)
            construction_time += TROOPS_DATA['Sentinels']['construction_time']

        return Response({"message": f"Started constructing {count} Sentinels."}, status=status.HTTP_200_OK)


class ConstructMaraudersView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, forge_id, count):
        # Get the Forge and Army instances
        try:
            forge = Forge.objects.get(pk=forge_id)
            army = forge.army
        except (Forge.DoesNotExist, Army.DoesNotExist):
            return Response({"error": "Forge or Army not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if enough resources are available
        planet = forge.planet
        silo = Silo.objects.get(planet=planet, name="Silo")

        # Check if there are enough resources in the Silo
        required_resources = {}
        for resource, cost in TROOP_COSTS['Marauders'].items():
            required_resources[resource] = cost * count

        for resource_type, required_amount in required_resources.items():
            if silo.stored_resources.get(resource_type, 0) < required_amount:
                return Response({"error": f"Not enough {resource_type} in the Silo."},
                                status=status.HTTP_400_BAD_REQUEST)

        # Deduct the resources from the Silo
        for resource_type, required_amount in required_resources.items():
            silo.stored_resources[resource_type] -= required_amount
        silo.save()

        # Schedule the construction of Marauders
        construction_time = TROOPS_DATA['Marauders']['construction_time']
        for _ in range(count):
            add_marauders.apply_async(args=[army.pk], countdown=construction_time)
            construction_time += TROOPS_DATA['Marauders']['construction_time']

        return Response({"message": f"Started constructing {count} Marauders."}, status=status.HTTP_200_OK)


class ConstructHarvestersView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, forge_id, count, add_harvesters=None):
        # Get the Forge and Army instances
        try:
            forge = Forge.objects.get(pk=forge_id)
            army = forge.army
        except (Forge.DoesNotExist, Army.DoesNotExist):
            return Response({"error": "Forge or Army not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if enough resources are available
        planet = forge.planet
        silo = Silo.objects.get(planet=planet, name="Silo")

        # Check if there are enough resources in the Silo
        required_resources = {}
        for resource, cost in TROOP_COSTS['Harvesters'].items():
            required_resources[resource] = cost * count

        for resource_type, required_amount in required_resources.items():
            if silo.stored_resources.get(resource_type, 0) < required_amount:
                return Response({"error": f"Not enough {resource_type} in the Silo."},
                                status=status.HTTP_400_BAD_REQUEST)

        # Deduct the resources from the Silo
        for resource_type, required_amount in required_resources.items():
            silo.stored_resources[resource_type] -= required_amount
        silo.save()

        # Schedule the construction of Harvesters
        construction_time = TROOPS_DATA['Harvesters']['construction_time']
        for _ in range(count):
            add_harvesters.apply_async(args=[army.pk], countdown=construction_time)
            construction_time += TROOPS_DATA['Harvesters']['construction_time']

        return Response({"message": f"Started constructing {count} Harvesters."}, status=status.HTTP_200_OK)


class ConstructBombersView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, forge_id, count):
        # Get the Forge and Army instances
        try:
            forge = Forge.objects.get(pk=forge_id)
            army = forge.army
        except (Forge.DoesNotExist, Army.DoesNotExist):
            return Response({"error": "Forge or Army not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if enough resources are available
        planet = forge.planet
        silo = Silo.objects.get(planet=planet, name="Silo")

        # Check if there are enough resources in the Silo
        required_resources = {}
        for resource, cost in TROOP_COSTS['Bombers'].items():
            required_resources[resource] = cost * count

        for resource_type, required_amount in required_resources.items():
            if silo.stored_resources.get(resource_type, 0) < required_amount:
                return Response({"error": f"Not enough {resource_type} in the Silo."},
                                status=status.HTTP_400_BAD_REQUEST)

        # Deduct the resources from the Silo
        for resource_type, required_amount in required_resources.items():
            silo.stored_resources[resource_type] -= required_amount
        silo.save()

        # Schedule the construction of Bombers
        construction_time = TROOPS_DATA['Bombers']['construction_time']
        for _ in range(count):
            add_bombers.apply_async(args=[army.pk], countdown=construction_time)
            construction_time += TROOPS_DATA['Bombers']['construction_time']

        return Response({"message": f"Started constructing {count} Bombers."}, status=status.HTTP_200_OK)


class ConstructDroneTroopersView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, forge_id, count):
        # Get the Forge and Army instances
        try:
            forge = Forge.objects.get(pk=forge_id)
            army = forge.army
        except (Forge.DoesNotExist, Army.DoesNotExist):
            return Response({"error": "Forge or Army not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if enough resources are available
        planet = forge.planet
        silo = Silo.objects.get(planet=planet, name="Silo")

        # Check if there are enough resources in the Silo
        required_resources = {}
        for resource, cost in TROOP_COSTS['Drone_Troopers'].items():
            required_resources[resource] = cost * count

        for resource_type, required_amount in required_resources.items():
            if silo.stored_resources.get(resource_type, 0) < required_amount:
                return Response({"error": f"Not enough {resource_type} in the Silo."},
                                status=status.HTTP_400_BAD_REQUEST)

        # Deduct the resources from the Silo
        for resource_type, required_amount in required_resources.items():
            silo.stored_resources[resource_type] -= required_amount
        silo.save()

        # Schedule the construction of Drone Troopers
        construction_time = TROOPS_DATA['Drone_Troopers']['construction_time']
        for _ in range(count):
            add_drone_troopers.apply_async(args=[army.pk], countdown=construction_time)
            construction_time += TROOPS_DATA['Drone_Troopers']['construction_time']

        return Response({"message": f"Started constructing {count} Drone Troopers."}, status=status.HTTP_200_OK)
