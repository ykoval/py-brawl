import pygame
import random
import math
from game_engine import GameState, SCREEN_WIDTH, SCREEN_HEIGHT, PyBrawl
from sprites import SpriteManager
import os

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BROWN = (165, 42, 42)
DARK_BLUE = (25, 25, 112)

def draw_title_screen(self):
    """Draw the title screen"""
    # Background
    if self.is_fullscreen:
        # In fullscreen mode, fill the entire screen first with black
        self.screen.fill((0, 0, 0))
    else:
        # In windowed mode, just fill the screen
        self.screen.fill(BLACK)
    
    # Load and display title image as full screen background
    title_path = os.path.join("assets", "title.png")
    if os.path.exists(title_path):
        try:
            title_image = pygame.image.load(title_path).convert_alpha()
            
            # Calculate dimensions to cover the entire screen/game area
            if self.is_fullscreen:
                # In fullscreen, cover the game area
                scaled_width = int(self.original_width * self.scale_factor)
                scaled_height = int(self.original_height * self.scale_factor)
                target_width = scaled_width
                target_height = scaled_height
                target_x = self.x_offset
                target_y = self.y_offset
            else:
                # In windowed mode, cover the entire window
                target_width = SCREEN_WIDTH
                target_height = SCREEN_HEIGHT
                target_x = 0
                target_y = 0
            
            # Scale the image to cover the entire screen/game area
            title_image = pygame.transform.scale(title_image, (target_width, target_height))
            
            # Draw the title image as background
            self.screen.blit(title_image, (target_x, target_y))
            
            # Add a semi-transparent overlay for better text readability
            overlay = pygame.Surface((target_width, target_height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))  # Black with 50% transparency
            self.screen.blit(overlay, (target_x, target_y))
            
        except Exception as e:
            print(f"Error loading title image: {e}")
    
    # Subtitle - position it at the bottom
    self.draw_outlined_text("A Simple Brawl Stars Inspired Game", self.menu_font, WHITE, 
                  SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80, outline_color=BLACK, outline_width=1)
    
    # Draw a pulsating effect at the bottom
    alpha = int(128 + 127 * math.sin(pygame.time.get_ticks() / 500))
    self.draw_outlined_text("Created while learning Python", self.menu_font, (255, 255, alpha), 
                  SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40, outline_color=BLACK, outline_width=1)
    
    # Draw grouped menu buttons
    button_width = 300  # Increased from 250 to fit text better
    button_height = 50
    menu_center_x = SCREEN_WIDTH // 2
    menu_start_y = SCREEN_HEIGHT // 2 + 50
    button_spacing = 20
    
    # Button background colors
    button_color = (50, 50, 50, 200)  # Semi-transparent
    button_hover_color = (100, 100, 100, 200)  # Semi-transparent hover
    text_color = WHITE
    
    # Get mouse position for hover effects
    mouse_x, mouse_y = pygame.mouse.get_pos()
    
    # Adjust mouse position if in fullscreen
    if self.is_fullscreen:
        # Convert screen coordinates to game coordinates
        mouse_x = (mouse_x - self.x_offset) / self.scale_factor
        mouse_y = (mouse_y - self.y_offset) / self.scale_factor
    
    # Continue button
    self.continue_button_rect = pygame.Rect(
        menu_center_x - button_width // 2,
        menu_start_y,
        button_width,
        button_height
    )
    
    # Exit button
    self.exit_button_rect = pygame.Rect(
        menu_center_x - button_width // 2,
        menu_start_y + button_height + button_spacing,
        button_width,
        button_height
    )
    
    # Check for button hover (for visual feedback)
    continue_hovered = self.continue_button_rect.collidepoint(mouse_x, mouse_y)
    exit_hovered = self.exit_button_rect.collidepoint(mouse_x, mouse_y)
    
    # Draw button backgrounds with hover effect
    pygame.draw.rect(self.screen, button_hover_color if continue_hovered else button_color, 
                    self.continue_button_rect, border_radius=10)
    pygame.draw.rect(self.screen, button_hover_color if exit_hovered else button_color, 
                    self.exit_button_rect, border_radius=10)
    
    # Draw button borders
    pygame.draw.rect(self.screen, WHITE, self.continue_button_rect, 2, border_radius=10)
    pygame.draw.rect(self.screen, WHITE, self.exit_button_rect, 2, border_radius=10)
    
    # Draw button text (without keyboard shortcuts)
    self.draw_outlined_text("Continue", self.menu_font, text_color, 
                  menu_center_x, self.continue_button_rect.centery, outline_color=BLACK, outline_width=1)
    self.draw_outlined_text("Exit", self.menu_font, text_color, 
                  menu_center_x, self.exit_button_rect.centery, outline_color=BLACK, outline_width=1)
    
    # Create small hint font for keyboard shortcuts
    hint_font = pygame.font.SysFont("Arial", 12)
    
    # Add small keyboard shortcut hints below each button
    continue_hint_y = self.continue_button_rect.bottom + 5
    exit_hint_y = self.exit_button_rect.bottom + 5
    
    self.draw_outlined_text("SPACE", hint_font, WHITE, 
                           menu_center_x, continue_hint_y, 
                           outline_color=BLACK, outline_width=1)
    self.draw_outlined_text("ESC", hint_font, WHITE, 
                           menu_center_x, exit_hint_y, 
                           outline_color=BLACK, outline_width=1)
    
    # Draw fullscreen toggle button in top-right corner
    fs_button_size = 40
    fs_button_margin = 20
    fs_button_x = SCREEN_WIDTH - fs_button_size - fs_button_margin
    fs_button_y = fs_button_margin
    
    # Create a more native-looking window button
    self.fullscreen_button_rect = pygame.Rect(
        fs_button_x, fs_button_y, fs_button_size, fs_button_size
    )
    
    # If in fullscreen mode, adjust the position
    if self.is_fullscreen:
        # Calculate scaled position
        scaled_fs_button_x = int(fs_button_x * self.scale_factor + self.x_offset)
        scaled_fs_button_y = int(fs_button_y * self.scale_factor + self.y_offset)
        scaled_fs_button_size = int(fs_button_size * self.scale_factor)
        
        # Update the button rect with scaled coordinates
        self.fullscreen_button_rect = pygame.Rect(
            scaled_fs_button_x, scaled_fs_button_y, 
            scaled_fs_button_size, scaled_fs_button_size
        )
    
    # Check if fullscreen button is hovered
    fs_button_hovered = self.fullscreen_button_rect.collidepoint(mouse_x, mouse_y)
    
    # Button colors
    fs_button_color = (60, 60, 60, 200)  # Base color with transparency
    fs_button_hover_color = (100, 100, 100, 220)  # Hover color
    
    # Draw the button background
    pygame.draw.rect(self.screen, 
                    fs_button_hover_color if fs_button_hovered else fs_button_color, 
                    self.fullscreen_button_rect, border_radius=5)
    
    # Draw button border
    pygame.draw.rect(self.screen, WHITE, self.fullscreen_button_rect, 2, border_radius=5)
    
    # Draw fullscreen/windowed icon
    icon_margin = 8
    icon_rect = pygame.Rect(
        self.fullscreen_button_rect.x + icon_margin,
        self.fullscreen_button_rect.y + icon_margin,
        self.fullscreen_button_rect.width - 2 * icon_margin,
        self.fullscreen_button_rect.height - 2 * icon_margin
    )
    
    # Draw appropriate icon based on current fullscreen state
    if self.is_fullscreen:
        # Windowed mode icon (smaller square)
        pygame.draw.rect(self.screen, WHITE, icon_rect, 2)
    else:
        # Fullscreen icon (corners of a square)
        corner_length = 6
        
        # Top-left corner
        pygame.draw.line(self.screen, WHITE, 
                        (icon_rect.left, icon_rect.top), 
                        (icon_rect.left + corner_length, icon_rect.top), 2)
        pygame.draw.line(self.screen, WHITE, 
                        (icon_rect.left, icon_rect.top), 
                        (icon_rect.left, icon_rect.top + corner_length), 2)
        
        # Top-right corner
        pygame.draw.line(self.screen, WHITE, 
                        (icon_rect.right, icon_rect.top), 
                        (icon_rect.right - corner_length, icon_rect.top), 2)
        pygame.draw.line(self.screen, WHITE, 
                        (icon_rect.right, icon_rect.top), 
                        (icon_rect.right, icon_rect.top + corner_length), 2)
        
        # Bottom-left corner
        pygame.draw.line(self.screen, WHITE, 
                        (icon_rect.left, icon_rect.bottom), 
                        (icon_rect.left + corner_length, icon_rect.bottom), 2)
        pygame.draw.line(self.screen, WHITE, 
                        (icon_rect.left, icon_rect.bottom), 
                        (icon_rect.left, icon_rect.bottom - corner_length), 2)
        
        # Bottom-right corner
        pygame.draw.line(self.screen, WHITE, 
                        (icon_rect.right, icon_rect.bottom), 
                        (icon_rect.right - corner_length, icon_rect.bottom), 2)
        pygame.draw.line(self.screen, WHITE, 
                        (icon_rect.right, icon_rect.bottom), 
                        (icon_rect.right, icon_rect.bottom - corner_length), 2)
    
    # Add small "F11" hint text below
    hint_font = pygame.font.SysFont("Arial", 12)
    hint_y = self.fullscreen_button_rect.bottom + 5
    self.draw_outlined_text("F11", hint_font, WHITE, 
                           self.fullscreen_button_rect.centerx, hint_y, 
                           outline_color=BLACK, outline_width=1)

