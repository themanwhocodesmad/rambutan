from django.urls import path
from .views import BuildingViewSet, SpecificBuildingViewSet, PlayerPlanetsView, ChangePlayerClassView, \
    UserProfileView, UserProfileSearchView, ForgeWithTroopsView, PlayerPlanetIdsView, UserPlanetsView, \
    CurrentPlanetDetailsView

urlpatterns = [

    path('all_my_planets/', UserPlanetsView.as_view(), name='my_planets'),
    path('current_planet_info/<str:planet_id>/', CurrentPlanetDetailsView.as_view(), name='planet-details'),
    # Get player's building characteristics and values
    path('current_planet/<str:planet_id>/buildings/<str:building_type>/',
         SpecificBuildingViewSet.as_view({'get': 'list'}),
         name='buildings_by_type'),

    # Get player planet ids
    path('player-planet-ids/', PlayerPlanetIdsView.as_view(), name='player_planet_ids'),
    path('profile/', UserProfileView.as_view(), name='view_your_player_profile'),
    path('search-players/<str:username>/', UserProfileSearchView.as_view(), name='view_other_players_profile'),
    path('change_player_class/', ChangePlayerClassView.as_view(), name='change_player_class'),

    path('planet/<str:planet_id>/all_building_stats/', BuildingViewSet.as_view({'get': 'list'}), name='planet_buildings'),
    path('planets/', PlayerPlanetsView.as_view(), name='player_planets'),

    # Troops
    path("planet/<str:planet_id>/forge_with_troops/", ForgeWithTroopsView.as_view(), name="forge_with_troops"),

]
