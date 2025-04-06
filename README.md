# Py-Brawl: A Simplified Brawl Stars Game

A beginner-friendly Python implementation of a simplified Brawl Stars-inspired game designed to help children learn programming concepts.

## Game Features

- **Start Screen**: Shows the game title and a welcome message
- **Character Selection**: Choose from different brawlers with unique stats
- **Top-Down Gameplay**: Control your brawler in a 2D arena
- **Combat Mechanics**: Shoot projectiles and defeat enemy robots
- **Level Features**: Navigate around walls and hide in bushes
- **Score System**: Earn points by defeating enemies
- **Themed Bosses**: Face challenging boss enemies with special prefixes (Chief, Commander, General, Overlord, King)
- **Boss Icons**: Each boss type has unique icons that appear alongside their names
- **Health Indicators**: Visual health bars appear above all characters
- **Ammo System**: Dynamic ammo reload indicators show your available shots and recharge progress
- **Special Boss Attacks**: Boss enemies have unique attack patterns including spread shots, burst fire, and sniper shots

## Controls

- **Arrow Keys**: Move your brawler (up, down, left, right)
- **Spacebar**: Shoot projectiles (three-shot system with reload)
- **ESC**: Return to the title screen
- **Enter**: Confirm selections, restart game after game over

## Project Structure

```
py-brawl/
├── assets/
│   └── images/
│       └── brawlers/  (Add brawler images here)
├── main.py            (Main entry point)
├── py_brawl.py        (Original entry script - forwards to main.py)
├── game_engine.py     (Core game engine)
├── game_mechanics.py  (Game logic and mechanics)
├── input_handler.py   (User input processing)
├── renderer.py        (Screen drawing and visual output)
├── brawlers.py        (Brawler definitions and stats)
├── sprites.py         (Sprite management and custom icon generation)
├── requirements.txt   (Dependencies)
└── README.md          (This file)
```

## Installation and Running

1. Ensure you have Python 3.x installed
2. Install the required dependencies:
   ```
   pip install pygame
   ```
3. Run the game:
   ```
   python py_brawl.py
   ```

## Game Mechanics

### Brawler Types
- **Shelly**: Balanced brawler with shotgun attack
- **Colt**: Fast shooter with long range
- **El Primo**: Tank with powerful close-range attacks

### Combat System
- Each brawler has a three-shot ammo system
- Ammo bars deplete from right to left as you shoot
- Empty ammo bars recharge from left to right
- Blue progress bars show recharge status
- You can fire if you have at least one fully charged (yellow) bar

### Boss System
- Boss enemies appear in every wave
- Each boss has a special prefix that determines its attack pattern and abilities
- Boss health is significantly higher than regular enemies
- Each boss type has a unique icon that appears next to its name
- Bosses use special attack patterns (spread, burst, or sniper)

## Learning Concepts for Kids

This project demonstrates many programming concepts that can help children learn to code:

### Basic Concepts
- **Variables**: Storing and manipulating data
- **Functions**: Reusable blocks of code
- **Conditionals**: Making decisions in code (if/else)
- **Loops**: Repeating actions for many items

### Intermediate Concepts
- **Classes and Objects**: Organizing code and data together
- **Event Handling**: Responding to user input
- **Collision Detection**: Detecting when objects intersect
- **Game States**: Managing different screens and modes

### Advanced Concepts
- **Game Physics**: Movement, velocity, and direction
- **Modularity**: Breaking code into manageable parts
- **Game Design**: Balancing gameplay elements

## Extension Ideas for Learning

Here are ways to extend this project as your child learns more:

1. **Add New Brawlers**: Create a new brawler with unique stats and abilities
2. **Special Abilities**: Add power-ups or special moves activated with different keys
3. **Improved Graphics**: Replace simple shapes with custom sprites and animations
4. **Sound Effects**: Add sounds for shooting, damage, and game events
5. **Multiple Levels**: Create different map layouts with increasing difficulty
6. **High Score System**: Save and display top scores using file I/O
7. **Multiplayer**: Add a second player controlled with different keys (local multiplayer)
8. **AI Improvements**: Make enemy robots smarter with better pathfinding

## Required but Missing Components

To complete the game, consider adding:

1. **Brawler Images**: Add PNG images to the `assets/images/brawlers/` folder with the names specified in `brawlers.py`
2. **Sound Effects**: Create a sounds folder and add basic game sounds
3. **Additional Brawlers**: Expand the selection with more character options
4. **Tutorial Screen**: Add instructions for first-time players

## Debugging Tips for Kids

If the game doesn't work as expected:

1. **Check the Console**: Read any error messages
2. **Print Values**: Add `print()` statements to see what's happening
3. **Change One Thing**: Make one change at a time and test
4. **Ask Questions**: Use problem-solving to identify issues

## Resources for Learning More

- [Python for Kids](https://www.nostarch.com/pythonforkids) - A beginner's guide to programming
- [Pygame Documentation](https://www.pygame.org/docs/) - Official documentation
- [Pygame Tutorials](https://www.pygame.org/wiki/tutorials) - Step-by-step guides
- [Code.org](https://code.org/) - Learn computer science fundamentals

Happy coding and have fun improving the game!
