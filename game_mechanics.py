import pygame
import random
import math
import sys
from game_engine import GameState, SCREEN_WIDTH, SCREEN_HEIGHT, PyBrawl

# Arrays for dynamic enemy name generation
WHO = [
    "Путин",
    "Лавров",
    "Ваня",
    "Шойгу",
    "Медведев",
    "Песков",
    "Рохлин",
    "Собчак",
    "Патрушев",
    "Жириновский",
    "Герасимов",
    "Кадыров",
    "Чуркин",
    "Володин",
    "Мишустин",
    "Сурков",
    "Бабурин",
    "Ткачёв",
    "Коровин",
    "Гиркин"
]

TERMS = [
    "Пидор",
    "Урод",
    "Лох",
    "Трус",
    "Свинья",
    "Идиот",
    "Балабол",
    "Колбаса",
    "Говноед",
    "Мразь",
    "Тварь",
    "Жопа",
    "Убийца",
    "Обманщик",
    "Сволочь",
    "Лохмотник",
    "Шлюха",
    "Безмозгов",
    "Говняшник"
]

def generate_map(self):
    """Generate the game map with walls and bushes"""
    max_attempts = 10  # Maximum attempts to generate a valid map
    
    for attempt in range(max_attempts):
        # Clear existing map elements
        self.walls = []
        self.bushes = []
        
        # Create border walls
        for x in range(self.map_width):
            self.walls.append({"x": x * self.tile_size, "y": 0, "width": self.tile_size, "height": self.tile_size})
            self.walls.append({"x": x * self.tile_size, "y": (self.map_height-1) * self.tile_size, 
                              "width": self.tile_size, "height": self.tile_size})
        
        for y in range(self.map_height):
            self.walls.append({"x": 0, "y": y * self.tile_size, "width": self.tile_size, "height": self.tile_size})
            self.walls.append({"x": (self.map_width-1) * self.tile_size, "y": y * self.tile_size, 
                              "width": self.tile_size, "height": self.tile_size})
        
        # Create random walls
        for _ in range(15):
            x = random.randint(2, self.map_width - 3) * self.tile_size
            y = random.randint(2, self.map_height - 3) * self.tile_size
            # Create wall clusters for more interesting map
            for dx, dy in [(0, 0), (1, 0), (0, 1), (1, 1)]:
                if random.random() < 0.7:  # 70% chance to place adjacent wall
                    self.walls.append({
                        "x": x + dx * self.tile_size, 
                        "y": y + dy * self.tile_size,
                        "width": self.tile_size, 
                        "height": self.tile_size
                    })
        
        # Check if map is fully connected (all open areas are reachable)
        if self.is_map_fully_connected():
            # Map is good, now add bushes
            self.add_bushes()
            return  # Successfully generated a connected map
        
        # If we get here, map generation failed this attempt
        print(f"Map generation attempt {attempt+1} failed - trying again")
    
    # If all attempts failed, create a very simple map
    print("All map generation attempts failed, creating simple map")
    self.walls = []
    self.bushes = []
    
    # Create only border walls for a simple open map
    for x in range(self.map_width):
        self.walls.append({"x": x * self.tile_size, "y": 0, "width": self.tile_size, "height": self.tile_size})
        self.walls.append({"x": x * self.tile_size, "y": (self.map_height-1) * self.tile_size, 
                          "width": self.tile_size, "height": self.tile_size})
    
    for y in range(self.map_height):
        self.walls.append({"x": 0, "y": y * self.tile_size, "width": self.tile_size, "height": self.tile_size})
        self.walls.append({"x": (self.map_width-1) * self.tile_size, "y": y * self.tile_size, 
                          "width": self.tile_size, "height": self.tile_size})
    
    # Add a few bushes to the simple map
    self.add_bushes()

def add_bushes(self):
    """Add bushes to the map"""
    # Create bushes
    for _ in range(10):
        x = random.randint(1, self.map_width - 2) * self.tile_size
        y = random.randint(1, self.map_height - 2) * self.tile_size
        
        # Check if the position isn't occupied by a wall
        if not any(w["x"] == x and w["y"] == y for w in self.walls):
            # Create bush clusters
            for dx, dy in [(0, 0), (1, 0), (0, 1), (1, 1), (-1, 0), (0, -1)]:
                if random.random() < 0.6:  # 60% chance to place adjacent bush
                    bush_x = x + dx * self.tile_size
                    bush_y = y + dy * self.tile_size
                    # Check if this position doesn't overlap with walls
                    if not any(w["x"] == bush_x and w["y"] == bush_y for w in self.walls):
                        self.bushes.append({
                            "x": bush_x, 
                            "y": bush_y,
                            "width": self.tile_size, 
                            "height": self.tile_size
                        })

