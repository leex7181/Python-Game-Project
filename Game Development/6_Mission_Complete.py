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


# creating the ball (4 different size)
ball_images = [
    pygame.image.load(os.path.join(image_path, "balloon1.png")),
    pygame.image.load(os.path.join(image_path, "balloon2.png")),
    pygame.image.load(os.path.join(image_path, "balloon3.png")),
    pygame.image.load(os.path.join(image_path, "balloon4.png"))]


# initial speed of ball based on different size 
ball_speed_y = [-18, -15, -12, -9] # index values of 0, 1, 2, 3 

# balls
balls = []

# add largest ball size
balls.append({
    "pos_x" : 50, # x coordinate
    "pos_y" : 50, # y coordinate
    "img_idx" : 0, # image index of the ball
    "to_x": 3, # when x coordinate is -3 left, 3 right
    "to_y": -6, # y
    "init_spd_y": ball_speed_y[0]})# y initial speed

# removed weapon, saved ball info variable 
weapon_to_remove = -1
ball_to_remove = -1

# Font definition
game_font = pygame.font.Font(None, 40)
total_time = 100
start_ticks = pygame.time.get_ticks() # definition of initial time

# game ended message
# Time Over
# Mission Complete
# Game Over 
game_result = "Game Over"

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
    
    # define location of the ball
    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        ball_size = ball_images[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]

        # change location of the ball when touching screen width(bouncing effect)
        if ball_pos_x < 0 or ball_pos_x > screen_width - ball_width:
            ball_val["to_x"] = ball_val["to_x"] * -1

       # height location
        # bouncing the ball when touching the stage
        if ball_pos_y >= screen_height - stage_height - ball_height:
            ball_val["to_y"] = ball_val["init_spd_y"]
        else: # increasing speed elsewhere
            ball_val["to_y"] += 0.5

        ball_val["pos_x"] += ball_val["to_x"]
        ball_val["pos_y"] += ball_val["to_y"]

      # 4. collision

    # update character rect information
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        # update ball rect information
        ball_rect = ball_images[ball_img_idx].get_rect()
        ball_rect.left = ball_pos_x
        ball_rect.top = ball_pos_y

        # check collision between the ball and character 
        if character_rect.colliderect(ball_rect):
            running = False
            break

        # collision the ball and weapon 
        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_pos_x = weapon_val[0]
            weapon_pos_y = weapon_val[1]

            # updata weapon rect information 
            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_pos_x
            weapon_rect.top = weapon_pos_y

            # collision check
            if weapon_rect.colliderect(ball_rect):
                weapon_to_remove = weapon_idx # setting value to remove the weapon 
                ball_to_remove = ball_idx # setting value to remove the ball 

                # divide into smaller ball unless the ball is smallest one 
                if ball_img_idx < 3:
                    # bring current info about ball size 
                    ball_width = ball_rect.size[0]
                    ball_height = ball_rect.size[1]

                    # divided ball info 
                    small_ball_rect = ball_images[ball_img_idx + 1].get_rect()
                    small_ball_width = small_ball_rect.size[0]
                    small_ball_height = small_ball_rect.size[1]

                    # bouncing toward left 
                    balls.append({
                        "pos_x" : ball_pos_x + (ball_width / 2) - (small_ball_width / 2), # x coordinate of the ball
                        "pos_y" : ball_pos_y + (ball_height / 2) - (small_ball_height / 2), # y coordinate of the ball
                        "img_idx" : ball_img_idx + 1, # image index of the ball 
                        "to_x": -3, # x coordinnate, -3 -> left, 3 -> right
                        "to_y": -6, # y coordinate,
                        "init_spd_y": ball_speed_y[ball_img_idx + 1]})# initial speed of y coordinate 

                    # bouncing toward right
                    balls.append({
                        "pos_x" : ball_pos_x + (ball_width / 2) - (small_ball_width / 2), # x coordinate of the ball
                        "pos_y" : ball_pos_y + (ball_height / 2) - (small_ball_height / 2), # y coordinate of the ball
                        "img_idx" : ball_img_idx + 1, # image index of the ball 
                        "to_x": 3, # x coordinnate, -3 -> left, 3 -> right
                        "to_y": -6, # y coordinate,
                        "init_spd_y": ball_speed_y[ball_img_idx + 1]})# initial speed of y coordinate 

                break
        else: # continue game
            continue 
        break 

   

   # remove divided ball or weapon 
    if ball_to_remove > -1:
        del balls[ball_to_remove]
        ball_to_remove = -1

    if weapon_to_remove > -1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1

    # complete the mission if all ball is removed
    if len(balls) == 0:
        game_result = "Mission Complete"
        running = False

    #  5. visualization on the screen
    screen.blit(background, (0, 0))
    
    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

    for idx, val in enumerate(balls):
        ball_pos_x = val["pos_x"]
        ball_pos_y = val["pos_y"]
        ball_img_idx = val["img_idx"]
        screen.blit(ball_images[ball_img_idx], (ball_pos_x, ball_pos_y))

    screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))
    
    # elapsed time calculate
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000 # ms -> s
    timer = game_font.render("Time : {}".format(int(total_time - elapsed_time)), True, (102, 51, 153))
    screen.blit(timer, (10, 10))

    # if elapsed time over
    if total_time - elapsed_time <= 0:
        game_result = "Time Over"
        running = False

    pygame.display.update()

# game over message
msg = game_font.render(game_result, True, (102, 51, 153)) # purple
msg_rect = msg.get_rect(center=(int(screen_width / 2), int(screen_height/6)))
screen.blit(msg, msg_rect)
pygame.display.update()

# 2 sec delay
pygame.time.delay(2000)

pygame.quit()