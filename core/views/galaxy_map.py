from logic.utils import generate_map_data
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from core.models import Map


class GalaxyMapView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, galaxy, *args, **kwargs):
        home_galaxy = request.user.planet_set.first().galaxy
        map_building = Map.objects.get(planet__owner=request.user)
        map_range = map_building.range
        map_data = generate_map_data(galaxy=galaxy, range=map_range)
        return Response({"home_galaxy": home_galaxy, "map_data": map_data})
