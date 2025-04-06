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
    
    # Пахан icons (aggressive)
    icons["pahan_fist"] = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.circle(icons["pahan_fist"], (255, 80, 80), (size//2, size//2), size//2 - 4)
    pygame.draw.circle(icons["pahan_fist"], (200, 50, 50), (size//2, size//2), size//2 - 8)
    pygame.draw.rect(icons["pahan_fist"], (220, 100, 100), (size//3, size//3, size//3, size//3))
    pygame.draw.line(icons["pahan_fist"], (255, 200, 200), (size//3, size//3), (size*2//3, size*2//3), 4)
    pygame.draw.line(icons["pahan_fist"], (255, 200, 200), (size//3, size*2//3), (size*2//3, size//3), 4)
    
    # Пахан fire icon
    icons["pahan_fire"] = pygame.Surface((size, size), pygame.SRCALPHA)
    points = [
        (size//2, 4),  # Top
        (size//4, size//2),  # Left middle
        (size//3, size//2),  # Inner left
        (size//2, size*3//4),  # Bottom middle
        (size*2//3, size//2),  # Inner right
        (size*3//4, size//2),  # Right middle
    ]
    pygame.draw.polygon(icons["pahan_fire"], (255, 100, 0), points)
    pygame.draw.polygon(icons["pahan_fire"], (255, 200, 0), [
        (size//2, size//4),
        (size*2//5, size//2),
        (size//2, size*2//3),
        (size*3//5, size//2)
    ])
    
    # Командир medal icon
    icons["komandir_medal"] = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.circle(icons["komandir_medal"], (255, 215, 0), (size//2, size//2), size//2 - 4)
    pygame.draw.circle(icons["komandir_medal"], (200, 170, 0), (size//2, size//2), size//2 - 8)
    pygame.draw.polygon(icons["komandir_medal"], (255, 255, 255), [
        (size//2, size//4),  # Top
        (size//3, size*2//3),  # Bottom left
        (size*2//3, size*2//3)  # Bottom right
    ])
    
    # Дегенерал shield/toilet icon
    icons["degeneral_shield"] = pygame.Surface((size, size), pygame.SRCALPHA)
    # Toilet seat shape
    pygame.draw.ellipse(icons["degeneral_shield"], (240, 240, 240), (4, 4, size-8, size*2//3))
    pygame.draw.ellipse(icons["degeneral_shield"], (200, 200, 200), (size//4, size//6, size//2, size//3))
    # Handle/tank
    pygame.draw.rect(icons["degeneral_shield"], (200, 200, 200), (size//3, size*2//3, size//3, size//3))
    # Water effect
    pygame.draw.arc(icons["degeneral_shield"], (100, 200, 255), (size//4, size//3, size//2, size//4), 0, 3.14, 2)
    
    # Владыка crown icon
    icons["vladyka_crown"] = pygame.Surface((size, size), pygame.SRCALPHA)
    # Base shape - yellow paper
    pygame.draw.polygon(icons["vladyka_crown"], (255, 230, 100), [
        (4, size*2//3),  # Bottom left
        (size-4, size*2//3),  # Bottom right
        (size*3//4, size//3),  # Right peak
        (size//2, size//2),  # Middle valley (higher)
        (size//4, size//3),  # Left peak
    ])
    # Ketchup and mustard stains
    pygame.draw.circle(icons["vladyka_crown"], (255, 50, 50), (size//4, size//2), 6)  # Ketchup
    pygame.draw.circle(icons["vladyka_crown"], (255, 200, 50), (size*3//4, size//2), 6)  # Mustard
    # Crumpled effect
    pygame.draw.line(icons["vladyka_crown"], (200, 180, 80), (size//3, size//2), (size//3, size*2//3), 2)
    pygame.draw.line(icons["vladyka_crown"], (200, 180, 80), (size*2//3, size//2), (size*2//3, size*2//3), 2)
    
    # Сцарь toy scepter icon
    icons["stsar_scepter"] = pygame.Surface((size, size), pygame.SRCALPHA)
    # Stick (bent/broken)
    pygame.draw.line(icons["stsar_scepter"], (150, 120, 50), (size//2, size//4), (size//2+10, size*3//4), 6)
    pygame.draw.line(icons["stsar_scepter"], (150, 120, 50), (size//2+10, size*3//4), (size//2, size*7//8), 6)
    # Plastic toy gem
    pygame.draw.circle(icons["stsar_scepter"], (255, 100, 255), (size//2, size//4), size//6)  # Pink plastic
    pygame.draw.circle(icons["stsar_scepter"], (200, 150, 200), (size//2, size//4), size//10)  # Highlight
    # Scotch tape holding it together
    pygame.draw.rect(icons["stsar_scepter"], (200, 200, 200, 150), (size//2-4, size*3//4-6, 20, 12), border_radius=2)
    
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
