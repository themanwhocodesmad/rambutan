import math
from celery import shared_task
from celery.loaders import app
from django.core.exceptions import ObjectDoesNotExist
from game_engine.models import Planet, Mine, Silo, Army, Fleet, Forge, Map
from decimal import Decimal


@shared_task(bind=True)
def upgrade_mine_task(self, mine_id, **kwargs):
    try:
        mine = Mine.objects.get(id=mine_id)
    except ObjectDoesNotExist:
        return

    # Upgrade the mine level, hp and production:
    mine.level += 1
    mine.hp += 100 * mine.level
    mine.production_rate_per_sec += 1

    # Clear the task ID and start time from the Mine model
    mine.upgrade_task_id = None
    mine.upgrade_start_time = None

    mine.save()


@shared_task(bind=True)
def upgrade_silo_task(self, silo_id, **kwargs):
    try:
        silo = Silo.objects.get(id=silo_id)
    except ObjectDoesNotExist:
        return

    # Upgrade the mine level, hp and production:
    silo.level += 1
    silo.hp += 100 * silo.level
    silo.max_capacity += 10000

    # Clear the task ID and start time from the Mine model
    silo.upgrade_task_id = None
    silo.upgrade_start_time = None

    silo.save()


@shared_task(bind=True)
def upgrade_map_task(self, mine_id, **kwargs):
    try:
        map1 = Map.objects.get(id=mine_id)
    except ObjectDoesNotExist:
        return

    # Upgrade the mine level, hp and production:
    map1.level += 1
    map1.hp += 100 * map1.level

    # Clear the task ID and start time from the Mine model
    map1.upgrade_task_id = None
    map1.upgrade_start_time = None

    map1.save()


@shared_task(bind=True)
def upgrade_forge_task(self, forge_id, **kwargs):
    try:
        forge = Forge.objects.get(id=forge_id)
    except ObjectDoesNotExist:
        return

    # Upgrade the forge level, hp and production:
    forge.level += 1
    forge.hp += 100 * forge.level

    # Clear the task ID and start time from the Forge model
    forge.upgrade_task_id = None
    forge.upgrade_start_time = None

    forge.save()


# TODO: Check validity of update generated resources function
@shared_task(bind=True)
def update_silo_resources():
    planets = Planet.objects.all()

    for planet in planets:
        try:
            silo = Silo.objects.get(planet=planet)
        except Silo.DoesNotExist:
            continue

        mines = Mine.objects.filter(planet=planet)

        for mine in mines:
            resource_type = mine.resource_type
            resource_increase = Decimal(mine.production_rate_per_sec) * 10  # Multiply by 10 seconds
            silo.stored_resources[resource_type] = min(
                silo.stored_resources[resource_type] + resource_increase,
                silo.max_capacity,
            )

        silo.save()


@shared_task(bind=True)
def add_infantry_units(army_id):
    army = Army.objects.get(pk=army_id)
    if army.troops['Infantry_units']['in_construction'] > 0:
        army.troops['Infantry_units']['count'] += 1
        army.troops['Infantry_units']['in_construction'] -= 1
        army.save()

        # construction_time = TROOPS_DATA['Infantry_units']['construction_time']
        # add_infantry_units.apply_async(args=[army.pk], countdown=construction_time)


@shared_task(bind=True)
def add_assault_tanks(army_id):
    army = Army.objects.get(pk=army_id)
    if army.troops['Assault_Tanks']['in_construction'] > 0:
        army.troops['Assault_Tanks']['count'] += 1
        army.troops['Assault_Tanks']['in_construction'] -= 1
        army.save()


@shared_task(bind=True)
def add_drone_troopers(army_id):
    army = Army.objects.get(pk=army_id)
    if army.troops['Drone_Troopers']['in_construction'] > 0:
        army.troops['Drone_Troopers']['count'] += 1
        army.troops['Drone_Troopers']['in_construction'] -= 1
        army.save()


@shared_task(bind=True)
def add_sentinels(army_id):
    army = Army.objects.get(pk=army_id)
    if army.troops['Sentinels']['in_construction'] > 0:
        army.troops['Sentinels']['count'] += 1
        army.troops['Sentinels']['in_construction'] -= 1
        army.save()


@shared_task(bind=True)
def add_bombers(army_id):
    army = Army.objects.get(pk=army_id)
    if army.troops['Bombers']['in_construction'] > 0:
        army.troops['Bombers']['count'] += 1
        army.troops['Bombers']['in_construction'] -= 1
        army.save()


@shared_task(bind=True)
def add_marauders(army_id):
    army = Army.objects.get(pk=army_id)
    if army.troops['Marauders']['in_construction'] > 0:
        army.troops['Marauders']['count'] += 1
        army.troops['Marauders']['in_construction'] -= 1
        army.save()


@shared_task(bind=True)
def add_harvesters(army_id):
    army = Army.objects.get(pk=army_id)
    if army.troops['Harvesters']['in_construction'] > 0:
        army.troops['Harvesters']['count'] += 1
        army.troops['Harvesters']['in_construction'] -= 1
        army.save()


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
