# Brawler data definitions

# Colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
YELLOW = (255, 255, 0)

# Brawler data - can be expanded with more brawlers
BRAWLERS = {
    "Shelly": {
        "health": 100,
        "speed": 5,
        "damage": 20,
        "attack_speed": 1.0,
        "range": 200,
        "image": "shelly.png",
        "color": BLUE,
        "description": "Balanced brawler with shotgun attack"
    },
    "Colt": {
        "health": 80,
        "speed": 6,
        "damage": 15,
        "attack_speed": 1.5,
        "range": 300,
        "image": "colt.png",
        "color": RED,
        "description": "Fast shooter with long range"
    },
    "El Primo": {
        "health": 150,
        "speed": 4,
        "damage": 30,
        "attack_speed": 0.8,
        "range": 100,
        "image": "el_primo.png",
        "color": GREEN,
        "description": "Tank with powerful close-range attacks"
    }
}
