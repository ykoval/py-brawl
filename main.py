import pygame
import sys
import os

# Make sure pygame is initialized
pygame.init()

# Import all the modules
from game_engine import PyBrawl
from brawlers import BRAWLERS
from game_mechanics import patch_pybrawl_class
from input_handler import patch_pybrawl_input
from renderer import patch_pybrawl_renderer

# Patch the PyBrawl class with all needed methods
patch_pybrawl_class()
patch_pybrawl_input()
patch_pybrawl_renderer()

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
    
    # Create the game instance
    game = PyBrawl()
    
    # Run the game
    game.run()
