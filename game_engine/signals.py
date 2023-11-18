from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from .constants.game_constrants import RESOURCE_CHOICES
from .models import Planet, Mine, Silo, Forge, Map, UserProfile


@receiver(post_save, sender=User)
def create_initial_planet_and_buildings(sender, instance, created, **kwargs):
    if created:
        # Create a new UserProfile for the user
        UserProfile.objects.create(user=instance)

        # Create a new planet for the user
        planet = Planet(owner=instance)
        planet.save()

        # Create 4 Mines for each resource type
        for resource_type, _ in RESOURCE_CHOICES:
            mine = Mine(planet=planet, name=f'{resource_type.capitalize()} Mine', resource_type=resource_type.lower())
            mine.save()

        # Create a Silo
        silo = Silo(planet=planet, name='Silo')
        silo.save()

        # Create a Forge
        forge = Forge(planet=planet, name='Forge')
        forge.save()

        # Create a Map
        map_instance = Map(planet=planet, name='Map')
        map_instance.save()
