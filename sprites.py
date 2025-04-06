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
        """Create boss icons using Pygame drawing primitives"""
        size = 24
        
        # Create boss icons
        self.boss_icons = {}
        
        # Chief icons
        self.boss_icons["Chief"] = []
        
        # Fist icon
        fist = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(fist, (200, 200, 200), (size//2, size//2), size//2 - 2)
        pygame.draw.line(fist, (100, 100, 100), (size//3, size//3), (size*2//3, size*2//3), 3)
        pygame.draw.line(fist, (100, 100, 100), (size//3, size*2//3), (size*2//3, size//3), 3)
        self.boss_icons["Chief"].append(fist)
        
        # Badge icon
        badge = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.polygon(badge, (200, 200, 200), [
            (size//2, 2),  # Top
            (2, size//2),  # Left
            (size//2, size-2),  # Bottom
            (size-2, size//2),  # Right
        ])
        pygame.draw.circle(badge, (150, 150, 150), (size//2, size//2), size//4)
        self.boss_icons["Chief"].append(badge)
        
        # Commander icons
        self.boss_icons["Commander"] = []
        
        # Medal icon
        medal = pygame.Surface((size, size), pygame.SRCALPHA)
        # Base shape
        pygame.draw.circle(medal, (220, 180, 50), (size//2, size//2), size//2 - 2)
        # Ribbon
        pygame.draw.polygon(medal, (100, 100, 180), [
            (size//2, size//4),
            (size//3, size*2//3),
            (size*2//3, size*2//3)
        ])
        # Star in the center
        pygame.draw.polygon(medal, (255, 255, 255), [
            (size//2, size//3),  # Top
            (size//2 + 5, size//2),  # Right
            (size//2, size*2//3),  # Bottom
            (size//2 - 5, size//2),  # Left
        ])
        self.boss_icons["Commander"].append(medal)
        
        # General icons
        self.boss_icons["General"] = []
        
        # Shield icon
        shield = pygame.Surface((size, size), pygame.SRCALPHA)
        # Shield shape
        pygame.draw.polygon(shield, (70, 70, 200), [
            (size//2, 4),  # Top
            (4, size//3),  # Left
            (size//2, size-4),  # Bottom
            (size-4, size//3),  # Right
        ])
        # Star emblem
        pygame.draw.polygon(shield, (255, 255, 200), [
            (size//2, size//3),  # Top
            (size//2 + 6, size//2),  # Right
            (size//2, size*2//3),  # Bottom
            (size//2 - 6, size//2),  # Left
        ])
        self.boss_icons["General"].append(shield)
        
        # Overlord icons
        self.boss_icons["Overlord"] = []
        
        # Crown icon
        crown = pygame.Surface((size, size), pygame.SRCALPHA)
        # Crown base
        pygame.draw.polygon(crown, (220, 180, 50), [
            (4, size*2//3),  # Bottom left
            (size-4, size*2//3),  # Bottom right
            (size*3//4, size//3),  # Right peak
            (size//2, size//2),  # Middle valley
            (size//4, size//3),  # Left peak
        ])
        # Gems on the crown
        pygame.draw.circle(crown, (255, 50, 50), (size//4, size//3), 3)  # Ruby
        pygame.draw.circle(crown, (50, 50, 255), (size//2, size//2), 3)  # Sapphire
        pygame.draw.circle(crown, (50, 255, 50), (size*3//4, size//3), 3)  # Emerald
        self.boss_icons["Overlord"].append(crown)
        
        # King icons
        self.boss_icons["King"] = []
        
        # Scepter icon
        scepter = pygame.Surface((size, size), pygame.SRCALPHA)
        # Scepter staff
        pygame.draw.rect(scepter, (150, 120, 50), (size//2-3, size//4, 6, size*2//3))
        # Ornate top
        pygame.draw.circle(scepter, (220, 180, 50), (size//2, size//4), size//6)
        pygame.draw.circle(scepter, (255, 50, 50), (size//2, size//4), size//10)  # Ruby
        # Base of scepter
        pygame.draw.rect(scepter, (220, 180, 50), (size//2-6, size*2//3+5, 12, 5), border_radius=3)
        self.boss_icons["King"].append(scepter)

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