def is_map_fully_connected(self):
    """Check if all open tiles in the map are reachable from a single starting point"""
    # Create a grid representation of the map
    grid = [[0 for _ in range(self.map_height)] for _ in range(self.map_width)]
    
    # Mark walls as obstacles (1)
    for wall in self.walls:
        grid_x = wall["x"] // self.tile_size
        grid_y = wall["y"] // self.tile_size
        
        # Skip if outside valid grid range
        if 0 <= grid_x < self.map_width and 0 <= grid_y < self.map_height:
            grid[grid_x][grid_y] = 1
    
    # Count total number of open spaces
    total_open_spaces = sum(row.count(0) for row in grid)
    
    # Find a starting point (any open cell)
    start_x, start_y = None, None
    for x in range(self.map_width):
        for y in range(self.map_height):
            if grid[x][y] == 0:
                start_x, start_y = x, y
                break
        if start_x is not None:
            break
    
    if start_x is None:
        # No open spaces found (all walls), which shouldn't happen
        return False
    
    # Perform BFS to count reachable spaces
    visited = set()
    queue = [(start_x, start_y)]
    visited.add((start_x, start_y))
    
    # Directions: up, right, down, left
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    
    while queue:
        x, y = queue.pop(0)
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            
            # Check if new position is within bounds and is an open space
            if (0 <= nx < self.map_width and 
                0 <= ny < self.map_height and 
                grid[nx][ny] == 0 and 
                (nx, ny) not in visited):
                
                queue.append((nx, ny))
                visited.add((nx, ny))
    
    # If the number of visited tiles equals the total open spaces,
    # then the map is fully connected
    return len(visited) == total_open_spaces

def spawn_enemies(self, count):
    """Spawn a number of enemies at random positions"""
    # Use persistent sets from the game engine instead of local sets
    # These will maintain name uniqueness across all waves
    
    # Determine if we should spawn a boss
    # Always spawn a boss in every wave
    spawn_boss = True
    
    # If we're spawning a boss, we'll spawn one boss and some regular enemies
    if spawn_boss:
        boss_count = 1
        regular_count = max(1, count - boss_count)  # Ensure at least one regular enemy
    else:
        boss_count = 0
        regular_count = count
    
    # Spawn regular enemies
    for _ in range(regular_count):
        # Find a valid spawn position away from the player and not inside walls
        while True:
            x = random.randint(1, self.map_width - 2) * self.tile_size
            y = random.randint(1, self.map_height - 2) * self.tile_size
            
            # Check if the position isn't occupied by a wall
            wall_collision = any(
                x < w["x"] + w["width"] and 
                x + self.tile_size > w["x"] and 
                y < w["y"] + w["height"] and 
                y + self.tile_size > w["y"] 
                for w in self.walls
            )
            
            # Make sure it's not too close to the player
            player_dist = math.sqrt((x - self.player["x"])**2 + (y - self.player["y"])**2)
            if not wall_collision and player_dist > 200:
                break
        
        # Generate random health between 40-60
        health = random.randint(40, 60)
        
        # Get available words list (words not yet used)
        available_first_words = [word for word in WHO if word not in self.used_first_words]
        available_second_words = [word for word in TERMS if word not in self.used_second_words]
        
        # If all words are used, reset the lists
        if not available_first_words:
            available_first_words = WHO.copy()
            self.used_first_words.clear()
        
        if not available_second_words:
            available_second_words = TERMS.copy()
            self.used_second_words.clear()
        
        # Select random first and second words
        first_word = random.choice(available_first_words)
        second_word = random.choice(available_second_words)
        
        # Build the full name
        enemy_name = f"{first_word} {second_word}"
        
        # Ensure the name is unique
        while enemy_name in self.used_names:
            # Try different words
            available_first_words = [word for word in WHO if word not in self.used_first_words]
            available_second_words = [word for word in TERMS if word not in self.used_second_words]
            
            if not available_first_words:
                available_first_words = WHO.copy()
                self.used_first_words.clear()
            
            if not available_second_words:
                available_second_words = TERMS.copy()
                self.used_second_words.clear()
            
            first_word = random.choice(available_first_words)
            second_word = random.choice(available_second_words)
            enemy_name = f"{first_word} {second_word}"
        
        # Add to used sets
        self.used_first_words.add(first_word)
        self.used_second_words.add(second_word)
        self.used_names.add(enemy_name)
        
        # Create enemy with random attributes        
        self.enemies.append({
            "x": x,
            "y": y,
            "width": 30,
            "height": 30,
            "health": health,
            "max_health": health,  # Store max health for HP bar calculation
            "speed": random.uniform(1.0, 3.0),
            "damage": 10,
            "attack_speed": random.uniform(0.5, 1.5),
            "range": 150,
            "last_attack_time": 0,
            "last_regen_time": pygame.time.get_ticks(),  # Track time for health regeneration
            "regen_rate": random.uniform(0.5, 1.0),  # HP per second
            "color": (
                random.randint(100, 200),
                random.randint(100, 200),
                random.randint(100, 200)
            ),
            "direction": random.uniform(0, 360),
            "name": enemy_name,  # Add the random name
            "is_boss": False,  # Flag to indicate this is not a boss
            
            # Add default special attack properties (not used by regular enemies, but prevent KeyErrors)
            "special_cooldown": 10000,  # Higher cooldown than bosses
            "last_special_attack_time": 0,
            "attack_pattern": "normal"  # Default pattern
        })
    
    # Spawn boss enemies (if applicable)
    for _ in range(boss_count):
        boss_enemy = self.spawn_boss()
        self.enemies.append(boss_enemy)

