#!/usr/bin/env python3
import pygame
import os
import sys

# Initialize pygame
pygame.init()

# Create output directory if it doesn't exist
output_dir = os.path.join("assets", "icons", "png")
os.makedirs(output_dir, exist_ok=True)

def create_boss_icons():
    """Create boss icons using Pygame drawing primitives and save them as PNG files"""
    # Dictionary to store all icons
    icons = {}
    size = 48  # Making them a bit larger for better quality
    
    # Chief icons (previously "Пахан")
    icons["chief_fist"] = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.circle(icons["chief_fist"], (200, 200, 200), (size//2, size//2), size//2 - 4)
    pygame.draw.line(icons["chief_fist"], (100, 100, 100), (size//3, size//3), (size*2//3, size*2//3), 5)
    pygame.draw.line(icons["chief_fist"], (100, 100, 100), (size//3, size*2//3), (size*2//3, size//3), 5)
    
    # Chief badge icon
    icons["chief_badge"] = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.polygon(icons["chief_badge"], (200, 200, 200), [
        (size//2, 4),  # Top
        (4, size//2),  # Left
        (size//2, size-4),  # Bottom
        (size-4, size//2),  # Right
    ])
    pygame.draw.circle(icons["chief_badge"], (150, 150, 150), (size//2, size//2), size//4)
    
    # Commander medal icon
    icons["commander_medal"] = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.circle(icons["commander_medal"], (220, 180, 50), (size//2, size//2), size//2 - 4)
    pygame.draw.polygon(icons["commander_medal"], (100, 100, 180), [
        (size//2, size//4),  # Top
        (size//3, size*2//3),  # Bottom left
        (size*2//3, size*2//3)  # Bottom right
    ])
    # Star in the center
    pygame.draw.polygon(icons["commander_medal"], (255, 255, 255), [
        (size//2, size//3),  # Top
        (size//2 + 8, size//2),  # Right
        (size//2, size*2//3),  # Bottom
        (size//2 - 8, size//2),  # Left
    ])
    
    # General shield icon
    icons["general_shield"] = pygame.Surface((size, size), pygame.SRCALPHA)
    # Shield shape
    pygame.draw.polygon(icons["general_shield"], (70, 70, 200), [
        (size//2, 4),  # Top
        (4, size//3),  # Left
        (size//2, size-4),  # Bottom
        (size-4, size//3),  # Right
    ])
    # Star emblem
    pygame.draw.polygon(icons["general_shield"], (255, 255, 200), [
        (size//2, size//3),  # Top
        (size//2 + 10, size//2),  # Right
        (size//2, size*2//3),  # Bottom
        (size//2 - 10, size//2),  # Left
    ])
    
    # Overlord crown icon
    icons["overlord_crown"] = pygame.Surface((size, size), pygame.SRCALPHA)
    # Crown base
    pygame.draw.polygon(icons["overlord_crown"], (220, 180, 50), [
        (4, size*2//3),  # Bottom left
        (size-4, size*2//3),  # Bottom right
        (size*3//4, size//3),  # Right peak
        (size//2, size//2),  # Middle valley
        (size//4, size//3),  # Left peak
    ])
    # Gems on the crown
    pygame.draw.circle(icons["overlord_crown"], (255, 50, 50), (size//4, size//3), 6)  # Ruby
    pygame.draw.circle(icons["overlord_crown"], (50, 50, 255), (size//2, size//2), 6)  # Sapphire
    pygame.draw.circle(icons["overlord_crown"], (50, 255, 50), (size*3//4, size//3), 6)  # Emerald
    
    # King scepter icon
    icons["king_scepter"] = pygame.Surface((size, size), pygame.SRCALPHA)
    # Scepter staff
    pygame.draw.rect(icons["king_scepter"], (150, 120, 50), (size//2-4, size//4, 8, size*2//3))
    # Ornate top
    pygame.draw.circle(icons["king_scepter"], (220, 180, 50), (size//2, size//4), size//6)
    pygame.draw.circle(icons["king_scepter"], (255, 50, 50), (size//2, size//4), size//10)  # Ruby
    # Base of scepter
    pygame.draw.rect(icons["king_scepter"], (220, 180, 50), (size//2-8, size*7//8-8, 16, 8), border_radius=3)
    
    return icons

def save_icons_to_png(icons):
    """Save all icons to PNG files"""
    for name, surface in icons.items():
        filepath = os.path.join(output_dir, f"{name}.png")
        pygame.image.save(surface, filepath)
        print(f"Saved {filepath}")

def main():
    """Main function to generate and save icons"""
    print("Generating boss icons as PNG files...")
    
    # Create icons
    icons = create_boss_icons()
    
    # Save icons to PNG files
    save_icons_to_png(icons)
    
    print(f"Successfully saved {len(icons)} icons to {output_dir}")

if __name__ == "__main__":
    main()
    pygame.quit()