def draw_character_select(self):
    """Draw the character selection screen"""
    # Background
    if self.is_fullscreen:
        # In fullscreen mode, fill the entire screen first with black
        self.screen.fill((0, 0, 0))
        
        # Calculate the scaled size for the game area
        scaled_width = int(self.original_width * self.scale_factor)
        scaled_height = int(self.original_height * self.scale_factor)
        
        # Draw the black background only in the game area
        char_select_bg = pygame.Surface((scaled_width, scaled_height))
        char_select_bg.fill(BLACK)
        self.screen.blit(char_select_bg, (self.x_offset, self.y_offset))
    else:
        # In windowed mode, just fill the screen
        self.screen.fill(BLACK)
    
    # Title
    self.draw_text("SELECT BRAWLER", self.title_font, WHITE, SCREEN_WIDTH // 2, 100)
    
    # Draw brawler cards
    card_width = 150
    card_height = 200
    card_spacing = 30
    
    # Updated to include 3 brawlers instead of 4
    total_width = (card_width * 3) + (card_spacing * 2)
    start_x = (SCREEN_WIDTH - total_width) // 2
    
    brawlers = [
        {
            "name": "Shelly",
            "health": 100,
            "damage": 20,
            "sprite": "shelly",
            "description": "Balanced brawler with shotgun attack"
        },
        {
            "name": "Colt",
            "health": 80,
            "damage": 15,
            "sprite": "colt",
            "description": "Fast shooter with long range"
        },
        {
            "name": "El Primo",
            "health": 150,
            "damage": 30,
            "sprite": "el_primo",
            "description": "Tank with powerful close-range attacks"
        }
    ]
    
    for i, brawler in enumerate(brawlers):
        brawler_name = brawler["name"]
        
        # Calculate card position
        card_x = start_x + (i * (card_width + card_spacing))
        card_y = SCREEN_HEIGHT // 2 - 50
        
        # Convert card position to screen coordinates for detection
        if self.is_fullscreen:
            screen_card_x = int(card_x * self.scale_factor + self.x_offset)
            screen_card_y = int(card_y * self.scale_factor + self.y_offset)
            screen_card_width = int(card_width * self.scale_factor)
            screen_card_height = int(card_height * self.scale_factor)
        else:
            screen_card_x = card_x
            screen_card_y = card_y
            screen_card_width = card_width
            screen_card_height = card_height
        
        # Store card rect for click detection
        if not hasattr(self, 'brawler_cards'):
            self.brawler_cards = []
            
        # Extend the list if needed
        while len(self.brawler_cards) <= i:
            self.brawler_cards.append(None)
            
        # Update the brawler card rect
        self.brawler_cards[i] = pygame.Rect(screen_card_x, screen_card_y, screen_card_width, screen_card_height)
        
        # Draw card background
        card_rect = self.scale_position(pygame.Rect(card_x, card_y, card_width, card_height))
        pygame.draw.rect(self.screen, DARK_BLUE, card_rect)
        pygame.draw.rect(self.screen, WHITE, card_rect, 2)  # White border
        
        # Draw brawler image
        portrait_size = 110
        portrait_x = card_x + (card_width - portrait_size) // 2
        portrait_y = card_y + 15
        
        portrait_rect = self.scale_position(pygame.Rect(portrait_x, portrait_y, portrait_size, portrait_size))
        
        # Try to use sprite for brawler portrait
        has_sprite = False
        if hasattr(self, 'sprite_manager') and "sprite" in brawler:
            sprite_name = brawler["sprite"]
            if hasattr(self.sprite_manager, 'sprites') and sprite_name in self.sprite_manager.sprites:
                portrait = self.sprite_manager.get_scaled_sprite(sprite_name, portrait_rect.width, portrait_rect.height)
                self.screen.blit(portrait, portrait_rect)
                has_sprite = True
        
        # Fallback if sprite not available
        if not has_sprite:
            # Create a placeholder colored rectangle
            color = BLUE
            if brawler_name == "Colt":
                color = RED
            elif brawler_name == "El Primo":
                color = GREEN
                
            pygame.draw.rect(self.screen, color, portrait_rect)
            pygame.draw.rect(self.screen, WHITE, portrait_rect, 1)  # White border
            
            # Draw a question mark
            question_text = self.title_font.render("?", True, WHITE)
            question_rect = question_text.get_rect(center=portrait_rect.center)
            self.screen.blit(question_text, question_rect)
        
        # Draw stats - adjust positioning and use smaller font
        stats_font = pygame.font.SysFont("Arial", 16)  # Smaller font for stats
        
        # Draw HP stat
        self.draw_text(f"HP: {brawler['health']}", stats_font, WHITE, 
                     card_x + card_width // 2, card_y + 160, True)
        
        # Draw DMG stat
        self.draw_text(f"DMG: {brawler['damage']}", stats_font, WHITE, 
                     card_x + card_width // 2, card_y + 180, True)
    
    # Draw instruction
    self.draw_text("Click on a brawler to start", self.menu_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80)

def draw_gameplay(self):
    """Draw the gameplay screen"""
    if self.is_fullscreen:
        # In fullscreen mode, fill the entire screen first with black
        self.screen.fill((0, 0, 0))
        
        # Calculate the scaled size for the game area
        scaled_width = int(self.original_width * self.scale_factor)
        scaled_height = int(self.original_height * self.scale_factor)
        
        # Create a surface for the gameplay area
        gameplay_bg = pygame.Surface((scaled_width, scaled_height))
        
        # Fill with ground tiles if sprite manager is available
        if hasattr(self, 'sprite_manager') and 'ground' in self.sprite_manager.sprites:
            # Calculate how many tiles we need to fill the screen
            tile_size = 40  # Size of each tile when drawn
            tile_size_scaled = int(tile_size * self.scale_factor)
            tiles_x = (scaled_width + tile_size_scaled - 1) // tile_size_scaled
            tiles_y = (scaled_height + tile_size_scaled - 1) // tile_size_scaled
            
            # Fill the background with ground tiles
            for x in range(tiles_x):
                for y in range(tiles_y):
                    ground_tile = self.sprite_manager.get_tile_sprite(
                        'ground', tile_size_scaled, tile_size_scaled
                    )
                    gameplay_bg.blit(ground_tile, (x * tile_size_scaled, y * tile_size_scaled))
        else:
            # Fallback to solid color if sprite not available
            gameplay_bg.fill(BROWN)  # Brown background for the gameplay area
            
        self.screen.blit(gameplay_bg, (self.x_offset, self.y_offset))
    else:
        # In windowed mode, fill the screen with ground tiles
        if hasattr(self, 'sprite_manager') and 'ground' in self.sprite_manager.sprites:
            # Clear the screen first
            self.screen.fill((0, 0, 0))
            
            # Calculate how many tiles we need to fill the screen
            tile_size = 40  # Size of each tile when drawn
            tiles_x = (SCREEN_WIDTH + tile_size - 1) // tile_size
            tiles_y = (SCREEN_HEIGHT + tile_size - 1) // tile_size
            
            # Fill the background with ground tiles
            for x in range(tiles_x):
                for y in range(tiles_y):
                    ground_tile = self.sprite_manager.get_tile_sprite(
                        'ground', tile_size, tile_size
                    )
                    self.screen.blit(ground_tile, (x * tile_size, y * tile_size))
        else:
            # Fallback to solid color if sprite not available
            self.screen.fill(BROWN)  # Brown background for the gameplay area
    
    # Draw map elements
    self.draw_map()
    
    # Draw bullets
    for bullet in self.bullets:
        # Draw a colored circle for bullets
        pygame.draw.circle(
            self.screen, 
            bullet["color"] if "color" in bullet else (255, 255, 255), 
            self.scale_position(bullet["x"], bullet["y"]),
            int(bullet["radius"] * self.scale_factor) if "radius" in bullet else 5
        )
    
    # Draw player
    player_rect = self.scale_position(
        pygame.Rect(self.player["x"], self.player["y"], self.player["width"], self.player["height"])
    )
    
    # Draw player with sprite if available
    player_sprite_drawn = False
    if hasattr(self, 'sprite_manager') and hasattr(self, 'selected_brawler') and self.selected_brawler:
        sprite_key = self.selected_brawler.lower().replace(" ", "_")
        if hasattr(self.sprite_manager, 'sprites') and sprite_key in self.sprite_manager.sprites:
            player_sprite = self.sprite_manager.get_scaled_sprite(
                sprite_key, player_rect.width, player_rect.height
            )
            self.screen.blit(player_sprite, player_rect)
            player_sprite_drawn = True
    
    # If no sprite available, fallback to a colored square
    if not player_sprite_drawn:
        pygame.draw.rect(self.screen, self.player["color"], player_rect)
        pygame.draw.rect(self.screen, WHITE, player_rect, 2)  # White border
    
    # Draw health bar above player
    player_health_percentage = self.player["health"] / self.player["max_health"]
    health_bar_width = int(self.player["width"] * 1.5)  # Make health bar wider than player
    health_bar_height = 5  # Slim health bar
    
    # Background of health bar (dark red background)
    pygame.draw.rect(
        self.screen,
        (100, 0, 0),  # Dark red
        pygame.Rect(
            player_rect.x - (health_bar_width - player_rect.width) // 2,  # Center above player
            player_rect.y - health_bar_height - 2,  # Just above player
            health_bar_width,
            health_bar_height
        )
    )
    
    # Foreground of health bar (green for remaining health)
    pygame.draw.rect(
        self.screen,
        (0, 200, 0),  # Green
        pygame.Rect(
            player_rect.x - (health_bar_width - player_rect.width) // 2,
            player_rect.y - health_bar_height - 2,
            int(health_bar_width * player_health_percentage),
            health_bar_height
        )
    )
    
    # Draw ammo reload indicator below health bar
    current_time = pygame.time.get_ticks()
    ammo_bar_width = int(health_bar_width / 3) - 2  # Width of each ammo segment, slightly narrower
    ammo_bar_height = 4  # Thinner than health bar
    ammo_bar_spacing = 2  # Space between ammo segments
    ammo_bar_y = player_rect.y - health_bar_height - ammo_bar_height - 4  # Position above health bar
    ammo_bar_x_start = player_rect.x - (health_bar_width - player_rect.width) // 2  # Align with health bar
    
    # Get player's burst info and attack cooldown
    burst_max = self.player.get("burst_max", 3)
    burst_count = self.player.get("burst_count", 0)
    attack_cooldown = 1000 / self.player.get("attack_speed", 1.0)  # Milliseconds between attacks
    time_since_attack = current_time - self.player.get("last_attack_time", 0)
    reload_progress = min(1.0, time_since_attack / attack_cooldown)
    
    # Calculate how many complete ammo are ready and the progress of the next one
    if burst_count == 0:
        # If all shots depleted, calculate recharge for all three shots
        complete_ammo = int(reload_progress * burst_max)
        next_ammo_progress = reload_progress * burst_max - complete_ammo
    else:
        # If we still have shots left, they're already complete
        complete_ammo = burst_count
        next_ammo_progress = 0
        
        # If we're reloading to full capacity
        if burst_count < burst_max and reload_progress >= 1.0:
            complete_ammo += 1
            next_ammo_progress = 0
        elif burst_count < burst_max:
            next_ammo_progress = reload_progress
    
    # Draw each ammo segment (from right to left)
    for i in range(burst_max):
        # Calculate position, starting from right to left
        index_from_right = burst_max - i - 1
        ammo_x = ammo_bar_x_start + index_from_right * (ammo_bar_width + ammo_bar_spacing)
        
        # Background of ammo bar (dark gray)
        pygame.draw.rect(
            self.screen,
            (50, 50, 50),  # Dark gray
            pygame.Rect(
                ammo_x,
                ammo_bar_y,
                ammo_bar_width,
                ammo_bar_height
            )
        )
        
        # Determine ammo status based on position
        if index_from_right < complete_ammo:
            # Fully charged ammo - yellow
            ammo_fill_width = ammo_bar_width
            ammo_color = (200, 200, 50)  # Yellow
        elif index_from_right == complete_ammo and next_ammo_progress > 0:
            # Currently charging ammo - blue with progress
            ammo_fill_width = int(ammo_bar_width * next_ammo_progress)
            ammo_color = (50, 150, 255)  # Blue for reloading
        else:
            # Empty ammo - no fill
            ammo_fill_width = 0
            ammo_color = None
        
        # Draw filled portion of ammo bar
        if ammo_fill_width > 0:
            pygame.draw.rect(
                self.screen,
                ammo_color,
                pygame.Rect(
                    ammo_x,
                    ammo_bar_y,
                    ammo_fill_width,
                    ammo_bar_height
                )
            )
    
    # Draw player aim direction line
    if "direction" in self.player:
        angle_rad = math.radians(self.player["direction"])
        start_x = self.player["x"] + self.player["width"] / 2
        start_y = self.player["y"] + self.player["height"] / 2
        end_x = start_x + math.cos(angle_rad) * 30
        end_y = start_y + math.sin(angle_rad) * 30
        
        pygame.draw.line(
            self.screen,
            (255, 255, 255),  # White line for player
            self.scale_position(start_x, start_y),
            self.scale_position(end_x, end_y),
            3
        )
    
    # Draw enemies
    self.draw_enemies()
    
    # Draw player health bar and number
    player_health_percent = self.player["health"] / self.player["max_health"]
    player_health_bar_width = 200
    player_health_bar_height = 20
    player_health_bar_x = 120  # Moved to center better
    player_health_bar_y = 20  # Moved up further
    
    # Background of health bar (red)
    health_bar_bg_rect = pygame.Rect(
        player_health_bar_x - player_health_bar_width // 2, 
        player_health_bar_y - player_health_bar_height // 2,
        player_health_bar_width, 
        player_health_bar_height
    )
    health_bar_bg_rect = self.scale_position(health_bar_bg_rect)
    pygame.draw.rect(self.screen, RED, health_bar_bg_rect)
    
    # Foreground of health bar (green for remaining health)
    health_bar_fg_width = int(player_health_bar_width * player_health_percent)
    health_bar_fg_rect = pygame.Rect(
        player_health_bar_x - player_health_bar_width // 2, 
        player_health_bar_y - player_health_bar_height // 2,
        health_bar_fg_width, 
        player_health_bar_height
    )
    health_bar_fg_rect = self.scale_position(health_bar_fg_rect)
    pygame.draw.rect(self.screen, GREEN, health_bar_fg_rect)
    
    # Border for health bar
    pygame.draw.rect(self.screen, WHITE, health_bar_bg_rect, 2)
    
    # Health number
    health_text = f"{self.player['health']}/{self.player['max_health']}"
    self.draw_outlined_text(
        health_text, 
        self.info_font, 
        WHITE, 
        player_health_bar_x, 
        player_health_bar_y, 
        outline_color=BLACK,
        outline_width=1,
        centered=True
    )
    
    # Combine wave and enemies information in a single line with outlined text
    wave_enemies_text = f"Wave: {self.current_wave}/{self.max_waves} | Enemies: {len([e for e in self.enemies if e['health'] > 0])}/{len(self.enemies)}"
    self.draw_outlined_text(
        wave_enemies_text, 
        self.info_font, 
        WHITE, 
        SCREEN_WIDTH - 150, 
        20,  # Moved up
        outline_color=BLACK,
        outline_width=1
    )
    
    # Draw game controller info with outlined text
    controls_text = "Arrow Keys: Move | Spacebar: Shoot | ESC: Menu"
    self.draw_outlined_text(
        controls_text, 
        self.info_font, 
        WHITE, 
        SCREEN_WIDTH // 2, 
        SCREEN_HEIGHT - 20,
        outline_color=BLACK,
        outline_width=1
    )
    
    # Draw kill notifications
    self.draw_kill_notifications()

def draw_map(self):
    """Draw the game map with walls and bushes"""
    # Use existing map elements (walls and bushes) from the game engine
    
    # Draw walls
    for wall in self.walls:
        wall_rect = self.scale_position(
            pygame.Rect(wall["x"], wall["y"], wall["width"], wall["height"])
        )
        
        # Draw wall with sprite if available
        if hasattr(self, 'sprite_manager'):
            wall_sprite = self.sprite_manager.get_tile_sprite(
                'wall', wall_rect.width, wall_rect.height
            )
            self.screen.blit(wall_sprite, wall_rect)
        else:
            # Fallback to colored rectangle
            pygame.draw.rect(self.screen, BLUE, wall_rect)
    
    # Draw bushes
    for bush in self.bushes:
        bush_rect = self.scale_position(
            pygame.Rect(bush["x"], bush["y"], bush["width"], bush["height"])
        )
        
        # Draw bush with sprite if available
        if hasattr(self, 'sprite_manager'):
            grass_sprite = self.sprite_manager.get_tile_sprite(
                'grass', bush_rect.width, bush_rect.height
            )
            self.screen.blit(grass_sprite, bush_rect)
        else:
            # Fallback to colored rectangle
            pygame.draw.rect(self.screen, GREEN, bush_rect)

def draw_game_over(self):
    """Draw the game over screen"""
    # Fill background with black first
    if self.is_fullscreen:
        # In fullscreen mode, fill the entire screen first
        self.screen.fill((0, 0, 0))  # Black background
    else:
        # In windowed mode, just fill the screen
        self.screen.fill((0, 0, 0))
    
    # Load and display lose image as background
    lose_path = os.path.join("assets", "lose.png")
    if os.path.exists(lose_path):
        try:
            lose_image = pygame.image.load(lose_path).convert_alpha()
            
            # Calculate dimensions to cover the entire screen/game area
            if self.is_fullscreen:
                # In fullscreen, cover the game area
                scaled_width = int(self.original_width * self.scale_factor)
                scaled_height = int(self.original_height * self.scale_factor)
                target_width = scaled_width
                target_height = scaled_height
                target_x = self.x_offset
                target_y = self.y_offset
            else:
                # In windowed mode, cover the entire window
                target_width = SCREEN_WIDTH
                target_height = SCREEN_HEIGHT
                target_x = 0
                target_y = 0
            
            # Scale the image to cover the entire screen/game area
            lose_image = pygame.transform.scale(lose_image, (target_width, target_height))
            
            # Draw the lose image as background
            self.screen.blit(lose_image, (target_x, target_y))
            
            # Add a semi-transparent overlay for better text readability
            overlay = pygame.Surface((target_width, target_height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))  # Semi-transparent black (more transparent than before)
            self.screen.blit(overlay, (target_x, target_y))
            
        except Exception as e:
            print(f"Error loading lose image: {e}")
            # Fallback to original semi-transparent overlay if image fails to load
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))  # Black with alpha
            self.screen.blit(overlay, (0, 0))
    else:
        # Fallback to original semi-transparent overlay if image doesn't exist
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))  # Black with alpha
        self.screen.blit(overlay, (0, 0))
    
    # Score text - positioned higher now that we removed the GAME OVER text
    self.draw_outlined_text(f"Final Score: {self.score}", self.menu_font, WHITE, 
                           SCREEN_WIDTH // 2, SCREEN_HEIGHT * 2 // 5,
                           outline_color=BLACK, outline_width=1)
    
    # Restart instructions
    self.draw_outlined_text("Press ENTER to return to title", self.menu_font, WHITE, 
                           SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40,
                           outline_color=BLACK, outline_width=1)

