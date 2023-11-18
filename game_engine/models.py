import uuid
from datetime import timedelta
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import JSONField, Sum
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
import random

from game_engine.constants.game_constrants import PLAYER_CLASS_CHOICES, CELESTIAL_WORDS, ASTROPHYSICS_WORDS, \
    GREEK_WORDS, TROOP_CHOICES, TROOPS_DATA, RESOURCE_CHOICES, BUILDING_COSTS


class GameMode(models.Model):
    CLASSICAL = 'Classical'
    RAPID = 'Rapid'

    MODE_CHOICES = [
        (CLASSICAL, 'Classical'),
        (RAPID, 'Rapid'),
    ]

    name = models.CharField(max_length=50, choices=MODE_CHOICES)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profiles')
    # Use the primary key of the GameMode instance as the default value
    game_mode = models.ForeignKey(GameMode, on_delete=models.CASCADE, default=1)
    display_name = models.CharField(max_length=50, unique=True)
    orion_credits = models.PositiveIntegerField(default=1000)
    population = models.PositiveIntegerField(default=0)
    attack_points = models.PositiveIntegerField(default=0)
    defense_points = models.PositiveIntegerField(default=0)
    raiding_points = models.PositiveIntegerField(default=0)
    player_class_choices = models.JSONField(default=dict)
    player_class = models.CharField(max_length=50, default='class1', null=True, blank=True)
    special_troops = models.JSONField(default=dict)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.special_troops:
            self.special_troops = PLAYER_CLASS_CHOICES[self.player_class]

    class Meta:
        unique_together = ('user', 'game_mode', 'display_name')  # Ensure each user can have only one profile per game mode with a unique display name

    def __str__(self):
        return f"{self.user.username} - {self.game_mode.name} - {self.display_name}"


def generate_random_name():
    word_lists = [CELESTIAL_WORDS, ASTROPHYSICS_WORDS, GREEK_WORDS]
    words = [random.choice(lst) for lst in word_lists]
    return '-'.join(words)


# Model for the planet(s):
class Planet(models.Model):
    """
    can have multiple planets. also creates the planet's name
    and coordinates
    """
    galaxy = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)], editable=False)
    planet_number = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)], editable=False)
    name = models.CharField(max_length=50, default=generate_random_name)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)

    class Meta:
        ordering = ['galaxy', 'planet_number']
        unique_together = ('galaxy', 'planet_number')

    # Create a new id, defined in below overridden save() function.
    id = models.CharField(max_length=12, primary_key=True, default='', editable=False)

    def generate_new_id(self):
        max_planet_number = Planet.objects.filter(galaxy=self.galaxy).aggregate(models.Max('planet_number'))[
            'planet_number__max']
        if max_planet_number is not None and max_planet_number >= 10:
            self.galaxy += 1
            self.planet_number = 1
        else:
            self.planet_number = (max_planet_number or 0) + 1
        return f"G{self.galaxy:02d}P{self.planet_number:02d}"

    def save(self, *args, **kwargs):
        if not self.id:  # object is being created
            self.id = self.generate_new_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.id


