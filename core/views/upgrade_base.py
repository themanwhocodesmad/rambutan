"""
Typical upgrade function cycle:

--> request:
    ---> check if resource requirement is met: Yes or no
            --->  query silo and building
                ---> subtract upgrade resources from silo and silo.save().
                    ---> increase dynamic_resource_costs by (level+1)
                         increase dynamic_upgrade_duration by (level+1)
                         building.save()

                         ---> start background task:
                              increase level by +1 after upgrade_duration passes
                              increase building hp by +1 after upgrade_duration passes
                              building.save()

"""
from core.models import Mine, Silo, Map, Forge
from core.serializers import MineSerializer, SiloSerializer, MapSerializer, ForgeSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
import datetime

# TODO update the celery tasks and location, this is just a placeholder.
from logic.tasks import *
from celery import app


class BuildingUpgradeView(APIView):
    # permission_classes = [IsAuthenticated]

    def get_serializer_class(self, building_type):
        serializer_classes = {
            Mine: MineSerializer,
            Silo: SiloSerializer,
            Map: MapSerializer,
            Forge: ForgeSerializer,
        }
        return serializer_classes.get(building_type)

    def upgrade(self, request, planet_id, related_name, resource_type=None):
        try:
            planet = Planet.objects.get(id=planet_id, owner=request.user)
        except Planet.DoesNotExist:
            return Response({"error": "Planet not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            silo = Silo.objects.get(planet=planet)
        except Silo.DoesNotExist:
            return Response({"error": "Silo not found"}, status=status.HTTP_404_NOT_FOUND)

        if related_name == "mine" and resource_type:
            try:
                building = Mine.objects.get(planet=planet, resource_type=resource_type)
            except Mine.DoesNotExist:
                return Response({"error": f"{resource_type} Mine not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            try:
                building = getattr(planet, related_name)
            except AttributeError:
                return Response({"error": f"{related_name} not found"}, status=status.HTTP_404_NOT_FOUND)

        building_type = type(building)

        # Check if enough resources are available and subtract resources:
        for resource_type, cost in building.dynamic_resource_costs.items():
            if silo.stored_resources[resource_type] < cost:
                return Response({"error": f"Not enough {resource_type}"}, status=status.HTTP_400_BAD_REQUEST)
            silo.stored_resources[resource_type] -= cost
        silo.save()

        # Update the building dynamic upgrade cost resources for display
        pseudo_level = int(building.level) + 1
        for resource_type in building.dynamic_resource_costs:
            building.dynamic_resource_costs[resource_type] = int(
                building.base_resource_costs[resource_type] * pseudo_level)

        # Call upgrade task with the upgrade duration
        building_type_task_mapping = {
            Mine: upgrade_mine_task,
            Silo: upgrade_silo_task,
            Map: upgrade_map_task,
            Forge: upgrade_forge_task,
        }

        task_func = building_type_task_mapping.get(building_type)
        task = task_func.apply_async(args=[building.id], countdown=building.dynamic_upgrade_duration.total_seconds())

        # Save the task ID and start time to the building model
        building.dynamic_upgrade_duration = pseudo_level * building.upgrade_duration
        building.upgrade_task_id = task.id
        building.upgrade_start_time = datetime.datetime.now()
        building.save()

        serializer_class = self.get_serializer_class(building_type)
        serializer = serializer_class(building)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, planet_id, related_name, resource_type=None, *args, **kwargs):
        return self.upgrade(request, planet_id, related_name, resource_type)


class BuildingCancelUpgradeView(APIView):
    # permission_classes = [IsAuthenticated]

    def cancel(self, request, planet_id, related_name):
        try:
            planet = Planet.objects.get(id=planet_id, owner=request.user)
        except Planet.DoesNotExist:
            return Response({"error": "Planet not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            building = getattr(planet, related_name)
            building_type = type(building)
        except AttributeError:
            return Response({"error": f"{related_name} not found"}, status=status.HTTP_404_NOT_FOUND)

        if building.upgrade_task_id:
            # Calculate the percentage of time lapsed
            now = timezone.now()
            previous_upgrade_duration = building.level * building.upgrade_duration
            time_lapsed = now - building.upgrade_start_time

            time_remaining = previous_upgrade_duration - time_lapsed
            percentage_remaining = time_remaining / previous_upgrade_duration

            # Refund resources based on percentage remaining
            try:
                silo = Silo.objects.get(planet=building.planet)
            except Silo.DoesNotExist:
                return Response({"error": "Silo not found"}, status=status.HTTP_404_NOT_FOUND)

            for resource_type, cost in building.dynamic_resource_costs.items():
                refund = int(cost * percentage_remaining)
                silo.stored_resources[resource_type] += refund
                silo.save()

            # Revoke the upgrade task
            app.control.revoke(building.upgrade_task_id, terminate=True)

            # Clear the task ID and start time from the building model
            building.upgrade_task_id = None
            building.upgrade_start_time = None

            # Revert dynamic upgrade costs for display:
            for resource_type in building.dynamic_resource_costs:
                building.dynamic_resource_costs[resource_type] = int(
                    building.base_resource_costs[resource_type] * building.level)

            building.save()
            return Response({"status": "Upgrade task cancelled", "refunded_resources": refund},
                            status=status.HTTP_200_OK)
        else:
            return Response({"error": "No upgrade task found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, planet_id, related_name, *args, **kwargs):
        return self.cancel(request, planet_id, related_name)