def draw_win_screen(self):
    """Draw the win screen when player completes all waves"""
    # Fill background with black first
    if self.is_fullscreen:
        # In fullscreen mode, fill the entire screen first
        self.screen.fill((0, 0, 0))  # Black background
    else:
        # In windowed mode, just fill the screen
        self.screen.fill((0, 0, 0))
    
    # Load and display win image as background
    win_path = os.path.join("assets", "win.png")
    if os.path.exists(win_path):
        try:
            win_image = pygame.image.load(win_path).convert_alpha()
            
            # Calculate dimensions to cover the entire screen/game area
            if self.is_fullscreen:
                # In fullscreen, cover the game area
                scaled_width = int(self.original_width * self.scale_factor)
                scaled_height = int(self.original_height * self.scale_factor)
                target_width = scaled_width
                target_height = scaled_height
                target_x = self.x_offset
                target_y = self.y_offset
            else:
                # In windowed mode, cover the entire window
                target_width = SCREEN_WIDTH
                target_height = SCREEN_HEIGHT
                target_x = 0
                target_y = 0
            
            # Scale the image to cover the entire screen/game area
            win_image = pygame.transform.scale(win_image, (target_width, target_height))
            
            # Draw the win image as background
            self.screen.blit(win_image, (target_x, target_y))
            
            # Add a semi-transparent overlay for better text readability
            overlay = pygame.Surface((target_width, target_height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 100))  # Semi-transparent black
            self.screen.blit(overlay, (target_x, target_y))
            
        except Exception as e:
            print(f"Error loading win image: {e}")
            # Fallback to solid color if image fails to load
            if self.is_fullscreen:
                # Draw the green background only in the game area
                scaled_width = int(self.original_width * self.scale_factor)
                scaled_height = int(self.original_height * self.scale_factor)
                victory_bg = pygame.Surface((scaled_width, scaled_height))
                victory_bg.fill((25, 100, 25))  # Dark green
                self.screen.blit(victory_bg, (self.x_offset, self.y_offset))
            else:
                # In windowed mode, just fill the screen
                self.screen.fill((25, 100, 25))  # Dark green
    else:
        # Fallback to solid color if image doesn't exist
        if self.is_fullscreen:
            # Draw the green background only in the game area
            scaled_width = int(self.original_width * self.scale_factor)
            scaled_height = int(self.original_height * self.scale_factor)
            victory_bg = pygame.Surface((scaled_width, scaled_height))
            victory_bg.fill((25, 100, 25))  # Dark green
            self.screen.blit(victory_bg, (self.x_offset, self.y_offset))
        else:
            # In windowed mode, just fill the screen
            self.screen.fill((25, 100, 25))  # Dark green
    
    # Draw congratulations message with outlined text for better visibility
    self.draw_outlined_text("VICTORY!", self.title_font, YELLOW, 
                           SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3,
                           outline_color=BLACK, outline_width=2)
    
    # Draw congratulatory message
    self.draw_outlined_text(f"You defeated all {self.max_waves} waves!", self.menu_font, WHITE, 
                           SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                           outline_color=BLACK, outline_width=1)
    
    # Draw score
    self.draw_outlined_text(f"Final Score: {self.score}", self.menu_font, WHITE, 
                           SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50,
                           outline_color=BLACK, outline_width=1)
    
    # Draw brawler used
    self.draw_outlined_text(f"Brawler: {self.selected_brawler}", self.menu_font, WHITE, 
                           SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100,
                           outline_color=BLACK, outline_width=1)
    
    # Draw play again instructions
    self.draw_outlined_text("Press ENTER to play again or ESC to exit", self.menu_font, WHITE, 
                           SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100,
                           outline_color=BLACK, outline_width=1)

