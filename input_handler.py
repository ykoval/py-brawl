import pygame
import sys
import math
from game_engine import GameState, SCREEN_WIDTH, SCREEN_HEIGHT
import random

def handle_title_screen_input(self):
    """Handle input on the title screen"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.state = GameState.CHARACTER_SELECT
            elif event.key == pygame.K_F11:
                self.toggle_fullscreen()
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Get mouse position
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            # If in fullscreen mode, convert screen coordinates to game coordinates
            if self.is_fullscreen:
                mouse_x = (mouse_x - self.x_offset) / self.scale_factor
                mouse_y = (mouse_y - self.y_offset) / self.scale_factor
            
            # Check if Continue button was clicked
            if hasattr(self, 'continue_button_rect') and self.continue_button_rect.collidepoint(mouse_x, mouse_y):
                self.state = GameState.CHARACTER_SELECT
            
            # Check if Exit button was clicked
            elif hasattr(self, 'exit_button_rect') and self.exit_button_rect.collidepoint(mouse_x, mouse_y):
                pygame.quit()
                sys.exit()
                
            # Check if Fullscreen button was clicked
            elif hasattr(self, 'fullscreen_button_rect') and self.fullscreen_button_rect.collidepoint(mouse_x, mouse_y):
                self.toggle_fullscreen()

def handle_character_select_input(self):
    """Handle input on the character selection screen"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                self.toggle_fullscreen()
            elif event.key == pygame.K_ESCAPE:
                self.state = GameState.TITLE
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Get mouse position in screen coordinates
            mouse_pos = pygame.mouse.get_pos()
            
            # Check if player clicked on a brawler card
            if hasattr(self, 'brawler_cards'):
                for i, card_rect in enumerate(self.brawler_cards):
                    if card_rect and card_rect.collidepoint(mouse_pos):
                        # Define the brawlers for character selection
                        brawlers = ["Shelly", "Colt", "El Primo"]
                        
                        # Select the brawler corresponding to the clicked card
                        if i < len(brawlers):
                            self.reset_game(brawlers[i])
                            break

def handle_gameplay_input(self):
    """Handle input during gameplay"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.state = GameState.TITLE
            elif event.key == pygame.K_F11:
                self.toggle_fullscreen()
    
    # Get current key states
    keys = pygame.key.get_pressed()
    
    # Move player based on arrow keys and WASD
    dx, dy = 0, 0
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        dy -= self.player["speed"]
        self.player["direction"] = 270
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        dy += self.player["speed"]
        self.player["direction"] = 90
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        dx -= self.player["speed"]
        self.player["direction"] = 180
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        dx += self.player["speed"]
        self.player["direction"] = 0
        
    # Diagonal movement - adjust direction and normalize speed
    if dx != 0 and dy != 0:
        if dx > 0 and dy < 0:
            self.player["direction"] = 315
        elif dx > 0 and dy > 0:
            self.player["direction"] = 45
        elif dx < 0 and dy > 0:
            self.player["direction"] = 135
        elif dx < 0 and dy < 0:
            self.player["direction"] = 225
            
        # Normalize diagonal movement
        magnitude = math.sqrt(dx**2 + dy**2)
        dx = dx / magnitude * self.player["speed"]
        dy = dy / magnitude * self.player["speed"]
    
    # Update player position and check for wall collisions
    new_x = self.player["x"] + dx
    new_y = self.player["y"] + dy
    
    # Check for wall collisions
    player_rect = pygame.Rect(
        new_x, new_y, 
        self.player["width"], self.player["height"]
    )
    
    wall_collision = False
    for wall in self.walls:
        wall_rect = pygame.Rect(
            wall["x"], wall["y"], 
            wall["width"], wall["height"]
        )
        if player_rect.colliderect(wall_rect):
            wall_collision = True
            break
    
    if not wall_collision:
        self.player["x"] = new_x
        self.player["y"] = new_y
    
    # Initialize series shooting variables if they don't exist
    if "burst_count" not in self.player:
        self.player["burst_count"] = 0
        self.player["burst_delay"] = 0
        self.player["burst_max"] = 3  # Number of bullets in a burst
        self.player["burst_interval"] = 100  # Milliseconds between shots in burst
    
    # Handle shooting with spacebar or enter
    current_time = pygame.time.get_ticks()
    
    # Process any active shooting burst
    if self.player["burst_count"] > 0 and current_time >= self.player["burst_delay"]:
        # Fire the next shot in the series
        self.player["burst_count"] -= 1
        self.player["burst_delay"] = current_time + self.player["burst_interval"]
        
        # Calculate bullet starting position
        angle_rad = math.radians(self.player["direction"])
        bullet_x = self.player["x"] + self.player["width"] / 2 + math.cos(angle_rad) * 30
        bullet_y = self.player["y"] + self.player["height"] / 2 + math.sin(angle_rad) * 30
        
        # Add a small spread for shotgun-like effect
        spread = 10  # Degree of spread
        spread_angle = self.player["direction"] + random.uniform(-spread, spread)
        
        # Play shooting sound
        self.play_sound("shoot")
        
        # Create the bullet
        self.create_bullet(
            bullet_x, bullet_y, 
            spread_angle,  # Use spread angle for more realism 
            self.player["damage"], 
            True, 
            self.player["color"]
        )
    
    # Start a new burst when spacebar or enter is pressed
    if keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:
        time_since_last_attack = current_time - self.player["last_attack_time"]
        
        # Check if enough time has passed for another attack series
        if time_since_last_attack > 1000 / self.player["attack_speed"] and self.player["burst_count"] == 0:
            self.player["last_attack_time"] = current_time
            
            # Start a new burst
            self.player["burst_count"] = self.player["burst_max"]
            self.player["burst_delay"] = current_time
            
            # Immediate first shot
            angle_rad = math.radians(self.player["direction"])
            bullet_x = self.player["x"] + self.player["width"] / 2 + math.cos(angle_rad) * 30
            bullet_y = self.player["y"] + self.player["height"] / 2 + math.sin(angle_rad) * 30
            
            # Add a small spread
            spread = 10
            spread_angle = self.player["direction"] + random.uniform(-spread, spread)
            
            # Play shooting sound
            self.play_sound("shoot")
            
            # Create the first bullet
            self.create_bullet(
                bullet_x, bullet_y, 
                spread_angle,
                self.player["damage"], 
                True, 
                self.player["color"]
            )
            
            # Decrease remaining burst count and set delay for next shot
            self.player["burst_count"] -= 1
            self.player["burst_delay"] = current_time + self.player["burst_interval"]

def handle_game_over_input(self):
    """Handle input on the game over screen"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.state = GameState.TITLE
            elif event.key == pygame.K_F11:
                self.toggle_fullscreen()

def handle_win_screen_input(self):
    """Handle input on the win screen"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Return to title screen
                self.state = GameState.TITLE
            elif event.key == pygame.K_RETURN:
                # Start a new game with the same brawler
                self.reset_game(self.selected_brawler)
            elif event.key == pygame.K_F11:
                self.toggle_fullscreen()

# Add these methods to the PyBrawl class
def patch_pybrawl_input():
    """Patch the PyBrawl class with these input handler functions"""
    from game_engine import PyBrawl
    
    PyBrawl.handle_title_screen_input = handle_title_screen_input
    PyBrawl.handle_character_select_input = handle_character_select_input
    PyBrawl.handle_gameplay_input = handle_gameplay_input
    PyBrawl.handle_game_over_input = handle_game_over_input
    PyBrawl.handle_win_screen_input = handle_win_screen_input
