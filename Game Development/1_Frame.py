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
    


running = True
while running:
    dt = clock.tick(30)
    
    # 2. event (keyboard, mouse)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 

    # 3. Define character location
    
    # 4. Collision

    # 5. visualization on the screen
    screen.blit(background, (0, 0))
    screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))
    
   
    pygame.display.update()

pygame.quit()