def draw_kill_notifications(self):
    """Draw kill notifications on the screen"""
    # Only show if there are notifications
    if not hasattr(self, 'kill_notifications') or not self.kill_notifications:
        return
    
    current_time = pygame.time.get_ticks()
    notifications_to_remove = []
    
    # Draw each notification
    y_offset = 80  # Start below the wave counter
    
    for i, notification in enumerate(self.kill_notifications):
        # Check if the notification has expired
        if current_time - notification['time'] > 3000:  # 3 seconds
            notifications_to_remove.append(i)
            continue
        
        # Use grave sprite instead of emoji if available
        if hasattr(self, 'sprite_manager') and 'grave' in self.sprite_manager.sprites:
            # Get text dimensions to properly align grave icon with text
            text_surface = self.info_font.render(notification['name'], True, (255, 255, 255))
            text_width = text_surface.get_width()
            text_height = text_surface.get_height()
            
            # Position text aligned to right edge with margin
            text_x = SCREEN_WIDTH - 20
            
            # Calculate grave icon size to match text height (smaller)
            grave_size = (int(text_height * 0.9), int(text_height * 0.9))
            
            # Draw the text right-aligned with outline
            self.draw_outlined_text(
                notification['name'], 
                self.info_font, 
                (255, 255, 255), 
                text_x, 
                y_offset, 
                outline_color=BLACK,
                outline_width=1,
                centered=False, 
                align="right"
            )
            
            # Place grave icon before the text with proper spacing
            grave_x = text_x - text_width - grave_size[0] - 5  # Position icon before text with reduced spacing
            grave_y = y_offset - (grave_size[1] - text_height) / 2  # Center vertically with text
            
            # Get the scaled position
            grave_pos = (
                int(grave_x * self.scale_factor + self.x_offset),
                int(grave_y * self.scale_factor + self.y_offset)
            )
            
            # Use the sprite manager's dedicated method for getting a scaled grave sprite
            grave_sprite = self.sprite_manager.get_scaled_grave_sprite(
                int(grave_size[0] * self.scale_factor), 
                int(grave_size[1] * self.scale_factor)
            )
            
            # Draw the grave sprite
            self.screen.blit(grave_sprite, grave_pos)
        else:
            # Fallback to emoji if sprite manager not available
            # Position text aligned to right edge with margin
            text_x = SCREEN_WIDTH - 20
            
            # Draw right-aligned text with emoji and outline
            kill_text = f"💀 {notification['name']}"
            self.draw_outlined_text(
                kill_text, 
                self.info_font, 
                (255, 255, 255), 
                text_x, 
                y_offset, 
                outline_color=BLACK,
                outline_width=1,
                centered=False, 
                align="right"
            )
        
        # Increase y_offset for next notification
        y_offset += 25
    
    # Remove expired notifications
    for i in sorted(notifications_to_remove, reverse=True):
        self.kill_notifications.pop(i)

