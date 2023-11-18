from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist

from game_engine.models import Planet, Silo, Mine


@shared_task(bind=True)
def update_silos_with_mine_production(self):
    """
    This function is a Celery shared task that calculates and adds the resource production from all mines on each planet
     to their respective silos. It loops through all the planets, retrieves their associated silo and mines, calculates
     the resource increase for the past 1 second(s), updates the silo's stored resources, and saves the changes.
    :param self:
    :return:
    """
    # Retrieve all planet instances
    planets = Planet.objects.all()

    # Loop through each planet instance
    for planet in planets:

        try:
            # Try to get the Silo instance associated with the current planet
            silo = planet.silo

        except Silo.DoesNotExist:
            # If the Silo does not exist for the current planet, skip to the next iteration
            continue

        # Retrieve all Mine instances associated with the current planet
        mines = Mine.objects.filter(planet=planet)

        # Loop through each Mine instance
        for mine in mines:
            # Get the resource type produced by the mine
            resource_type = mine.resource_type

            # Calculate the increase in resources produced by the mine in the last 1 seconds
            resource_increase = mine.production_rate_per_sec * 1  # Multiply by 1 seconds

            # Update the stored resources in the Silo, ensuring it does not exceed the max capacity
            silo.stored_resources[resource_type] = min(
                silo.stored_resources[resource_type] + resource_increase,
                silo.max_capacity,
            )

        # Save the updated Silo instance
        silo.save()

    # Return a string indicating the task is complete
    return "Done"


@shared_task(bind=True)
def upgrade_mine_task(mine_id):
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
