# Class choices
PLAYER_CLASS_CHOICES = {
    "class1": ["Gaea Guardians"],
    "class2": ["Phoenix Sentinels"],
    "class3": ["Stormbringer Ravagers"]
}


# Resource choices
RESOURCE_CHOICES = (
    ('Boron', 'Boron'),
    ('Oxygen', 'Oxygen'),
    ('Uranium', 'Uranium'),
    ('Helium', 'Helium'),
)
# Building costs
BUILDING_COSTS = {
    'Mine': {
        'Boron': 120,
        'Oxygen': 90,
        'Uranium': 140,
        'Helium': 0,
    },
    'Silo': {
        'Boron': 70,
        'Oxygen': 100,
        'Uranium': 30,
        'Helium': 0,
    },
    # Add other building types and costs here
}

# TROOPS CONSTANTS:

TROOP_COSTS = {
    'Infantry_units': {
        'Boron': 100,
        'Oxygen': 50,
        'Uranium': 300,
        'Helium': 0,
    },
    'Assault_Tanks': {
        'Boron': 300,
        'Oxygen': 200,
        'Uranium': 180,
        'Helium': 0,
    },
    'Drone_Troopers': {
        'Boron': 240,
        'Oxygen': 150,
        'Uranium': 210,
        'Helium': 0,
    },
    'Sentinels': {
        'Boron': 180,
        'Oxygen': 250,
        'Uranium': 200,
        'Helium': 0,
    },
    'Harvesters': {
        'Boron': 3000,
        'Oxygen': 2100,
        'Uranium': 1800,
        'Helium': 0,
    },
    'Bombers': {
        'Boron': 2000,
        'Oxygen': 3500,
        'Uranium': 500,
        'Helium': 0,
    },
    'Marauders': {
        'Boron': 2500,
        'Oxygen': 1500,
        'Uranium': 700,
        'Helium': 0,
    },
    'Gaea Guardians': {
        'Boron': 15000,
        'Oxygen': 5000,
        'Uranium': 20000,
        'Helium': 100,
    },
    'Phoenix Sentinels': {
        'Boron': 10000,
        'Oxygen': 8000,
        'Uranium': 18000,
        'Helium': 50,
    },
    'Stormbringer Ravagers': {
        'Boron': 12000,
        'Oxygen': 10000,
        'Uranium': 15000,
        'Helium': 150,
    },
}


TROOP_CHOICES = [
    ('Infantry', 'Infantry units'),
    ('AssaultTanks', 'Assault Tanks'),
    ('DroneTroopers', 'Drone Troopers'),
    ('Sentinels', 'Sentinels'),
    ('Harvesters', 'Harvesters'),
    ('Bombers', 'Bombers'),
    ('Marauders', 'Marauders'),
]


TROOPS_DATA = {
    'Infantry_units': {
        'attack_hp': 100,
        'defense_hp': 25,
        'speed': 9000,
        'cargo_space': 120,
        'construction_time': 160,  # seconds
        'helium_3_tax': 1,
    },
    'Assault_Tanks': {
        'attack_hp': 250,
        'defense_hp': 70,
        'speed': 11000,
        'cargo_space': 50,
        'construction_time': 300,  # seconds
        'helium_3_tax': 1,
    },
    'Drone_Troopers': {
        'attack_hp': 175,
        'defense_hp': 150,
        'speed': 15000,
        'cargo_space': 180,
        'construction_time': 385,  # seconds
        'helium_3_tax': 1,
    },
    'Sentinels': {
        'attack_hp': 80,
        'defense_hp': 150,
        'speed': 8000,
        'cargo_space': 100,
        'construction_time': 180,  # seconds
        'helium_3_tax': 1,
    },
    'Harvesters': {
        'attack_hp': 25,
        'defense_hp': 20,
        'speed': 20000,
        'cargo_space': 1000,
        'construction_time': 120,  # seconds
        'helium_3_tax': 1,
    },
    'Bombers': {
        'attack_hp': 15,
        'defense_hp': 15,
        'speed': 10000,
        'cargo_space': 1,
        'construction_time': 500,  # seconds
        'helium_3_tax': 1,
    },
    'Marauders': {
        'attack_hp': 15,
        'defense_hp': 15,
        'speed': 17000,
        'cargo_space': 450,  # Can only raid helium
        'construction_time': 90,  # seconds
        'helium_3_tax': 1,
    },
    'Gaea Guardians': {
        'attack_hp': 500,
        'defense_hp': 500,
        'speed': 10000,
        'cargo_space': 250,
        'construction_time': 1000,  # seconds
        'helium_3_tax': 2,
    },
    'Phoenix Sentinels': {
        'attack_hp': 400,
        'defense_hp': 500,
        'speed': 12000,
        'cargo_space': 100,
        'construction_time': 800,  # seconds
        'helium_3_tax': 2,
    },
    'Stormbringer Ravagers': {
        'attack_hp': 500,
        'defense_hp': 400,
        'speed': 15000,
        'cargo_space': 250,
        'construction_time': 1200,  # seconds
        'helium_3_tax': 2,
    },
}


GREEK_WORDS = [
    'alpha', 'beta', 'gamma', 'delta', 'epsilon', 'zeta', 'eta', 'theta', 'iota',
    'kappa', 'lambda', 'mu', 'nu', 'xi', 'omicron', 'pi', 'rho', 'sigma', 'tau',
    'upsilon', 'phi', 'chi', 'psi', 'omega'
]

CELESTIAL_WORDS = [
    'comet', 'asteroid', 'nebula', 'quasar', 'supernova', 'galaxy', 'black hole',
    'cosmic', 'orbit', 'planet', 'star', 'meteor', 'meteorite', 'lunar', 'solar',
    'cosmos', 'constellation', 'eclipse', 'astronomy', 'astrology', 'grav'
]

ASTROPHYSICS_WORDS = [
    'jupiter', 'neptune', 'mercury', 'mars', 'venus', 'saturn', 'uranus', 'pluto',
    'apollo', 'juno', 'vesta', 'ceres', 'mars', 'minerva', 'bacchus', 'janus',
    'diana', 'venus', 'faunus', 'vulcan', 'hercules', 'pan', 'jupiter', 'saturn'
]