def draw_enemies(self):
    """Draw enemies and their health bars"""
    for enemy in self.enemies:
        # Scale enemy position for rendering
        enemy_rect = self.scale_position(
            pygame.Rect(enemy["x"], enemy["y"], enemy["width"], enemy["height"])
        )
        
        # Check if it's a boss
        is_boss = enemy.get("is_boss", False)
        
        # Draw enemy with sprite if available
        enemy_sprite_drawn = False
        if hasattr(self, 'sprite_manager'):
            # If the enemy is defeated, use the grave sprite
            if enemy["health"] <= 0:
                grave_sprite = self.sprite_manager.get_scaled_grave_sprite(
                    enemy_rect.width, enemy_rect.height
                )
                self.screen.blit(grave_sprite, enemy_rect)
                enemy_sprite_drawn = True
            else:
                # Use regular enemy sprite (randomly selected if not specified)
                if "portrait_index" not in enemy:
                    # Assign a random portrait index if not yet assigned
                    enemy["portrait_index"] = random.randint(0, 4)
                    
                enemy_sprite = self.sprite_manager.get_enemy_portrait(enemy["portrait_index"])
                enemy_sprite = pygame.transform.scale(enemy_sprite, (enemy_rect.width, enemy_rect.height))
                self.screen.blit(enemy_sprite, enemy_rect)
                enemy_sprite_drawn = True
        
        # If no sprite available, fallback to colored shapes
        if not enemy_sprite_drawn:
            # For dead enemies, make them semi-transparent
            if enemy["health"] <= 0:
                alpha = 100  # Semi-transparent
                # Create a transparent version of the color
                color = (*enemy["color"], alpha)
                
                # Create a transparent surface and draw the enemy
                s = pygame.Surface((enemy_rect.width, enemy_rect.height), pygame.SRCALPHA)
                pygame.draw.rect(s, color, (0, 0, enemy_rect.width, enemy_rect.height))
                
                # Draw on the game screen at the appropriate position
                self.screen.blit(s, enemy_rect)
            else:
                # Draw normal enemy
                pygame.draw.rect(self.screen, enemy["color"], enemy_rect)
                pygame.draw.rect(self.screen, (255, 255, 255), enemy_rect, 2)  # White border
            
            # If boss, draw a crown or indicator above it
            if is_boss:
                alpha = 100 if enemy["health"] <= 0 else 255
                crown_color = (255, 215, 0, alpha) if enemy["health"] <= 0 else (255, 215, 0)
                crown_points = [
                    (enemy_rect.centerx, enemy_rect.top - 10),
                    (enemy_rect.centerx - 10, enemy_rect.top - 5),
                    (enemy_rect.centerx - 5, enemy_rect.top - 15),
                    (enemy_rect.centerx, enemy_rect.top - 5),
                    (enemy_rect.centerx + 5, enemy_rect.top - 15),
                    (enemy_rect.centerx + 10, enemy_rect.top - 5)
                ]
                pygame.draw.polygon(self.screen, crown_color, crown_points)
        
        # If in debug mode, show collision boxes for bosses
        if is_boss and hasattr(self, 'debug_mode') and self.debug_mode:
            # Get collision dimensions and position
            col_x = enemy["x"] + enemy.get("collision_offset_x", 0)
            col_y = enemy["y"] + enemy.get("collision_offset_y", 0)
            col_width = enemy.get("collision_width", enemy["width"])
            col_height = enemy.get("collision_height", enemy["height"])
            
            # Scale for rendering
            col_rect = self.scale_position(
                pygame.Rect(col_x, col_y, col_width, col_height)
            )
            
            # Draw the collision box with transparency
            s = pygame.Surface((col_rect.width, col_rect.height), pygame.SRCALPHA)
            pygame.draw.rect(s, (255, 255, 0, 100), (0, 0, col_rect.width, col_rect.height))
            self.screen.blit(s, col_rect)
        
        # Draw health bar above enemy
        health_bar_width = enemy_rect.width
        health_bar_height = 5
        health_percentage = enemy["health"] / enemy["max_health"]
        
        # Background of health bar (gray)
        pygame.draw.rect(
            self.screen,
            (100, 100, 100),
            (
                enemy_rect.x,
                enemy_rect.y - health_bar_height - 2,
                health_bar_width,
                health_bar_height
            )
        )
        
        # Foreground of health bar (colored based on health)
        if health_percentage > 0.7:
            health_color = (0, 255, 0)  # Green
        elif health_percentage > 0.3:
            health_color = (255, 255, 0)  # Yellow
        else:
            health_color = (255, 0, 0)  # Red
            
        pygame.draw.rect(
            self.screen,
            health_color,
            (
                enemy_rect.x,
                enemy_rect.y - health_bar_height - 2,
                health_bar_width * health_percentage,
                health_bar_height
            )
        )
        
        # Draw enemy name above health bar with outline
        if "name" in enemy:
            # Set the font based on whether it's a boss
            if hasattr(self, 'bot_nickname_font'):
                name_font = self.bot_nickname_font  # Regular enemies
            elif hasattr(self, 'info_font'):
                name_font = self.info_font  # Fallback
            else:
                # Create font if necessary
                name_font = pygame.font.SysFont("Arial", 16)
            
            # Use larger font for bosses if available
            if is_boss:
                if hasattr(self, 'info_font'):
                    name_font = self.info_font  # Larger font for bosses
                elif hasattr(self, 'menu_font'):
                    name_font = self.menu_font  # Alternative
                else:
                    # Create font if necessary
                    name_font = pygame.font.SysFont("Arial", 24)
            
            # Draw name with outline for better contrast
            # For defeated enemies, position the name higher
            name_y_position = enemy_rect.y - health_bar_height - 15  # Default position
            
            # If enemy is defeated, move the name higher
            if enemy["health"] <= 0:
                name_y_position = enemy_rect.y - 30  # Higher position for defeated enemies
            
            # Check if enemy is a boss
            is_boss = "is_boss" in enemy and enemy["is_boss"]
            icon_width = 0
            
            if is_boss:
                # Get boss type from name
                icon_type = "Boss"  # Default
                if "boss_prefix" in enemy:
                    icon_type = enemy["boss_prefix"]
                
                # Try to get the icon from sprite manager
                icon = self.sprite_manager.get_boss_icon(icon_type)
                
                # Calculate icon position (left of the name)
                icon_size = 24
                
                # Measure text width to properly position the icon
                text_width = name_font.size(enemy["name"])[0]
                
                # Create more distance between icon and text (position icon far to the left)
                icon_x = enemy_rect.centerx - text_width//2 - icon_size - 5  # Reduced spacing
                icon_y = name_y_position - icon_size//2
                
                # Check if this boss already has a cached icon
                if "cached_icon" not in enemy:
                    # Cache the icon for this boss
                    enemy["cached_icon"] = pygame.transform.scale(icon, (icon_size, icon_size))
                
                # Draw the cached icon
                self.screen.blit(enemy["cached_icon"], (icon_x, icon_y))
                
                # Keep text centered on the enemy (don't adjust for icon)
                text_x = enemy_rect.centerx
                icon_width = 0  # Don't shift the text
            else:
                text_x = enemy_rect.centerx
            
            # Draw name with outline and adjusted position for icon
            self.draw_outlined_text(
                enemy["name"],
                name_font,
                (255, 255, 255),  # White text
                text_x,  # Use the calculated text position
                name_y_position,
                outline_color=(0, 0, 0),  # Black outline
                outline_width=1
            )
            
        # Draw direction indicator (aim line) for living enemies
        if "direction" in enemy and enemy["health"] > 0:
            angle_rad = math.radians(enemy["direction"])
            start_x = enemy["x"] + enemy["width"] / 2
            start_y = enemy["y"] + enemy["height"] / 2
            end_x = start_x + math.cos(angle_rad) * 20
            end_y = start_y + math.sin(angle_rad) * 20
            
            pygame.draw.line(
                self.screen,
                (255, 0, 0),  # Red line for enemies
                self.scale_position(start_x, start_y),
                self.scale_position(end_x, end_y),
                2
            )

