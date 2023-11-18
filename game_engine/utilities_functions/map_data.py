from game_engine.models import Planet


def generate_map_data(galaxy=None, range=None):
    map_data = []

    if galaxy is None:
        galaxy_range = range(1, 11)  # Assuming 10 galaxies
    else:
        galaxy_range = range(galaxy, galaxy + 1)

    for galaxy in galaxy_range:
        for planet_number in range(1, 11):  # Assuming 10 planets per galaxy
            if range is None or abs(galaxy - range) <= range:
                try:
                    planet = Planet.objects.get(galaxy=galaxy, planet_number=planet_number)
                    outpost_data = {
                        "galaxy": galaxy,
                        "planet_number": planet_number,
                        "planet_name": planet.name,
                        "owner_name": planet.owner.username,
                        "occupied": True,
                    }
                except Planet.DoesNotExist:
                    outpost_data = {
                        "galaxy": galaxy,
                        "planet_number": planet_number,
                        "planet_name": None,
                        "owner_name": None,
                        "occupied": False,
                    }
                map_data.append(outpost_data)

    return map_data
