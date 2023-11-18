from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Planet, Mine, Silo, Forge, Map, UserProfile


# Define inline admin classes for related models
class PlanetInline(admin.TabularInline):
    model = Planet
    extra = 1


class MineInline(admin.StackedInline):
    model = Mine
    extra = 1


class SiloInline(admin.StackedInline):
    model = Silo
    extra = 1


class MapInline(admin.StackedInline):
    model = Map
    extra = 1


# Custom ForgeInline admin class
class ForgeInline(admin.StackedInline):
    model = Forge
    extra = 1
    readonly_fields = ('army_troops',)

    # Custom method to display Army troops
    def army_troops(self, obj):
        if obj.army:
            return ', '.join(
                [f"{troop_name}: {troop_data['count']}" for troop_name, troop_data in obj.army.troops.items()])
        return 'No troops'

    army_troops.short_description = 'Army Troops'


# Define admin class for User model with related planets
class UserAdmin(BaseUserAdmin):
    inlines = [PlanetInline]
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff')


# Define admin class for Planet model with related buildings, mines, and silos
class PlanetAdmin(admin.ModelAdmin):
    inlines = [MineInline, SiloInline, ForgeInline, MapInline]
    list_display = ('id', 'name', 'owner', 'galaxy', 'planet_number')


class SiloAdmin(admin.ModelAdmin):
    list_display = ('id', 'planet', 'owner')

    def owner(self, obj):
        return obj.planet.owner

    owner.short_description = 'Owner'


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profiles'


class CustomUserAdmin(BaseUserAdmin):
    inlines = [UserProfileInline]  # Add UserProfileInline to the User admin


# Unregister the default User admin and register the custom UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Register the UserProfileAdmin
admin.site.register(UserProfile)

# Register the PlanetAdmin
admin.site.register(Planet, PlanetAdmin)

# Register the SiloAdmin
admin.site.register(Silo, SiloAdmin)