def draw_text(self, text, font, color, x, y, centered=True, align="center"):
    """
    Helper function to draw text with proper scaling and positioning
    
    Args:
        text: Text string to render
        font: pygame Font object
        color: Color tuple (r,g,b) or (r,g,b,a)
        x, y: Position coordinates in original game space
        centered: Whether text should be centered at x,y (default: True)
        align: Alignment of the text (left, center, right)
    """
    text_surface = font.render(text, True, color)
    
    if centered:
        text_rect = text_surface.get_rect(center=(x, y))
    else:
        if align == "left":
            text_rect = text_surface.get_rect(topleft=(x, y))
        elif align == "right":
            text_rect = text_surface.get_rect(topright=(x, y))
        else:
            text_rect = text_surface.get_rect(center=(x, y))
    
    # Apply scaling
    scaled_x = text_rect.x * self.scale_factor + self.x_offset
    scaled_y = text_rect.y * self.scale_factor + self.y_offset
    
    # Position the text
    scaled_pos = (scaled_x, scaled_y)
    
    # For improved text rendering at larger scales, check if we need to scale the text
    if self.is_fullscreen and self.scale_factor > 1.5:
        # Scale the text itself for better clarity
        orig_width, orig_height = text_surface.get_size()
        scaled_text = pygame.transform.smoothscale(
            text_surface, 
            (int(orig_width * self.scale_factor), int(orig_height * self.scale_factor))
        )
        self.screen.blit(scaled_text, scaled_pos)
    else:
        self.screen.blit(text_surface, scaled_pos)

