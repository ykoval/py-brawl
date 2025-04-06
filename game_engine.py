import pygame
import sys
import random
import os
import math
from enum import Enum
from sprites import SpriteManager

# Import brawler data
from brawlers import BRAWLERS

# Game states
class GameState(Enum):
    TITLE = 0
    CHARACTER_SELECT = 1
    GAMEPLAY = 2
    GAME_OVER = 3
    WIN_SCREEN = 4

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

class PyBrawl:
    def __init__(self):
        """Initialize the game components"""
        # Set up the display
        pygame.init()
        
        # Initialize the window
        pygame.display.set_caption("Py Brawl")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        
        # Initialize fullscreen variables
        self.is_fullscreen = False
        self.x_offset = 0
        self.y_offset = 0
        self.scale_factor = 1.0
        self.original_width = SCREEN_WIDTH
        self.original_height = SCREEN_HEIGHT
        
        # Initialize sprite manager
        self.sprite_manager = SpriteManager()
        
        # Game state
        self.state = GameState.TITLE
        self.selected_brawler = None
        self.player = None
        self.enemies = []
        self.bullets = []
        self.score = 0
        
        # Map elements
        self.walls = []
        self.bushes = []
        self.map_width = 20  # Number of tiles horizontally
        self.map_height = 15  # Number of tiles vertically
        self.tile_size = 40  # Size of each tile
        
        # Load fonts
        self.title_font = pygame.font.SysFont("Arial", 72, bold=True)
        self.menu_font = pygame.font.SysFont("Arial", 36)
        self.info_font = pygame.font.SysFont("Arial", 24)
        self.bot_nickname_font = pygame.font.SysFont("Arial", 16)  # Smaller font for bot nicknames
        
        # Initialize sounds
        pygame.mixer.init()
        self.sounds = {}
        self.load_sounds()
        
        # Try to load brawler images, if not available, use colored rectangles
        self.brawler_images = {}
        for brawler_name in BRAWLERS:
            try:
                img_path = os.path.join("assets", "images", "brawlers", BRAWLERS[brawler_name]["image"])
                self.brawler_images[brawler_name] = pygame.image.load(img_path)
                self.brawler_images[brawler_name] = pygame.transform.scale(
                    self.brawler_images[brawler_name], (100, 150))
            except:
                # If image loading fails, we'll use colored rectangles later
                pass
        
        # Wave tracking
        self.current_wave = 0
        self.max_waves = 3
        self.wave_size = 5  # Number of enemies per wave
        
        # Add persistent sets to track used name words across all waves
        self.used_first_words = set()
        self.used_second_words = set()
        self.used_names = set()
    
    def load_sounds(self):
        """Load sound effects using a simplified approach"""
        # Initialize mixer with specific settings for better audio
        pygame.mixer.quit()  # Reset mixer if previously initialized
        pygame.mixer.init(22050, -16, 2, 1024)  # Lower sample rate for deeper sounds
        pygame.mixer.set_num_channels(16)  # Allow more simultaneous sounds
        
        # Create simple but effective sounds
        try:
            # Create a deeper shotgun-like sound
            shotgun_length = 4000  # Longer sample for deeper sound
            shotgun_arr = pygame.sndarray.array([0] * shotgun_length)
            
            # Create a deeper, sharper attack
            attack_length = 300
            for i in range(attack_length):
                # Add lower frequency components
                base_freq = 80  # Lower base frequency
                if i < 100:  # Very sharp attack at the beginning
                    amplitude = 16000 * (1 - i/200)
                else:
                    amplitude = 8000 * (1 - (i-100)/200)
                
                # Add noise plus some bass components for depth
                noise = random.random() * 2 - 1
                bass = math.sin(2 * math.pi * base_freq * i / 22050) * 0.5  # Add some bass
                shotgun_arr[i] = int(amplitude * (noise * 0.7 + bass * 0.3))  # Mix noise and bass
            
            # Add some deeper sustain and rumble
            decay_length = 2000
            for i in range(attack_length, attack_length + decay_length):
                # Decaying rumble
                amplitude = 4000 * (1 - (i-attack_length)/decay_length)**2
                noise = random.random() * 2 - 1
                bass = math.sin(2 * math.pi * 60 * i / 22050) * 0.6
                shotgun_arr[i] = int(amplitude * (noise * 0.6 + bass * 0.4))
            
            # Rest of decay
            for i in range(attack_length + decay_length, shotgun_length):
                amplitude = 1000 * (1 - (i-attack_length-decay_length)/(shotgun_length-attack_length-decay_length))
                shotgun_arr[i] = int(amplitude * (random.random() * 2 - 1) * 0.5)
            
            # Create the sound from the array
            self.sounds["shoot"] = pygame.sndarray.make_sound(shotgun_arr)
            self.sounds["shoot"].set_volume(1.0)  # Full volume for the lower sound
            
            # Create a higher pitched sound for hits
            arr = pygame.sndarray.array([4096 * math.sin(x/5.0) for x in range(500)])
            self.sounds["hit"] = pygame.sndarray.make_sound(arr)
            self.sounds["hit"].set_volume(1.0)
            
            # Create a lower pitched sound for explosions
            arr = pygame.sndarray.array([4096 * math.sin(x/20.0) for x in range(1000)])
            self.sounds["explosion"] = pygame.sndarray.make_sound(arr)
            self.sounds["explosion"].set_volume(1.0)
        except Exception as e:
            # Set fallback sounds that should work in most environments
            try:
                # Use absolute frequency values for more reliable sound
                beep_frequency = 440  # A standard A note
                sample_rate = 22050   # CD quality
                
                # Generate a simple sine wave
                buffer = bytearray(int(sample_rate * 0.5))  # 0.5 second sound
                for i in range(len(buffer)):
                    buffer[i] = int(127 + 127 * math.sin(2 * math.pi * beep_frequency * i / sample_rate))
                
                self.sounds["shoot"] = pygame.mixer.Sound(buffer=buffer)
                self.sounds["hit"] = pygame.mixer.Sound(buffer=buffer)
                self.sounds["explosion"] = pygame.mixer.Sound(buffer=buffer)
            except:
                self.sounds["shoot"] = None
                self.sounds["hit"] = None
                self.sounds["explosion"] = None
    
    def play_sound(self, sound_name):
        """Play a sound effect if it exists"""
        if sound_name in self.sounds and self.sounds[sound_name] is not None:
            try:
                # Play on channel 0 to ensure it always plays
                channel = pygame.mixer.Channel(0)
                channel.play(self.sounds[sound_name])
            except Exception as e:
                pass
    
    def toggle_fullscreen(self):
        """Toggle between fullscreen and windowed mode"""
        self.is_fullscreen = not self.is_fullscreen
        
        if self.is_fullscreen:
            # For Mac, the display info doesn't always work correctly before going fullscreen
            
            # First, go to fullscreen using the system's native resolution
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            
            # Now get the actual resolution we're running at
            screen_width = pygame.display.Info().current_w
            screen_height = pygame.display.Info().current_h
            
            # If we still get invalid resolution (sometimes happens on Mac)
            if screen_width <= SCREEN_WIDTH or screen_height <= SCREEN_HEIGHT:
                # Use the user's reported resolution as fallback
                screen_width = 1728
                screen_height = 1117
            
            print(f"Actual fullscreen size: {screen_width}x{screen_height}")
            
            # Calculate scale factors for both dimensions
            width_scale = screen_width / self.original_width
            height_scale = screen_height / self.original_height
            
            # Use the smaller scale to ensure the entire game fits on screen
            self.scale_factor = min(width_scale, height_scale)
            
            # Calculate centered position for the game surface
            # This ensures equal empty space on left and right sides
            self.x_offset = int((screen_width - (self.original_width * self.scale_factor)) / 2)
            self.y_offset = int((screen_height - (self.original_height * self.scale_factor)) / 2)
            
            print(f"Fullscreen mode: Screen size = {screen_width}x{screen_height}")
            print(f"Scale factor = {self.scale_factor}")
            print(f"Offsets: x = {self.x_offset}, y = {self.y_offset}")
            
            # Fill screen with black to cover areas outside the game
            self.screen.fill((0, 0, 0))
        else:
            # Switch back to windowed mode
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.scale_factor = 1.0
            self.x_offset = 0
            self.y_offset = 0
    
    def run(self):
        """Main game loop"""
        while True:
            # Clear the screen first
            if self.is_fullscreen:
                self.screen.fill((0, 0, 0))
            
            # Handle input based on current game state
            if self.state == GameState.TITLE:
                self.handle_title_screen_input()
                self.draw_title_screen()
            elif self.state == GameState.CHARACTER_SELECT:
                self.handle_character_select_input()
                self.draw_character_select()
            elif self.state == GameState.GAMEPLAY:
                self.handle_gameplay_input()
                self.update_gameplay()
                self.draw_gameplay()
            elif self.state == GameState.GAME_OVER:
                self.handle_game_over_input()
                self.draw_game_over()
            elif self.state == GameState.WIN_SCREEN:
                self.handle_win_screen_input()
                self.draw_win_screen()
            
            # Update display
            pygame.display.flip()
            
            # Control game speed
            self.clock.tick(FPS)
    
    def reset_game(self, brawler_name):
        """Reset the game state to start a new game with the selected brawler"""
        self.selected_brawler = brawler_name
        brawler_data = BRAWLERS[brawler_name]
        
        # Generate map first (walls and bushes)
        self.generate_map()
        
        # Find a safe spawn position for the player
        player_width = 30
        player_height = 30
        safe_position = self.find_safe_spawn_position(player_width, player_height)
        
        # Create player with safe spawn position
        self.player = {
            "x": safe_position[0],
            "y": safe_position[1],
            "width": player_width,
            "height": player_height,
            "health": brawler_data["health"],
            "max_health": brawler_data["health"],
            "speed": brawler_data["speed"],
            "damage": brawler_data["damage"],
            "attack_speed": brawler_data["attack_speed"],
            "range": brawler_data["range"],
            "last_attack_time": 0,
            "color": brawler_data["color"],
            "direction": 0  # Angle in degrees
        }
        
        # Load player sprite based on selected brawler
        sprite_key = None
        if brawler_name == "Shelly":
            sprite_key = "shelly"
        elif brawler_name == "Colt":
            sprite_key = "colt"
        elif brawler_name == "El Primo":
            sprite_key = "el_primo"
        else:
            # For custom brawler or other cases
            sprite_key = "custom"  # If you have a custom sprite for the custom brawler
        
        # Try to load the sprite from the sprite manager
        if hasattr(self, 'sprite_manager') and sprite_key:
            if sprite_key == "custom":
                # For custom sprite, try to load directly from the assets folder
                custom_path = os.path.join("assets", "sprite.png")
                if os.path.exists(custom_path):
                    try:
                        self.player_sprite = pygame.image.load(custom_path).convert_alpha()
                        # Resize to appropriate dimensions
                        self.player_sprite = pygame.transform.scale(self.player_sprite, (player_width, player_height))
                        print(f"Loaded custom player sprite from {custom_path}")
                    except Exception as e:
                        print(f"Error loading custom sprite: {e}")
                        self.player_sprite = None
                else:
                    print(f"Custom sprite not found at {custom_path}")
                    self.player_sprite = None
            else:
                # Try to get sprite from sprite manager
                if sprite_key in self.sprite_manager.sprites:
                    sprite = self.sprite_manager.sprites[sprite_key]
                    # Resize to player dimensions
                    self.player_sprite = pygame.transform.scale(sprite, (player_width, player_height))
                    print(f"Loaded sprite '{sprite_key}' for {brawler_name}")
                else:
                    print(f"Warning: Sprite '{sprite_key}' not found in sprite manager")
                    self.player_sprite = None
        else:
            print("No sprite manager available or no sprite key determined")
            self.player_sprite = None
        
        # Clear previous game objects
        self.enemies = []
        self.bullets = []
        self.score = 0
        self.current_wave = 0
        
        # Spawn initial enemies
        self.spawn_enemies(self.wave_size)
        
        # Set state to gameplay
        self.state = GameState.GAMEPLAY
        
    def find_safe_spawn_position(self, width, height):
        """Find a spawn position that doesn't collide with any walls"""
        # Start with center of the screen as default
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        
        # Try center first
        if not self.position_collides_with_walls(center_x, center_y, width, height):
            return (center_x, center_y)
        
        # If center is not safe, try predefined safe positions
        safe_positions = [
            (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4),
            (SCREEN_WIDTH // 4, 3 * SCREEN_HEIGHT // 4),
            (3 * SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4),
            (3 * SCREEN_WIDTH // 4, 3 * SCREEN_HEIGHT // 4),
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4),
            (SCREEN_WIDTH // 2, 3 * SCREEN_HEIGHT // 4),
            (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2),
            (3 * SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
        ]
        
        # Try each predefined position
        for pos in safe_positions:
            if not self.position_collides_with_walls(pos[0], pos[1], width, height):
                return pos
        
        # If none of the predefined positions work, scan the map for a safe spot
        for x in range(self.tile_size * 2, SCREEN_WIDTH - self.tile_size * 2, self.tile_size):
            for y in range(self.tile_size * 2, SCREEN_HEIGHT - self.tile_size * 2, self.tile_size):
                if not self.position_collides_with_walls(x, y, width, height):
                    return (x, y)
        
        # If all else fails, return center and hope for the best
        print("Warning: Could not find a safe spawn position!")
        return (center_x, center_y)
    
    def position_collides_with_walls(self, x, y, width, height):
        """Check if a position collides with any walls"""
        # Create a rect for the position
        position_rect = pygame.Rect(x, y, width, height)
        
        # Check collision with each wall
        for wall in self.walls:
            wall_rect = pygame.Rect(
                wall["x"], wall["y"], 
                wall["width"], wall["height"]
            )
            
            # Add a small buffer around walls for safer spawning
            wall_rect_with_buffer = wall_rect.inflate(10, 10)
            
            if position_rect.colliderect(wall_rect_with_buffer):
                return True
        
        return False
    
    # The rest of the implementation is in game_mechanics.py and game_rendering.py
