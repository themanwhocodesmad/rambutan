from django.contrib.auth.models import User

from users.serializers import UserSerializer
from rest_framework import serializers
from .models import Planet, Building, Mine, Silo, Fleet, Map, Forge, UserProfile, Army


class PlanetIdSerializer(serializers.ModelSerializer):
    """
    Serializer for Planet objects that only includes the planet ID.
    """

    class Meta:
        model = Planet
        fields = ('id',)


class UserProfileSearchSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = UserProfile
        fields = (
            "population",
            "attack_points",
            "defense_points",
            "raiding_points",
            "player_class",
            "special_troops",
            "user",
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ('id', 'orion_credits', 'population', 'attack_points', 'defense_points', 'raiding_points',
                  'player_class_choices', 'player_class', 'special_troops', 'user')


class PlanetSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Planet
        fields = '__all__'


class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = '__all__'

    def to_representation(self, instance):
        if isinstance(instance, Mine):
            return MineSerializer(instance).data
        elif isinstance(instance, Silo):
            return SiloSerializer(instance).data
        elif isinstance(instance, Map):
            return MapSerializer(instance).data
        elif isinstance(instance, Forge):
            return ForgeSerializer(instance).data
        return super().to_representation(instance)


class MineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mine
        fields = '__all__'


class SiloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Silo
        fields = '__all__'


class MapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Map
        fields = '__all__'


class ForgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forge
        fields = '__all__'


class TroopsField(serializers.Field):
    def to_representation(self, value):
        return [{"troop_name": k, "count": v["count"]} for k, v in value.items()]


class ArmySerializer(serializers.ModelSerializer):
    troops = TroopsField()

    class Meta:
        model = Army
        fields = ('troops',)


class UserProfileTroopsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ("special_troops",)


class ForgeWithTroopsSerializer(serializers.ModelSerializer):
    user_profile = UserProfileTroopsSerializer()
    troops = ArmySerializer(many=True, read_only=True)

    class Meta:
        model = Forge
        fields = (
            "id",
            "name",
            "level",
            "upgrade_duration",
            "dynamic_upgrade_duration",
            "upgrade_task_id",
            "upgrade_start_time",
            "user_profile",
            "troops",
        )


class FleetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fleet
        fields = ['id', 'name', 'planet', 'troops']