def draw_outlined_text(self, text, font, color, x, y, outline_color=(0, 0, 0), outline_width=1, centered=True, align="center"):
    """
    Draw text with an outline for better readability
    
    Args:
        text: Text string to render
        font: pygame Font object
        color: Text color tuple (r,g,b)
        x, y: Position coordinates in original game space
        outline_color: Color of the outline
        outline_width: Width of the outline in pixels
        centered: Whether text should be centered at x,y
        align: Alignment of the text (left, center, right)
    """
    # Create the main text surface
    text_surface = font.render(text, True, color)
    
    # Create a separate surface for the outline
    outline_surface = font.render(text, True, outline_color)
    
    if centered:
        text_rect = text_surface.get_rect(center=(x, y))
    else:
        if align == "left":
            text_rect = text_surface.get_rect(topleft=(x, y))
        elif align == "right":
            text_rect = text_surface.get_rect(topright=(x, y))
        else:
            text_rect = text_surface.get_rect(center=(x, y))
    
    # Apply scaling
    scaled_x = text_rect.x * self.scale_factor + self.x_offset
    scaled_y = text_rect.y * self.scale_factor + self.y_offset
    
    # Create scaled versions of the text surfaces if needed
    if self.is_fullscreen and self.scale_factor > 1.5:
        orig_width, orig_height = text_surface.get_size()
        scaled_width = int(orig_width * self.scale_factor)
        scaled_height = int(orig_height * self.scale_factor)
        
        text_surface = pygame.transform.smoothscale(text_surface, (scaled_width, scaled_height))
        outline_surface = pygame.transform.smoothscale(outline_surface, (scaled_width, scaled_height))
    
    # Draw the outline by offsetting the text in all directions
    for dx in range(-outline_width, outline_width + 1):
        for dy in range(-outline_width, outline_width + 1):
            if dx != 0 or dy != 0:  # Skip the center position
                # Draw outline positions
                self.screen.blit(outline_surface, (scaled_x + dx, scaled_y + dy))
    
    # Draw the actual text on top of the outline
    self.screen.blit(text_surface, (scaled_x, scaled_y))

