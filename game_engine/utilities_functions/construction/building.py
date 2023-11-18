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


