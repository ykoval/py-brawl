import pygame
import sys
import random
import os
import math
from enum import Enum

# Initialize pygame
pygame.init()

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
BROWN = (165, 42, 42)

# Game states
class GameState(Enum):
    TITLE = 0
    CHARACTER_SELECT = 1
    GAMEPLAY = 2
    GAME_OVER = 3

# Import game modules
from brawlers import BRAWLERS
from game_engine import PyBrawl
from game_mechanics import setup as setup_game_mechanics
from input_handler import patch_pybrawl_input
from renderer import patch_pybrawl_class as patch_renderer

# Patch the PyBrawl class with all needed methods
setup_game_mechanics(PyBrawl)
patch_pybrawl_input()
patch_renderer()

# Add BRAWLERS to PyBrawl class
PyBrawl.BRAWLERS = BRAWLERS

# Run the game if the script is executed directly
if __name__ == "__main__":
    # Print welcome message
    print("Starting Py Brawl - A simplified Brawl Stars inspired game!")
    print("Controls:")
    print("  - Arrow keys: Move your brawler")
    print("  - Spacebar: Shoot")
    print("  - ESC: Return to title screen")
    
    game = PyBrawl()
    game.run()