def scale_position(self, x, y=None, width=None, height=None):
    """
    Scale positions and dimensions for fullscreen mode.
    If y is None, x is assumed to be a tuple or list (x, y) or a pygame.Rect.
    Returns scaled coordinates as tuple, or Rect if width/height are provided.
    """
    if not self.is_fullscreen:
        if y is None:
            if hasattr(x, 'x'):  # It's a Rect
                if width is None and height is None:
                    return x  # Return original rect if no sizes provided
                return pygame.Rect(x.x, x.y, width or x.width, height or x.height)
            return x  # Return original coordinates/tuple
        
        if width is not None and height is not None:
            return pygame.Rect(x, y, width, height)
        return (x, y)
    
    # Handle different input types
    if y is None:
        if hasattr(x, 'x'):  # It's a Rect
            scaled_x = x.x * self.scale_factor + self.x_offset
            scaled_y = x.y * self.scale_factor + self.y_offset
            scaled_w = x.width * self.scale_factor if width is None else width * self.scale_factor
            scaled_h = x.height * self.scale_factor if height is None else height * self.scale_factor
            return pygame.Rect(scaled_x, scaled_y, scaled_w, scaled_h)
        
        # Assume it's a tuple/list of (x,y)
        return (x[0] * self.scale_factor + self.x_offset, 
                x[1] * self.scale_factor + self.y_offset)
    
    # Handle separate x,y coordinates
    scaled_x = x * self.scale_factor + self.x_offset
    scaled_y = y * self.scale_factor + self.y_offset
    
    if width is not None and height is not None:
        scaled_w = width * self.scale_factor
        scaled_h = height * self.scale_factor
        return pygame.Rect(scaled_x, scaled_y, scaled_w, scaled_h)
    
    return (scaled_x, scaled_y)

# Add these methods to the PyBrawl class
def patch_pybrawl_class():
    """Patch the PyBrawl class with rendering functions"""
    from game_engine import PyBrawl
    
    PyBrawl.draw_title_screen = draw_title_screen
    PyBrawl.draw_character_select = draw_character_select
    PyBrawl.draw_gameplay = draw_gameplay
    PyBrawl.draw_game_over = draw_game_over
    PyBrawl.draw_outlined_text = draw_outlined_text
    PyBrawl.draw_map = draw_map  # Add the new map drawing function
    PyBrawl.scale_position = scale_position
    PyBrawl.draw_text = draw_text  # Add the draw_text function
    PyBrawl.draw_enemies = draw_enemies  # Add the new enemy drawing function
    
    # Make sure to add optional functions only if they exist
    if 'draw_win_screen' in globals():
        PyBrawl.draw_win_screen = draw_win_screen
    
    if 'draw_kill_notifications' in globals():
        PyBrawl.draw_kill_notifications = draw_kill_notifications
        
    if 'draw_hud' in globals():
        PyBrawl.draw_hud = draw_hud
        
    if 'draw_health_bar' in globals():
        PyBrawl.draw_health_bar = draw_health_bar
        
    if 'draw_wave_info' in globals():
        PyBrawl.draw_wave_info = draw_wave_info

# Register renderer functions with PyBrawl
patch_pybrawl_class()