def spawn_boss(self):
    """Spawn a boss enemy"""
    # Find a valid spawn position away from the player and not inside walls
    while True:
        # Position bosses a bit further from the player initially
        x = random.randint(1, self.map_width - 2) * self.tile_size
        y = random.randint(1, self.map_height - 2) * self.tile_size
        
        # Randomize position slightly to avoid predictable placements
        x += random.randint(-1, 1) * self.tile_size
        y += random.randint(-1, 1) * self.tile_size
        
        # Make sure x and y are within valid map bounds
        x = max(1, min(self.map_width - 2, x // self.tile_size)) * self.tile_size
        y = max(1, min(self.map_height - 2, y // self.tile_size)) * self.tile_size
        
        # Check if the position isn't occupied by a wall
        wall_collision = any(
            x < w["x"] + w["width"] and 
            x + self.tile_size > w["x"] and 
            y < w["y"] + w["height"] and 
            y + self.tile_size > w["y"] 
            for w in self.walls
        )
        
        # Make sure it's not too close to the player
        player_dist = math.sqrt((x - self.player["x"])**2 + (y - self.player["y"])**2)
        if not wall_collision and player_dist > 300:  # Boss should be further away initially
            break
    
    # Generate boss health (much higher than regular enemies)
    boss_health = random.randint(150, 200)
    
    # Generate a boss name with a title prefix
    boss_prefixes = ["Пахан", "Командир", "Дегенерал", "Владыка", "Сцарь"]
    
    # Get available words (not used by other bosses or regular enemies)
    available_prefixes = [prefix for prefix in boss_prefixes if prefix not in self.used_first_words]
    available_second_words = [word for word in WHO if word.capitalize() not in self.used_second_words]
    
    # If all words are used, reset the lists (less likely for bosses)
    if not available_prefixes:
        available_prefixes = boss_prefixes.copy()
    
    if not available_second_words:
        available_second_words = WHO.copy()
    
    first_word = random.choice(available_prefixes)
    second_word = random.choice(available_second_words).capitalize()
    
    # We'll use icons instead of emojis - just set the name normally
    # The renderer will handle displaying the icon next to the name
    boss_name = f"{first_word} {second_word}"
    
    # Store the prefix for icon selection
    boss_prefix = first_word
    
    # Add to used sets
    self.used_first_words.add(first_word)
    self.used_second_words.add(second_word)
    
    # Ensure uniqueness of full name
    while boss_name in self.used_names:
        available_prefixes = [prefix for prefix in boss_prefixes if prefix not in self.used_first_words]
        available_second_words = [word for word in WHO if word.capitalize() not in self.used_second_words]
        
        if not available_prefixes:
            available_prefixes = boss_prefixes.copy()
        
        if not available_second_words:
            available_second_words = WHO.copy()
        
        first_word = random.choice(available_prefixes)
        second_word = random.choice(available_second_words).capitalize()
        boss_name = f"{first_word} {second_word}"
        boss_prefix = first_word
        
        self.used_first_words.add(first_word)
        self.used_second_words.add(second_word)
    
    self.used_names.add(boss_name)
    
    # Boss colors - more vivid and threatening
    boss_colors = [
        (255, 0, 0),  # Pure red
        (255, 50, 0),  # Red-orange
        (200, 0, 50),  # Crimson
    ]
    boss_color = random.choice(boss_colors)
    
    # Create the boss enemy with enhanced attributes
    boss_enemy = {
        "x": x,
        "y": y,
        "width": self.tile_size,
        "height": self.tile_size,
        "speed": 3.0,  # Slightly faster to make bosses more dangerous
        "health": boss_health,
        "max_health": boss_health,
        "color": boss_color,
        "direction": random.randint(0, 360),
        "last_shot_time": 0,
        "shot_cooldown": 1500,  # milliseconds
        "bullet_speed": 8.0,  # Faster bullets
        "is_boss": True,  # Flag to indicate it's a boss
        "boss_prefix": boss_prefix,  # Store the prefix for icon selection
        "name": boss_name,  # The enemy's name
        "last_ai_move_time": 0,
        "last_ai_threat_check": 0,
        "ai_threat_assessment": None,
        "collision_box": {  # Smaller collision box to allow movement
            "width": int(self.tile_size * 0.75),
            "height": int(self.tile_size * 0.75)
        },
        # Add missing attributes needed for enemy logic
        "range": 250,  # Bosses have longer attack range
        "damage": 20,  # Bosses deal more damage
        "attack_speed": 2.0,  # Attacks per second
        "last_attack_time": 0, 
        "last_regen_time": pygame.time.get_ticks(),
        "regen_rate": 2.0,  # Bosses regenerate faster
        
        # Special attack properties
        "special_cooldown": 5000,  # 5 seconds between special attacks
        "last_special_attack_time": 0,
        "attack_pattern": random.choice(["spread", "burst", "sniper"])  # Randomly assign an attack pattern
    }
    
    return boss_enemy

def create_bullet(self, x, y, direction, damage, is_player, color=(255, 255, 255)):
    """Create a bullet object"""
    self.bullets.append({
        "x": x,
        "y": y,
        "radius": 5,
        "speed": 10,
        "damage": damage,
        "direction": direction,
        "is_player": is_player,
        "color": color
    })

def update_gameplay(self):
    """Update all gameplay elements"""
    self.update_bullets()
    self.update_player_aim()  # Add auto-aim functionality
    self.update_enemies()
    self.update_player_health_regeneration()
    
    # Initialize kill notifications list if it doesn't exist
    if not hasattr(self, 'kill_notifications'):
        self.kill_notifications = []
    
    # Check if all enemies are dead
    if self.player is not None and len(self.enemies) == 0:
        # If we haven't completed all waves, start the next wave
        if self.current_wave < self.max_waves:
            self.current_wave += 1
            self.spawn_enemies(self.wave_size)  # Spawn the set number of enemies for this wave
        else:
            # All waves completed, show victory screen
            self.state = GameState.WIN_SCREEN

def update_bullets(self):
    """Update positions and collisions for all bullets"""
    bullets_to_remove = []
    
    for i, bullet in enumerate(self.bullets):
        # Update bullet position
        angle_rad = math.radians(bullet["direction"])
        bullet["x"] += math.cos(angle_rad) * bullet["speed"]
        bullet["y"] += math.sin(angle_rad) * bullet["speed"]
        
        # Check if bullet is out of bounds
        if (bullet["x"] < 0 or bullet["x"] > SCREEN_WIDTH or
            bullet["y"] < 0 or bullet["y"] > SCREEN_HEIGHT):
            bullets_to_remove.append(i)
            continue
        
        # Create bullet collision rectangle
        bullet_rect = pygame.Rect(
            bullet["x"] - bullet["radius"], 
            bullet["y"] - bullet["radius"],
            bullet["radius"] * 2, 
            bullet["radius"] * 2
        )
        
        # Check for wall collisions
        for wall in self.walls:
            wall_rect = pygame.Rect(wall["x"], wall["y"], wall["width"], wall["height"])
            
            if bullet_rect.colliderect(wall_rect):
                bullets_to_remove.append(i)
                break
        
        # Check for enemy collisions if player bullet
        if bullet["is_player"]:
            for j, enemy in enumerate(self.enemies):
                # Create enemy collision rectangle
                if "collision_width" in enemy:
                    enemy_rect = pygame.Rect(
                        enemy["x"] + enemy["collision_offset_x"], 
                        enemy["y"] + enemy["collision_offset_y"], 
                        enemy["collision_width"], 
                        enemy["collision_height"]
                    )
                else:
                    enemy_rect = pygame.Rect(
                        enemy["x"], enemy["y"], enemy["width"], enemy["height"]
                    )
                
                if bullet_rect.colliderect(enemy_rect):
                    # Damage enemy
                    enemy["health"] -= bullet["damage"]
                    bullets_to_remove.append(i)
                    
                    # Check if enemy is dead
                    if enemy["health"] <= 0:
                        # Add kill notification with current time
                        if hasattr(self, 'kill_notifications'):
                            self.kill_notifications.append({
                                'name': enemy["name"],
                                'time': pygame.time.get_ticks()
                            })
                        
                        # Remove enemy and increase score
                        self.enemies.pop(j)
                        self.score += 100
                    
                    break
        # Check for player collision if enemy bullet
        elif not bullet["is_player"]:
            player_rect = pygame.Rect(
                self.player["x"], self.player["y"],
                self.player["width"], self.player["height"]
            )
            
            if bullet_rect.colliderect(player_rect):
                # Hit the player
                self.player["health"] -= bullet["damage"]
                bullets_to_remove.append(i)
                
                # Check if player is defeated
                if self.player["health"] <= 0:
                    self.state = GameState.GAME_OVER
                    break
    
    # Remove bullets marked for deletion (in reverse order to avoid index issues)
    for i in sorted(bullets_to_remove, reverse=True):
        if i < len(self.bullets):
            self.bullets.pop(i)

def update_enemies(self):
    """Update enemy behavior and attacks"""
    current_time = pygame.time.get_ticks()
    
    # First pass - update direction and attack logic
    for enemy in self.enemies:
        # Skip dead enemies
        if enemy["health"] <= 0:
            continue
        
        # Calculate health percentage to determine behavior
        health_percentage = enemy["health"] / enemy["max_health"]
        
        # Calculate distance to player
        dx = self.player["x"] - enemy["x"]
        dy = self.player["y"] - enemy["y"]
        distance = math.sqrt(dx**2 + dy**2)
        
        # Get centers for calculations
        player_center_x = self.player["x"] + self.player["width"] / 2
        player_center_y = self.player["y"] + self.player["height"] / 2
        enemy_center_x = enemy["x"] + enemy["width"] / 2
        enemy_center_y = enemy["y"] + enemy["height"] / 2
        
        # Check if line of sight to player is clear
        line_of_sight = True  # Assume true and then check for obstructions
        for wall in self.walls:
            # Check if the line from enemy to player intersects with this wall
            if self.line_intersects_rect(
                enemy_center_x, enemy_center_y,
                player_center_x, player_center_y,
                wall["x"], wall["y"], wall["width"], wall["height"]
            ):
                line_of_sight = False
                break
        
        # Health regeneration when not shooting
        # Calculate time since last attack
        time_since_last_attack = current_time - enemy.get("last_attack_time", 0) 
        
        # Only regenerate if:
        # 1. It's been at least 2 seconds since last attack 
        # 2. Health is below max health
        # 3. Preferably when not in line of sight (faster regeneration when hidden)
        if time_since_last_attack > 2000 and enemy["health"] < enemy["max_health"]:
            # Initialize last_regen_time if it doesn't exist
            if "last_regen_time" not in enemy:
                enemy["last_regen_time"] = current_time - 100  # Set slightly behind for immediate small regen
            
            # Calculate time since last regeneration
            time_since_last_regen = current_time - enemy.get("last_regen_time", 0)
            
            # Convert to seconds for the regen calculation
            seconds_elapsed = time_since_last_regen / 1000
            
            # Initialize regen_rate if it doesn't exist (fallback)
            if "regen_rate" not in enemy:
                enemy["regen_rate"] = 0.5 if not enemy.get("is_boss", False) else 1.0
            
            # Calculate regeneration amount (faster when hiding)
            regen_multiplier = 0.5 if line_of_sight else 1.0  # Regenerate faster when hidden
            regen_amount = enemy["regen_rate"] * seconds_elapsed * regen_multiplier
            
            # Only apply regeneration if there's a meaningful amount
            if regen_amount > 0.001:  # Ensure there's actual healing to apply
                # Apply the health regeneration
                old_health = enemy["health"]
                enemy["health"] = min(enemy["max_health"], enemy["health"] + regen_amount)
                actual_healing = enemy["health"] - old_health
                
                # Update last regeneration time
                enemy["last_regen_time"] = current_time
                
                # Visual effect for regeneration (if significant healing occurred)
                if actual_healing > 0.5:  # Only show for noticeable healing
                    # Store healing indicators if not already present
                    if not hasattr(self, 'healing_indicators'):
                        self.healing_indicators = []
                    
                    # Show a heart or + symbol for healing with low chance to avoid spam
                    if random.random() < 0.1:  # 10% chance per significant healing
                        self.healing_indicators.append({
                            "x": enemy["x"] + enemy["width"] / 2,
                            "y": enemy["y"] - 15,
                            "text": "+",
                            "color": (50, 255, 50),  # Green for healing
                            "time_created": current_time,
                            "lifespan": 800  # milliseconds
                        })
        
        # Determine behavior based on health
        is_retreating = health_percentage < 0.5  # Retreat if below 50% health
        
        # Bosses are more aggressive and retreat only at lower health
        if enemy.get("is_boss", False):
            is_retreating = health_percentage < 0.3  # Bosses retreat only below 30% health
        
        # If enemy is at high health or is a boss with decent health, be aggressive
        if not is_retreating:
            # AGGRESSIVE BEHAVIOR - Attack player
            
            # Update enemy direction to face player (for aiming)
            target_direction = math.degrees(math.atan2(dy, dx))
            
            # Smooth rotation for more natural movement
            angle_diff = (target_direction - enemy["direction"] + 180) % 360 - 180
            rotation_speed = 5  # degrees per frame
            if abs(angle_diff) > rotation_speed:
                if angle_diff > 0:
                    enemy["direction"] += rotation_speed
                else:
                    enemy["direction"] -= rotation_speed
            else:
                enemy["direction"] = target_direction
            
            # Keep direction in 0-360 range
            enemy["direction"] = enemy["direction"] % 360
            
            # If player is within attack range and we have line of sight, shoot
            if distance <= enemy["range"] and line_of_sight:
                # Regular attack logic
                time_since_last_attack = current_time - enemy["last_attack_time"]
                
                # Only shoot if it's been long enough since last attack
                attack_interval = 1000 / enemy["attack_speed"]
                if time_since_last_attack > attack_interval:
                    enemy["last_attack_time"] = current_time
                    
                    # Play enemy shoot sound
                    self.play_sound("shoot")
                    
                    # Calculate bullet starting position
                    angle_rad = math.radians(enemy["direction"])
                    bullet_x = enemy["x"] + enemy["width"] / 2 + math.cos(angle_rad) * 30
                    bullet_y = enemy["y"] + enemy["height"] / 2 + math.sin(angle_rad) * 30
                    
                    # For bosses, use special attack patterns
                    if enemy.get("is_boss", False):
                        # Check if it's time for a special attack
                        time_since_special = current_time - enemy.get("last_special_attack_time", 0)
                        
                        if time_since_special > enemy["special_cooldown"]:
                            # It's time for a special attack!
                            enemy["last_special_attack_time"] = current_time
                            
                            # Different attack patterns for bosses
                            if enemy["attack_pattern"] == "spread":
                                # Spread shot - 5 bullets in a spread pattern
                                for angle_offset in [-30, -15, 0, 15, 30]:
                                    spread_angle = enemy["direction"] + angle_offset
                                    spread_rad = math.radians(spread_angle)
                                    spread_x = enemy["x"] + enemy["width"] / 2 + math.cos(spread_rad) * 30
                                    spread_y = enemy["y"] + enemy["height"] / 2 + math.sin(spread_rad) * 30
                                    
                                    self.create_bullet(
                                        spread_x, spread_y,
                                        spread_angle,
                                        enemy["damage"],
                                        False,
                                        enemy["color"]
                                    )
                            
                            elif enemy["attack_pattern"] == "burst":
                                # Burst fire - multiple bullets in quick succession
                                for _ in range(3):
                                    # Add slight random variation to each shot
                                    burst_angle = enemy["direction"] + random.uniform(-5, 5)
                                    burst_rad = math.radians(burst_angle)
                                    burst_x = enemy["x"] + enemy["width"] / 2 + math.cos(burst_rad) * 30
                                    burst_y = enemy["y"] + enemy["height"] / 2 + math.sin(burst_rad) * 30
                                    
                                    self.create_bullet(
                                        burst_x, burst_y,
                                        burst_angle,
                                        enemy["damage"],
                                        False,
                                        enemy["color"]
                                    )
                            
                            elif enemy["attack_pattern"] == "sniper":
                                # Sniper shot - single powerful bullet
                                self.create_bullet(
                                    bullet_x, bullet_y,
                                    enemy["direction"],
                                    enemy["damage"] * 2,  # Double damage
                                    False,
                                    (255, 255, 0)  # Yellow bullet for sniper shot
                                )
                        else:
                            # Regular attack for bosses between special attacks
                            self.create_bullet(
                                bullet_x, bullet_y,
                                enemy["direction"],
                                enemy["damage"],
                                False,
                                enemy["color"]
                            )
                    else:
                        # Regular enemy - just create a single bullet
                        self.create_bullet(
                            bullet_x, bullet_y,
                            enemy["direction"],
                            enemy["damage"],
                            False,
                            enemy["color"]
                        )
            
            # Move towards player with smart positioning
            # Calculate movement vector towards player
            angle_rad = math.radians(enemy["direction"])
            move_speed = enemy["speed"]
            
            # Determine optimal shooting distance based on enemy type
            optimal_distance = enemy["range"] * 0.7  # Stay at 70% of maximum range
            
            # For bosses, maintain even more distance to make them harder to hit
            if enemy.get("is_boss", False):
                optimal_distance = enemy["range"] * 0.8  # Stay at 80% of max range for bosses
            
            # Adjust movement based on current distance to player
            if distance > optimal_distance + 20:  # Too far, move closer
                # Move toward player
                new_x = enemy["x"] + math.cos(angle_rad) * move_speed
                new_y = enemy["y"] + math.sin(angle_rad) * move_speed
            elif distance < optimal_distance - 20:  # Too close, back away
                # Move away from player
                retreat_angle_rad = math.radians((enemy["direction"] + 180) % 360)
                new_x = enemy["x"] + math.cos(retreat_angle_rad) * (move_speed * 0.7)  # Move away slower
                new_y = enemy["y"] + math.sin(retreat_angle_rad) * (move_speed * 0.7)
            else:
                # At good shooting distance, strafe sideways to make harder target
                strafe_direction = 1 if random.random() < 0.5 else -1  # Randomly go left or right
                strafe_angle_rad = math.radians((enemy["direction"] + strafe_direction * 90) % 360)
                
                # If enemy has an ID, use it to make strafing more consistent
                if "id" in enemy:
                    # Use ID to determine strafe direction (even IDs go right, odd go left)
                    strafe_direction = 1 if enemy["id"] % 2 == 0 else -1
                    strafe_angle_rad = math.radians((enemy["direction"] + strafe_direction * 90) % 360)
                
                # Strafe at reduced speed
                new_x = enemy["x"] + math.cos(strafe_angle_rad) * (move_speed * 0.5)
                new_y = enemy["y"] + math.sin(strafe_angle_rad) * (move_speed * 0.5)
                
                # Occasionally stop to aim better (10% chance while at optimal range)
                if random.random() < 0.1:
                    new_x = enemy["x"]
                    new_y = enemy["y"]
                    
        else:
            # RETREAT BEHAVIOR - Run away and find cover
            
            # Initialize variables to find the best retreat direction
            best_hiding_spot = None
            best_hiding_distance = float('inf')
            
            # Try to find a wall to hide behind
            for wall in self.walls:
                wall_center_x = wall["x"] + wall["width"] / 2
                wall_center_y = wall["y"] + wall["height"] / 2
                
                # Calculate vector from player to wall center
                player_to_wall_x = wall_center_x - player_center_x
                player_to_wall_y = wall_center_y - player_center_y
                player_to_wall_dist = math.sqrt(player_to_wall_x**2 + player_to_wall_y**2)
                
                # Calculate vector from enemy to wall center
                enemy_to_wall_x = wall_center_x - enemy_center_x
                enemy_to_wall_y = wall_center_y - enemy_center_y
                enemy_to_wall_dist = math.sqrt(enemy_to_wall_x**2 + enemy_to_wall_y**2)
                
                # Only consider walls that are:
                # 1. Relatively far from player
                # 2. Can provide cover (break line of sight)
                # 3. Not too far from the enemy
                if (player_to_wall_dist > 200 and  # Wall is far from player
                    enemy_to_wall_dist < 300 and   # Wall is not too far from enemy
                    not line_of_sight):            # Wall can provide cover
                    
                    # Check if this wall is better than previously found walls
                    if enemy_to_wall_dist < best_hiding_distance:
                        best_hiding_spot = (wall_center_x, wall_center_y)
                        best_hiding_distance = enemy_to_wall_dist
            
            # If we found a suitable wall to hide behind
            if best_hiding_spot:
                # Calculate direction towards hiding spot
                hide_dx = best_hiding_spot[0] - enemy_center_x
                hide_dy = best_hiding_spot[1] - enemy_center_y
                retreat_direction = math.degrees(math.atan2(hide_dy, hide_dx))
                
                # Set enemy direction to face the hiding spot
                enemy["direction"] = retreat_direction
                
                # Calculate movement with a boost to retreat speed
                retreat_speed_multiplier = 1.2  # Retreat 20% faster than normal
                angle_rad = math.radians(retreat_direction)
                move_speed = enemy["speed"] * retreat_speed_multiplier
                new_x = enemy["x"] + math.cos(angle_rad) * move_speed
                new_y = enemy["y"] + math.sin(angle_rad) * move_speed
                
            else:
                # No good hiding spot found, just run away from player
                retreat_direction = (math.degrees(math.atan2(dy, dx)) + 180) % 360
                
                # Set enemy direction away from player
                enemy["direction"] = retreat_direction
                
                # Retreat movement with speed boost
                retreat_speed_multiplier = 1.2  # Retreat 20% faster than normal
                angle_rad = math.radians(retreat_direction)
                move_speed = enemy["speed"] * retreat_speed_multiplier
                new_x = enemy["x"] + math.cos(angle_rad) * move_speed
                new_y = enemy["y"] + math.sin(angle_rad) * move_speed
            
            # Every so often, shoot back while retreating (if we have line of sight)
            if line_of_sight and random.random() < 0.1 and distance <= enemy["range"]:  # 10% chance to fire while retreating
                current_time = pygame.time.get_ticks()
                time_since_last_attack = current_time - enemy["last_attack_time"]
                
                # Only shoot if it's been long enough since last attack
                attack_interval = 1000 / enemy["attack_speed"]
                if time_since_last_attack > attack_interval * 1.5:  # Slower attack rate while retreating
                    # Temporarily face player to shoot
                    original_direction = enemy["direction"]
                    enemy["direction"] = math.degrees(math.atan2(dy, dx))
                    
                    # Play enemy shoot sound
                    self.play_sound("shoot")
                    
                    # Calculate bullet starting position
                    shoot_angle_rad = math.radians(enemy["direction"])
                    bullet_x = enemy["x"] + enemy["width"] / 2 + math.cos(shoot_angle_rad) * 30
                    bullet_y = enemy["y"] + enemy["height"] / 2 + math.sin(shoot_angle_rad) * 30
                    
                    # Create bullet (basic attack only while retreating)
                    self.create_bullet(
                        bullet_x, bullet_y,
                        enemy["direction"],
                        enemy["damage"] * 0.7,  # Reduced damage while retreating
                        False,
                        enemy["color"]
                    )
                    
                    # Reset direction back to retreat direction
                    enemy["direction"] = original_direction
                    enemy["last_attack_time"] = current_time
            
        # Check for wall collisions
        collision_with_wall = False
        for wall in self.walls:
            if "collision_width" in enemy:
                if (new_x + enemy["collision_offset_x"] < wall["x"] + wall["width"] and
                    new_x + enemy["collision_offset_x"] + enemy["collision_width"] > wall["x"] and
                    new_y + enemy["collision_offset_y"] < wall["y"] + wall["height"] and
                    new_y + enemy["collision_offset_y"] + enemy["collision_height"] > wall["y"]):
                    collision_with_wall = True
                    break
            else:
                if (new_x < wall["x"] + wall["width"] and
                    new_x + enemy["width"] > wall["x"] and
                    new_y < wall["y"] + wall["height"] and
                    new_y + enemy["height"] > wall["y"]):
                    collision_with_wall = True
                    break
        
        # Only move if no collision with walls
        if not collision_with_wall:
            enemy["x"] = new_x
            enemy["y"] = new_y
            
        # If enemy is at low health, occasionally add a visual indicator
        if is_retreating and random.random() < 0.05:  # 5% chance per frame
            # Store retreat indicators if not already present
            if not hasattr(self, 'retreat_indicators'):
                self.retreat_indicators = []
                
            # Add retreat visual indicator (e.g., "!!" or "Retreating!")
            self.retreat_indicators.append({
                "x": enemy["x"] + enemy["width"] / 2,
                "y": enemy["y"] - 15,
                "text": "!!",
                "color": (255, 100, 100),
                "time_created": pygame.time.get_ticks(),
                "lifespan": 500  # milliseconds
            })
    
    # Second pass - handle enemy-to-enemy collisions and separation
    for i, enemy1 in enumerate(self.enemies):
        # Skip dead enemies
        if enemy1["health"] <= 0:
            continue
            
        # Store total repulsion forces for this enemy
        repulsion_x = 0
        repulsion_y = 0
        collisions_detected = 0
        
        # Check collisions with all other enemies
        for j, enemy2 in enumerate(self.enemies):
            # Skip if same enemy or if enemy2 is dead
            if i == j or enemy2["health"] <= 0:
                continue
                
            # Calculate centers
            enemy1_center_x = enemy1["x"] + enemy1["width"] / 2
            enemy1_center_y = enemy1["y"] + enemy1["height"] / 2
            enemy2_center_x = enemy2["x"] + enemy2["width"] / 2
            enemy2_center_y = enemy2["y"] + enemy2["height"] / 2
            
            # Calculate distance between centers
            dx = enemy1_center_x - enemy2_center_x
            dy = enemy1_center_y - enemy2_center_y
            distance = math.sqrt(dx**2 + dy**2)
            
            # Calculate minimum distance needed to prevent overlap
            if "collision_width" in enemy1:
                min_distance = (enemy1["collision_width"] + enemy2.get("collision_width", enemy2["width"])) / 2
            else:
                min_distance = (enemy1["width"] + enemy2.get("collision_width", enemy2["width"])) / 2
            
            # If overlapping
            if distance < min_distance:
                # Calculate unit vector of repulsion
                if distance > 0:  # Avoid division by zero
                    dx = dx / distance
                    dy = dy / distance
                else:
                    # If directly on top of each other, choose a random direction
                    angle = random.uniform(0, 2 * math.pi)
                    dx = math.cos(angle)
                    dy = math.sin(angle)
                
                # Calculate repulsion force (stronger when closer)
                overlap_amount = min_distance - distance
                repulsion_force = overlap_amount * 0.5  # Adjust factor for faster/slower separation
                
                # Add to total repulsion for this enemy
                repulsion_x += dx * repulsion_force
                repulsion_y += dy * repulsion_force
                collisions_detected += 1
        
        # Apply combined repulsion forces if any collisions were detected
        if collisions_detected > 0:
            # Apply a slightly larger force for bosses (they're more forceful)
            force_multiplier = 1.5 if enemy1.get("is_boss", False) else 1.0
            
            # Add repulsion to position (with collision check for walls)
            new_x = enemy1["x"] + repulsion_x * force_multiplier
            new_y = enemy1["y"] + repulsion_y * force_multiplier
            
            # Check wall collisions for the repulsion movement
            wall_collision = False
            for wall in self.walls:
                if "collision_width" in enemy1:
                    if (new_x + enemy1["collision_offset_x"] < wall["x"] + wall["width"] and
                        new_x + enemy1["collision_offset_x"] + enemy1["collision_width"] > wall["x"] and
                        new_y + enemy1["collision_offset_y"] < wall["y"] + wall["height"] and
                        new_y + enemy1["collision_offset_y"] + enemy1["collision_height"] > wall["y"]):
                        wall_collision = True
                        break
                else:
                    if (new_x < wall["x"] + wall["width"] and
                        new_x + enemy1["width"] > wall["x"] and
                        new_y < wall["y"] + wall["height"] and
                        new_y + enemy1["height"] > wall["y"]):
                        wall_collision = True
                        break
            
            # Only apply repulsion if it doesn't cause a wall collision
            if not wall_collision:
                enemy1["x"] = new_x
                enemy1["y"] = new_y

def line_intersects_rect(self, x1, y1, x2, y2, rx, ry, rw, rh):
    """Check if line from (x1,y1) to (x2,y2) intersects with rectangle (rx,ry,rw,rh)"""
    # Convert rectangle to its four line segments
    lines = [
        (rx, ry, rx + rw, ry),         # Top
        (rx, ry + rh, rx + rw, ry + rh), # Bottom
        (rx, ry, rx, ry + rh),         # Left
        (rx + rw, ry, rx + rw, ry + rh)  # Right
    ]
    
    # Check if the line intersects with any of the rectangle's sides
    for lx1, ly1, lx2, ly2 in lines:
        if self.line_intersection(x1, y1, x2, y2, lx1, ly1, lx2, ly2):
            return True
    
    # Also check if either endpoint is inside the rectangle
    if (rx <= x1 <= rx + rw and ry <= y1 <= ry + rh) or (rx <= x2 <= rx + rw and ry <= y2 <= ry + rh):
        return True
        
    return False

def line_intersection(self, x1, y1, x2, y2, x3, y3, x4, y4):
    """Check if two line segments intersect"""
    # Calculate determinants
    den = (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)
    
    # Lines are parallel if den is zero
    if den == 0:
        return False
        
    ua = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / den
    ub = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / den
    
    # Return true if line segments intersect
    return 0 <= ua <= 1 and 0 <= ub <= 1

def update_player_health_regeneration(self):
    """Regenerate player health when not shooting"""
    # Check if player exists (game has started)
    if self.player is None:
        return
        
    current_time = pygame.time.get_ticks()
    
    # We use the player's last_attack_time to determine if player is shooting
    # If the player shot recently, don't regenerate health
    if "last_attack_time" in self.player:
        time_since_last_shot = current_time - self.player["last_attack_time"]
        
        # Only start regenerating if player hasn't shot for at least 1 second
        if time_since_last_shot >= 1000:
            # Initialize regen timer if it doesn't exist
            if 'last_regen_time' not in self.player:
                self.player['last_regen_time'] = current_time
            
            # Calculate time since last regeneration
            time_since_last_regen = current_time - self.player['last_regen_time']
            
            # Only regenerate health every 1000ms (1 second)
            if time_since_last_regen >= 1000:
                self.player['last_regen_time'] = current_time
                
                # Only regenerate if health is below max
                if self.player['health'] < self.player['max_health']:
                    # Regenerate 5% of max health per second
                    regen_amount = max(1, int(self.player['max_health'] * 0.05))
                    self.player['health'] = min(self.player['max_health'], self.player['health'] + regen_amount)
    else:
        # If last_attack_time doesn't exist yet, initialize it
        self.player["last_attack_time"] = current_time

def update_player_aim(self):
    """Update player direction to aim at the closest enemy"""
    if not self.player or not self.enemies:
        return
    
    # Find the closest enemy
    closest_enemy = None
    closest_distance = float('inf')
    
    player_center_x = self.player["x"] + self.player["width"] / 2
    player_center_y = self.player["y"] + self.player["height"] / 2
    
    for enemy in self.enemies:
        enemy_center_x = enemy["x"] + enemy["width"] / 2
        enemy_center_y = enemy["y"] + enemy["height"] / 2
        
        dx = enemy_center_x - player_center_x
        dy = enemy_center_y - player_center_y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance < closest_distance:
            closest_distance = distance
            closest_enemy = enemy
    
    # Update player direction to aim at the closest enemy
    if closest_enemy:
        enemy_center_x = closest_enemy["x"] + closest_enemy["width"] / 2
        enemy_center_y = closest_enemy["y"] + closest_enemy["height"] / 2
        
        dx = enemy_center_x - player_center_x
        dy = enemy_center_y - player_center_y
        
        # Calculate angle in degrees (0 = right, 90 = down, 180 = left, 270 = up)
        self.player["direction"] = math.degrees(math.atan2(dy, dx))

# Register all functions to the PyBrawl class
def setup(PyBrawl):
    """Set up the game mechanics by adding all functions to the PyBrawl class."""
    # Map and Enemy spawning
    PyBrawl.generate_map = generate_map
    PyBrawl.add_bushes = add_bushes  # New function
    PyBrawl.is_map_fully_connected = is_map_fully_connected  # New function
    PyBrawl.spawn_enemies = spawn_enemies
    PyBrawl.create_bullet = create_bullet
    
    # Update functions
    PyBrawl.update_gameplay = update_gameplay
    PyBrawl.update_bullets = update_bullets
    PyBrawl.update_enemies = update_enemies
    PyBrawl.update_player_health_regeneration = update_player_health_regeneration
    PyBrawl.update_player_aim = update_player_aim
    
    # Add line intersection utility methods for improved enemy AI
    PyBrawl.line_intersects_rect = line_intersects_rect
    PyBrawl.line_intersection = line_intersection
    
    # Add spawn_boss as a standalone function
    PyBrawl.spawn_boss = spawn_boss