# Model describing what a building or structure is:
class Building(models.Model):
    """
    Ties all buildings to a planet. A single planet can have
    multiple buildings.

    Common fields for Building, Map, Forge, etc.

    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, default='Default Building', editable=False)
    level = models.PositiveSmallIntegerField(default=1)

    base_resource_costs = JSONField(default=dict)
    upgrade_duration = models.DurationField(default=timedelta(seconds=5))

    dynamic_resource_costs = JSONField(default=dict)
    dynamic_upgrade_duration = models.DurationField(default=timedelta(seconds=5))

    arithmetic_population = models.PositiveSmallIntegerField(default=0)
    hp = models.PositiveSmallIntegerField(default=100)

    # Add the upgrade_task_id and upgrade_start_time attributes
    upgrade_task_id = models.CharField(max_length=255, null=True, blank=True)
    upgrade_start_time = models.DateTimeField(null=True, blank=True)

    def initialize_base_resource_costs(self, building_type=None):
        if building_type and building_type in BUILDING_COSTS:
            costs = BUILDING_COSTS[building_type]
            for resource_type, cost in costs.items():
                self.base_resource_costs[resource_type] = cost
        else:
            for resource_type, _ in RESOURCE_CHOICES:
                self.base_resource_costs[resource_type] = 100

    def __init__(self, *args, **kwargs):
        building_type = kwargs.pop('building_type', None)
        super().__init__(*args, **kwargs)
        if not self.base_resource_costs:
            self.initialize_base_resource_costs(building_type)
        if not self.dynamic_resource_costs:
            self.initialize_dynamic_resource_costs()

    def initialize_dynamic_resource_costs(self):
        for resource_type in self.base_resource_costs:
            self.dynamic_resource_costs[resource_type] = self.base_resource_costs[resource_type]

    def __str__(self):
        return self.name


class Mine(Building):
    generated_resources = models.PositiveIntegerField(default=0)
    production_rate_per_sec = models.PositiveIntegerField(default=1)  # Change this line
    resource_type = models.CharField(max_length=10, choices=RESOURCE_CHOICES)
    planet = models.ForeignKey(Planet, on_delete=models.CASCADE, related_name='%(class)s_mine')

    class Meta:
        unique_together = ('planet', 'resource_type')

    def __init__(self, *args, **kwargs):
        super().__init__(building_type='Mine', *args, **kwargs)


class Silo(Building):
    stored_resources = JSONField(default=dict)
    max_capacity = models.PositiveIntegerField(default=20000)
    building_type = models.CharField(max_length=10, default='Silo')
    planet = models.OneToOneField(Planet, on_delete=models.CASCADE, related_name='silo')

    def __init__(self, *args, **kwargs):
        super().__init__(building_type='Silo', *args, **kwargs)
        if not self.stored_resources:
            self.initialize_resource_storage()

    def initialize_resource_storage(self):
        for resource_type, _ in RESOURCE_CHOICES:
            if resource_type not in self.stored_resources:
                self.stored_resources[resource_type] = 10000


class Map(Building):
    base_range = models.IntegerField(default=1)
    planet = models.OneToOneField(Planet, on_delete=models.CASCADE, related_name='map')

    @property
    def range(self):
        return self.base_range * self.level


class Army(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    planet = models.OneToOneField(Planet, on_delete=models.CASCADE, related_name='army')
    troops = JSONField(default=dict)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.troops:
            self.initialize_troops()

    def initialize_troops(self):
        # Get the user profile for the current planet's owner
        user_profile = UserProfile.objects.get(user=self.planet.owner)

        # Initialize basic troops
        for troop_name, _ in TROOP_CHOICES:
            self.troops[troop_name] = {
                'count': 0,
                'in_construction': 0,
            }

        # Add special troops based on the player's class
        for special_troop in user_profile.special_troops:
            self.troops[special_troop] = {
                'count': 0,
                'in_construction': 0,
            }

    def __str__(self):
        return f"Army of planet {self.planet_id}"


class Forge(Building):
    army = models.OneToOneField(Army, on_delete=models.CASCADE, related_name='forge', null=True, blank=True)
    planet = models.OneToOneField(Planet, on_delete=models.CASCADE, related_name='forge')

    def __init__(self, *args, **kwargs):
        kwargs['building_type'] = 'Forge'
        super().__init__(*args, **kwargs)
        self.name = 'Forge'

    def save(self, *args, **kwargs):
        is_new = not self.pk
        super().save(*args, **kwargs)
        if is_new:
            army = Army.objects.create(planet=self.planet)
            self.army = army
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} on {self.planet_id}"


class Fleet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    planet = models.ForeignKey(Planet, on_delete=models.CASCADE, related_name='fleets')
    troops = JSONField(default=dict)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.troops:
            self.initialize_troops()

    def initialize_troops(self):
        for troop_name, _ in TROOP_CHOICES:
            self.troops[troop_name] = 0

    def total_troops(self):
        return sum(self.troops.values())

    def total_attack_hp(self):
        return sum(
            [self.troops[troop_name] * TROOPS_DATA[f"{troop_name}_units"]['attack_hp'] for troop_name in self.troops])

    def total_defense_hp(self):
        return sum(
            [self.troops[troop_name] * TROOPS_DATA[f"{troop_name}_units"]['defense_hp'] for troop_name in self.troops])

    def total_cargo_space(self):
        return sum(
            [self.troops[troop_name] * TROOPS_DATA[f"{troop_name}_units"]['cargo_space'] for troop_name in self.troops])

    def max_travel_speed(self):
        return min(
            [TROOPS_DATA[f"{troop_name}_units"]['speed'] for troop_name in self.troops if self.troops[troop_name] > 0])

    def __str__(self):
        return f"{self.name} on {self.planet_id}"
