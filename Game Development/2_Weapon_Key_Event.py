import os
import pygame
##############################################################
# Initializationn of fundamental setting
pygame.init()

# Size of screen
screen_width = 640 # size of width
screen_height = 480 # size of height
screen = pygame.display.set_mode((screen_width, screen_height))

# Screen title
pygame.display.set_caption("Bouncing The Ball With Lee")

# FPS
clock = pygame.time.Clock()
##############################################################

# 1. User game initialization (Background, Game image, Coordinate, Speed, Font......)
current_path = os.path.dirname(__file__) # Return current folder location
image_path = os.path.join(current_path, "images") # Return images folder location

# creatinng background
background = pygame.image.load(os.path.join(image_path, "background.png"))

# creating stage
stage = pygame.image.load(os.path.join(image_path, "stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1] # Use for placing character on the stage

 # creating character
character = pygame.image.load(os.path.join(image_path, "character.jpeg"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width / 2) - (character_width / 2)
character_y_pos = screen_height - character_height - stage_height

# character movement direction
character_to_x = 0

# character movement speed
character_speed = 5

# creating weapon
weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

# fire the weapon multiple time at once
weapons = []

# speed of the weapon
weapon_speed = 10

running = True
while running:
    dt = clock.tick(30)
    
    # 2. event (keyboard, mouse)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: # move character left
                character_to_x -= character_speed
            elif event.key == pygame.K_RIGHT: # move character right
                character_to_x += character_speed
            elif event.key == pygame.K_SPACE: # fire the weapon
                weapon_x_pos = character_x_pos + (character_width / 2) - (weapon_width / 2)
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos])
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0

    # 3.define location of character
    character_x_pos += character_to_x

    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    # weapon location
    # 100, 200 -> 180, 160, 140, ...
    # 500, 200 -> 180, 160, 140, ...
    weapons = [ [w[0], w[1] - weapon_speed] for w in weapons] # fire the weapon to upper direction

    # Get rid off weapon when passing over the screen
    weapons = [ [w[0], w[1]] for w in weapons if w[1] > 0]
    
    # 4. Collision

    # 5. visualization on the screen
    screen.blit(background, (0, 0))
    
    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

    screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))
    
    pygame.display.update()

pygame.quit()