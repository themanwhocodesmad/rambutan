import math
from celery import shared_task
from celery.loaders import app
from django.core.exceptions import ObjectDoesNotExist
from game_engine.models import Planet, Mine, Silo, Army, Fleet, Forge, Map
from decimal import Decimal


@shared_task(bind=True)
def process_attack(attacker_fleet_id, defender_planet_id):
    attacker_fleet = Fleet.objects.get(id=attacker_fleet_id)
    defender_planet = Planet.objects.get(id=defender_planet_id)
    defender_forge = Forge.objects.get(planet_id=defender_planet_id)
    defender_army = Army.objects.get(planet_id=defender_planet_id)

    attacker_hp = sum(troop['attack_hp'] * count for troop, count in attacker_fleet.troops.items())
    defender_hp = sum(troop['defense_hp'] * count for troop, count in defender_army.troops.items())

    if attacker_hp > defender_hp:
        winner = "attacker"
        loser = "defender"
    else:
        winner = "defender"
        loser = "attacker"

    loss_ratio = (attacker_hp / defender_hp) ** 1.5

    if winner == "attacker":
        # Remove a percentage of attacker's units equal to the loss ratio
        for troop in attacker_fleet.troops:
            attacker_fleet.troops[troop] = math.floor(attacker_fleet.troops[troop] * (1 - loss_ratio))
            defender_army.troops[troop] = 0
    else:
        # Remove a percentage of defender's units equal to the loss ratio
        for troop in defender_army.troops:
            defender_army.troops[troop] = math.floor(defender_army.troops[troop] * (1 - loss_ratio))
            attacker_fleet.troops[troop] = 0

    # TODO : Add attacker points and raider points

    attacker_fleet.save()
    defender_army.save()
