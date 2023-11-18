from django.urls import path
from core.views import *
from core.views.attack_move_reinforce import FleetAttackView
from core.views.constructing_troops import *

urlpatterns = [

    # View galaxy map urls

    # Building view urls
    path('planet/<str:planet_id>/<str:related_name>/upgrade/', BuildingUpgradeView.as_view(),
         name='building_upgrade'),
    path('planet/<str:planet_id>/<str:related_name>/<str:resource_type>/upgrade/', BuildingUpgradeView.as_view(),
         name='mine_upgrade'),
    path('planet/<str:planet_id>/<str:related_name>/cancel/', BuildingCancelUpgradeView.as_view(), name='cancel_building_upgrade'),


    # Construct Troops:
    path('construct_infantry_units/<uuid:forge_id>/<int:count>/', ConstructInfantryView.as_view(), name='construct_infantry'),
    path('construct_bombers/<int:forge_id>/<int:count>/', ConstructBombersView.as_view(), name='construct-bombers'),
    path('construct_assault_tanks/<int:forge_id>/<int:count>/', ConstructAssaultTanksView.as_view(), name='construct-assault-tanks'),
    path('construct_drone_troopers/<int:forge_id>/<int:count>/', ConstructDroneTroopersView.as_view(), name='construct-drone-troopers'),
    path('construct_sentinels/<int:forge_id>/<int:count>/', ConstructSentinelsView.as_view(), name='construct-sentinels'),
    path('construct_harvesters/<int:forge_id>/<int:count>/', ConstructHarvestersView.as_view(), name='construct-harvesters'),
    path('construct_marauders/<int:forge_id>/<int:count>/', ConstructMaraudersView.as_view(), name='construct-marauders'),


    # Constructing Fleets
    path('fleets/create/', FleetCreateView.as_view(), name='fleet-create'),
    path('fleets/create-all/', FleetCreateWithAllTroopsView.as_view(), name='fleet-create-all'),
    path('fleets/<uuid:pk>/remove-units/', FleetRemoveUnitsView.as_view(), name='fleet-remove-units'),
    path('fleets/<uuid:pk>/remove-all-units/', FleetRemoveAllUnitsView.as_view(), name='fleet-remove-all-units'),
    path('fleets/<uuid:pk>/disband/', FleetDisbandView.as_view(), name='fleet-disband'),

    # Launch attack
    path('fleets/<uuid:pk>/attack/', FleetAttackView.as_view(), name='fleet-attack'),
]