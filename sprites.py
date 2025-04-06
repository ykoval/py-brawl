import pygame
import os
import random
import io

class SpriteManager:
    """Sprite manager for loading and handling game sprites"""
    
    def __init__(self):
        # Dictionary to store sprites
        self.sprites = {}
        
        # Set grid cell size for the 200x200px sprite sheet
        self.tile_size = 200  # Each sprite is 200x200 pixels in the grid
        
        # Check if the 200x200px sprite sheet exists
        sprite_path = os.path.join("assets", "sprite_200x200.png")
        if os.path.exists(sprite_path):
            self.load_sprites_from_grid(sprite_path)
        else:
            print(f"Warning: Sprite sheet not found at {sprite_path}")
            self.create_placeholder_sprites()
        
        # Initialize boss icons
        self.boss_icons = {}
        self.create_boss_icons()
    
    def load_sprites_from_grid(self, path):
        """Load sprites from a regular grid-based sprite sheet"""
        try:
            # Load the sprite sheet
            sprite_sheet = pygame.image.load(path).convert_alpha()
            
            # Get dimensions of the sheet
            sheet_width = sprite_sheet.get_width()
            sheet_height = sprite_sheet.get_height()
            
            # Calculate grid dimensions
            cols = sheet_width // self.tile_size
            rows = sheet_height // self.tile_size
            
            # Load sprites according to user's description:
            # 1. wall, 2. grass, 3. ground, 4. shelly, 5. colt, 6. el-primo, 7-9 enemy bots, 10. grave icon
            
            # Define sprite mapping from grid positions
            # Format: [name, row, col]
            sprite_positions = [
                # First row - Tiles (Wall, Grass, Ground)
                ["wall", 0, 0],     # 1. wall
                ["grass", 0, 1],    # 2. grass
                ["ground", 0, 2],   # 3. ground
                
                # Second row - Brawlers
                ["shelly", 1, 0],   # 4. shelly
                ["colt", 1, 1],     # 5. colt
                ["el_primo", 1, 2], # 6. el-primo
                
                # Third row - Enemy bots
                ["enemy_bot1", 2, 0], # 7. enemy bot 1
                ["enemy_bot2", 2, 1], # 8. enemy bot 2
                ["enemy_bot3", 2, 2], # 9. enemy bot 3
                
                # Fourth row - Grave icon and possibly others
                ["grave", 3, 0],    # 10. grave icon
            ]
            
            # Load each sprite based on its position
            for name, row, col in sprite_positions:
                # Only attempt to extract if the position is within grid bounds
                if row < rows and col < cols:
                    self.sprites[name] = self.get_sprite_from_grid(sprite_sheet, row, col)
                else:
                    print(f"Warning: Grid position ({row}, {col}) is out of bounds for sprite '{name}'")
            
            # Build enemy portraits list for easy random selection
            self.enemy_portraits = []
            valid_enemy_keys = ['enemy_bot1', 'enemy_bot2', 'enemy_bot3']
            for key in valid_enemy_keys:
                if key in self.sprites and self.sprites[key] is not None:
                    self.enemy_portraits.append(self.sprites[key])
        except Exception as e:
            print(f"Error loading sprites from grid: {e}")
            self.create_placeholder_sprites()
    
    def get_sprite_from_grid(self, sheet, row, col):
        """Extract a sprite from a regular grid layout"""
        x = col * self.tile_size
        y = row * self.tile_size
        
        # Check if the grid position is within the sheet bounds
        if x + self.tile_size <= sheet.get_width() and y + self.tile_size <= sheet.get_height():
            # Create a new surface for the sprite with alpha channel
            sprite = pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA)
            
            # Copy the sprite from the sheet to our new surface
            sprite.blit(sheet, (0, 0), (x, y, self.tile_size, self.tile_size))
            
            return sprite
        else:
            print(f"Warning: Grid position ({row}, {col}) is out of bounds")
            return self.create_colored_square((255, 0, 0))  # Return red square for out of bounds
    
    def create_placeholder_sprites(self):
        """Create colored rectangles as placeholder sprites"""
        print("Creating placeholder sprites")
        self.sprites['wall'] = self.create_colored_square((0, 100, 255))   # Blue
        self.sprites['grass'] = self.create_colored_square((0, 200, 0))    # Green
        self.sprites['ground'] = self.create_colored_square((210, 180, 140)) # Tan
        self.sprites['shelly'] = self.create_colored_square((128, 0, 255))  # Purple
        self.sprites['colt'] = self.create_colored_square((255, 100, 0))    # Orange-Red
        self.sprites['el_primo'] = self.create_colored_square((0, 255, 0))  # Bright Green
        self.sprites['grave'] = self.create_colored_square((80, 80, 80))    # Dark gray
        
        # Create enemy portraits
        self.enemy_portraits = [
            self.create_colored_square((255, 0, 0)),    # Red
            self.create_colored_square((0, 255, 0)),    # Green
            self.create_colored_square((0, 0, 255)),    # Blue
        ]
    
    def create_colored_square(self, color):
        """Create a colored square sprite as placeholder"""
        surface = pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA)
        pygame.draw.rect(surface, color, (0, 0, self.tile_size, self.tile_size))
        pygame.draw.rect(surface, (0, 0, 0), (0, 0, self.tile_size, self.tile_size), 1)  # Black border
        return surface
    
    def get_enemy_portrait(self, index=None):
        """Get an enemy portrait, either by index or randomly"""
        if not self.enemy_portraits:
            return self.create_colored_square((255, 0, 0))
            
        if index is None or index >= len(self.enemy_portraits):
            return random.choice(self.enemy_portraits)
        else:
            return self.enemy_portraits[index]
    
    def get_scaled_sprite(self, sprite_name, width, height):
        """Get a scaled version of a sprite"""
        if sprite_name not in self.sprites:
            print(f"Warning: Sprite '{sprite_name}' not found in available sprites: {list(self.sprites.keys())}")
            # Return a default colored square if sprite not found
            default = self.create_colored_square((255, 0, 0))  # Red square for missing sprites
            return pygame.transform.scale(default, (width, height))
        
        # Return a scaled version of the sprite
        return pygame.transform.scale(self.sprites[sprite_name], (width, height))

    def get_scaled_grave_sprite(self, width, height):
        """Get a scaled version of the grave sprite"""
        return self.get_scaled_sprite('grave', width, height)
    
    def get_tile_sprite(self, tile_type, width, height):
        """Get a scaled tile sprite based on type: wall, grass, or ground"""
        if tile_type in ['wall', 'grass', 'ground']:
            return self.get_scaled_sprite(tile_type, width, height)
        else:
            print(f"Warning: Unknown tile type '{tile_type}'")
            return self.get_scaled_sprite('ground', width, height)  # Default to ground

    def create_boss_icons(self):
        """Create disrespectful boss icons using Pygame drawing primitives"""
        size = 24
        
        # Boss icons ("Пахан" - mocking the thug boss)
        self.boss_icons["Пахан"] = []
        
        # Broken fist/thumbs down icon
        fist = pygame.Surface((size, size), pygame.SRCALPHA)
        # Base shape (red-ish)
        pygame.draw.circle(fist, (255, 80, 80), (size//2, size//2), size//2 - 2)
        # Thumbs down gesture
        pygame.draw.rect(fist, (200, 50, 50), (size//3, size//3, size//3, size//2))
        pygame.draw.circle(fist, (200, 50, 50), (size//2, size*5//6), size//6)
        # Add a crossed-out effect
        pygame.draw.line(fist, (255, 255, 255), (size//4, size//4), (size*3//4, size*3//4), 3)
        pygame.draw.line(fist, (255, 255, 255), (size*3//4, size//4), (size//4, size*3//4), 3)
        self.boss_icons["Пахан"].append(fist)
        
        # Toilet paper roll instead of fire
        toilet = pygame.Surface((size, size), pygame.SRCALPHA)
        # Roll base
        pygame.draw.ellipse(toilet, (240, 240, 240), (size//4, size//4, size//2, size//2))
        pygame.draw.ellipse(toilet, (200, 200, 200), (size//4+2, size//4+2, size//2-4, size//2-4))
        # Hanging paper
        pygame.draw.rect(toilet, (240, 240, 240), (size//2-2, size//2, 4, size//2))
        pygame.draw.arc(toilet, (240, 240, 240), (size//4, size*2//3, size//2, size//3), 0, 3.14, 3)
        self.boss_icons["Пахан"].append(toilet)
        
        # Commander icons ("Командир" - mock military leader)
        self.boss_icons["Командир"] = []
        
        # Broken medal/participation trophy
        medal = pygame.Surface((size, size), pygame.SRCALPHA)
        # Base shape
        pygame.draw.circle(medal, (255, 215, 0), (size//2, size//2), size//2 - 2)
        # "Participation" ribbon (blue rather than gold)
        pygame.draw.polygon(medal, (100, 100, 255), [
            (size//2, size//4),
            (size//3, size*2//3),
            (size*2//3, size*2//3)
        ])
        # Add #1 LOSER text suggestion
        pygame.draw.line(medal, (0, 0, 0), (size//2-4, size//2-2), (size//2-4, size//2+4), 2)  # L
        pygame.draw.arc(medal, (0, 0, 0), (size//2-2, size//2-2, 7, 7), 3.14, 6.28, 2)  # o
        self.boss_icons["Командир"].append(medal)
        
        # "Дегенерал" icons (instead of "Генерал" - mock authority even more)
        self.boss_icons["Дегенерал"] = []
        
        # Paper shield/toilet seat cover
        shield = pygame.Surface((size, size), pygame.SRCALPHA)
        # Toilet seat shape
        pygame.draw.ellipse(shield, (240, 240, 240), (2, 2, size-4, size*2//3))
        pygame.draw.ellipse(shield, (200, 200, 200), (size//4, size//6, size//2, size//3))
        # Handle/tank
        pygame.draw.rect(shield, (200, 200, 200), (size//3, size*2//3, size//3, size//3))
        # Water effect
        pygame.draw.arc(shield, (100, 200, 255), (size//4, size//3, size//2, size//4), 0, 3.14, 2)
        self.boss_icons["Дегенерал"].append(shield)
        
        # Overlord icons ("Владыка" - mock royalty)
        self.boss_icons["Владыка"] = []
        
        # Burger King style paper crown
        crown = pygame.Surface((size, size), pygame.SRCALPHA)
        # Base shape - yellow paper
        pygame.draw.polygon(crown, (255, 230, 100), [
            (2, size*2//3),  # Bottom left
            (size-2, size*2//3),  # Bottom right
            (size*3//4, size//3),  # Right peak
            (size//2, size//2),  # Middle valley (higher)
            (size//4, size//3),  # Left peak
        ])
        # Ketchup and mustard stains
        pygame.draw.circle(crown, (255, 50, 50), (size//4, size//2), 3)  # Ketchup
        pygame.draw.circle(crown, (255, 200, 50), (size*3//4, size//2), 3)  # Mustard
        # Crumpled effect
        pygame.draw.line(crown, (200, 180, 80), (size//3, size//2), (size//3, size*2//3), 1)
        pygame.draw.line(crown, (200, 180, 80), (size*2//3, size//2), (size*2//3, size*2//3), 1)
        self.boss_icons["Владыка"].append(crown)
        
        # "Сцарь" icons (instead of "Царь" - mock supreme authority even more)
        self.boss_icons["Сцарь"] = []
        
        # Toy scepter/broken stick
        scepter = pygame.Surface((size, size), pygame.SRCALPHA)
        # Stick (bent/broken)
        pygame.draw.line(scepter, (150, 120, 50), (size//2, size//4), (size//2+5, size*3//4), 3)
        pygame.draw.line(scepter, (150, 120, 50), (size//2+5, size*3//4), (size//2, size*7//8), 3)
        # Plastic toy gem
        pygame.draw.circle(scepter, (255, 100, 255), (size//2, size//4), size//6)  # Pink plastic
        pygame.draw.circle(scepter, (200, 150, 200), (size//2, size//4), size//10)  # Highlight
        # Scotch tape holding it together
        pygame.draw.rect(scepter, (200, 200, 200, 150), (size//2-2, size*3//4-3, 10, 6), border_radius=1)
        self.boss_icons["Сцарь"].append(scepter)

    def get_boss_icon(self, boss_prefix):
        """Get a random boss icon for the given prefix"""
        if boss_prefix in self.boss_icons and self.boss_icons[boss_prefix]:
            return random.choice(self.boss_icons[boss_prefix])
        
        # Fallback - create a default crown icon
        print(f"WARNING: No icon found for prefix '{boss_prefix}', using fallback")
        size = 24
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.polygon(surface, (255, 215, 0), [
            (size//2, 0), 
            (0, size//2), 
            (size//4, size//2), 
            (size//2, size), 
            (3*size//4, size//2), 
            (size, size//2)
        ])
        return surface
