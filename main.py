# Author : Adrien Pillou
# Date : 21/11/2020
# Description : Breakout game made using pygame

import pygame
import os
import sys
import random
import time
import webbrowser
import math
from enum import Enum, auto
from utils import *

# Setting the current dir to this file parent directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

   #     #####   #####  ####### #######  #####  
  # #   #     # #     # #          #    #     # 
 #   #  #       #       #          #    #       
#     #  #####   #####  #####      #     #####  
#######       #       # #          #          # 
#     # #     # #     # #          #    #     # 
#     #  #####   #####  #######    #     #####  
                                                 
# Mixer setup
pygame.mixer.init(44100, -16, 2, 1024)
sounds = dict()
sounds['bounce'] = pygame.mixer.Sound("./assets/sounds/footstep_concrete_003.ogg")
sounds['brique'] = pygame.mixer.Sound("./assets/sounds/impactMetal_heavy_003.ogg")
sounds['break'] = pygame.mixer.Sound("./assets/sounds/footstep_grass_003.ogg")
sounds['select'] = pygame.mixer.Sound("./assets/sounds/drop_003.ogg")
sounds['confirm'] = pygame.mixer.Sound("./assets/sounds/confirmation_001.ogg")

# Loading the font
pygame.font.init()
roboto_regular = Font("./assets/fonts/Roboto-Regular.ttf", 24)
roboto_bold = Font("./assets/fonts/Roboto-Bold.ttf", 24)

# Levels dictionnary
levels = dict()
levels[0] = "./assets/lvl0.csv"
levels[1] = "./assets/lvl1.csv"
levels[2] = "./assets/lvl2.csv"
levels[3] = "./assets/lvl3.csv"
levels[4] = "./assets/lvl4.csv"
levels[5] = "./assets/lvl5.csv"
level_index = 0

 #####  ####### ####### ####### ### #     #  #####   #####  
#     # #          #       #     #  ##    # #     # #     # 
#       #          #       #     #  # #   # #       #       
 #####  #####      #       #     #  #  #  # #  ####  #####  
      # #          #       #     #  #   # # #     #       # 
#     # #          #       #     #  #    ## #     # #     # 
 #####  #######    #       #    ### #     #  #####   #####  
                                                             
TARGET_FPS = 60
WIDTH = 800 # Screen height
HEIGHT = 600 # Screen width
TITLE = "Brique Breaker"
FULLSCREEN = False 
RUNNING = True
VOLUME = .8
GAME_RESOLUTION = (WIDTH, HEIGHT) # Base resolution tuple


 #####  #       ####### ######     #    #          #     #    #    ######   #####  
#     # #       #     # #     #   # #   #          #     #   # #   #     # #     # 
#       #       #     # #     #  #   #  #          #     #  #   #  #     # #       
#  #### #       #     # ######  #     # #          #     # #     # ######   #####  
#     # #       #     # #     # ####### #           #   #  ####### #   #         # 
#     # #       #     # #     # #     # #            # #   #     # #    #  #     # 
 #####  ####### ####### ######  #     # #######       #    #     # #     #  #####  
                                                                                    
clock = pygame.time.Clock()
playing = False
lives = 5
score = 0

# Game state enum
class GameState(Enum):
    main = auto()
    play = auto()
    pause = auto()

state = GameState.main

 #####  ####### ####### #     # ######  
#     # #          #    #     # #     # 
#       #          #    #     # #     # 
 #####  #####      #    #     # ######  
      # #          #    #     # #       
#     # #          #    #     # #       
 #####  #######    #     #####  #       
                                         
pygame.init()
monitor_definition = (pygame.display.Info().current_w, pygame.display.Info().current_h)
os.environ['SDL_VIDEO_CENTERED'] = '1'
os.environ['SDL_VIDEODRIVER'] = 'directx'
last_time = time.time()
dt=1/TARGET_FPS
window = pygame.display.set_mode(GAME_RESOLUTION, pygame.DOUBLEBUF | pygame.HWSURFACE)
surface = pygame.surface.Surface(GAME_RESOLUTION)
icon = pygame.image.load(os.path.join('assets', 'icon32.png')) 
pygame.display.set_icon(icon) # Custom window icon
pygame.display.set_caption(TITLE)

shaker = ScreenShake(0, 0, 0)

gameobjects = []
bricks = []

# Adding the player
player = Player("player", (WIDTH/2-32, HEIGHT-32), (76, 24))
gameobjects.append(player)

# Adding the ball
ball = Ball("ball", (WIDTH/2, HEIGHT-64), (16, 16))
ball.set_z_order(100)
gameobjects.append(ball)
trail = Trail("ball trail", ball.get_rect().center, -1, 1, -1, .05)
gameobjects.append(trail)

lives_label = Text("lives", (0,0), "0", 24)
lives_label.set_font(Font("./assets/fonts/Roboto-Bold.ttf", 24))
lives_label.set_color((0, 0, 0))
gameobjects.append(lives_label)

score_label = Text("score", (WIDTH//2, HEIGHT//2), "0", 256)
score_label.set_font(Font("./assets/fonts/Roboto-Bold.ttf", 256))
score_label.set_color((50, 50, 50))
score_label.set_z_order(-1)
gameobjects.append(score_label)

tilemap = Tilemap()

######  ####### #######  #####  
#     # #       #       #     # 
#     # #       #       #       
#     # #####   #####    #####  
#     # #       #             # 
#     # #       #       #     # 
######  ####### #        #####  
                                 
def place_bricks():
    # Adding the bricks (10x10 grid tilemap)
    padding = 4
    brick_width = 64
    brick_height = 32
    top_offset = 4
    group_width = tilemap.cols*(brick_width+padding)
    for j in range(tilemap.rows):
        for i in range(tilemap.cols):
            tile_key = int(tilemap.get_tile_key((i, j)))
            if tile_key >= 1:
                new_brick = Brick(f"Brick-{i}:{j}", (WIDTH/2-group_width/2+i*(brick_width+padding), top_offset+j*(brick_height+padding)), (brick_width, brick_height))
                new_brick.set_lives(tile_key)
                gameobjects.append(new_brick)
                bricks.append(new_brick)

def manage_inputs():
    keys = pygame.key.get_pressed()
    # Player movements
    direction = 0
    movement = player.speed*dt
    if keys[pygame.K_RIGHT]:
        direction = 1    
    elif keys[pygame.K_LEFT]:
        direction = -1
    elif keys[pygame.K_SPACE]:
        global playing
        if(not playing):
            playing = True
            ball.set_velocity(((random.choice([-1, 1]), -1)))
    movement*=direction
    player.set_position(Vector2(player.position.x + movement, player.position.y))
    if(player.position.x<0):
        player.position.x = 0
    if(player.position.x + player.size.x>=WIDTH):
        player.position.x = WIDTH-player.size.x

# Moving to a level
def goto_level(index):
    remove_bricks()
    if (index>=len(levels)):
        index = 0
        goto_level(0)
    else:
        global playing
        tilemap.set_file(levels[index])
        player.position = Vector2(WIDTH/2-player.size.x/2, HEIGHT-32)
        playing = False
        ball.velocity = Vector2().zero()
        ball.position = player.position + Vector2(player.size.x/2 - ball.size.x/2,- (ball.size.y+player.size.y/2))
        place_bricks()

# Remove all bricks from the screen
def remove_bricks():
    global bricks, gameobjects
    for brick in bricks:
        if brick in gameobjects:
            gameobjects.remove(brick)
    bricks = []

# Handling ball behaviour
def update_ball(ball_object):
    global playing, lives, score
    if(not playing):
        ball.position = player.position + Vector2(player.size.x/2 - ball.size.x/2,- (ball.size.y+player.size.y/2))
    
    # Update the trail position
    trail.position = ball.get_rect().center

    # Screen Borders
    if(ball.position.x+ball.size.x>=WIDTH):
        ball.get_rect().right = WIDTH-1
        ball.velocity.x*=-1
        play_sound('bounce')
        shaker.set_properties(5, 10, 0.8)
    if (ball.position.x<0):
        ball.get_rect().left = 0
        ball.velocity.x*=-1
        play_sound('bounce')
        shaker.set_properties(5, 10, 0.8)
    if(ball.position.y<0):
        ball.get_rect().top = 0
        ball.velocity.y*=-1
        play_sound('bounce')
        shaker.set_properties(5, 10, 0.8)
    
    # Collision with the player paddle
    if check_collision(ball, player):
        # Handling bounce angle
        a = Vector2(player.get_rect().centerx, player.get_rect().centery)
        b = Vector2(ball.get_rect().centerx, ball.get_rect().centery)
        d = a-b
        x_angle = d.x/(player.size.x*.5)
        max_slope = .75
        if(x_angle>max_slope): x_angle = max_slope
        elif(x_angle<-max_slope):x_angle = -max_slope
        y_angle = 1-abs(x_angle)
        side = get_ball_collision_side(player.get_rect())
        
        if side=="ABOVE":
            ball.velocity.x = -x_angle
            ball.velocity.y = -y_angle
            ball.get_rect().bottom = player.get_rect().top - 1
        elif side =="RIGHT":
            ball.velocity.x *= -1
            ball.get_rect().left = player.get_rect().right + 1
        elif side =="LEFT":
            ball.velocity.x *= -1
            ball.get_rect().right = player.get_rect().left - 1
        ball.velocity = ball.velocity.normalized()
        shaker.set_properties(8, 10, 0.8)
        play_sound('bounce')
        
    if(ball.get_rect().centery >= HEIGHT + 32):
        lives-=1
        if lives == 0:
            remove_bricks()
            goto_level(0)
            lives = 5
        playing = False
        ball.position = player.position + Vector2(player.size.x/2 - ball.size.x/2,- (ball.size.y+player.size.y/2))
        ball.velocity = Vector2().zero()
    
    # Handle collisions with the bricks
    for brick in bricks:
        if ball.get_rect().colliderect(brick.get_rect()):
            side = get_ball_collision_side(brick.get_rect())
            if side == "ABOVE":
                ball.velocity.y*=-1
                ball.get_rect().bottom = brick.get_rect().top - 3
            elif side == "UNDER":
                ball.velocity.y*=-1
                ball.get_rect().top = brick.get_rect().bottom + 3
            elif side =="RIGHT":
                ball.velocity.x*=-1
                ball.get_rect().left = brick.get_rect().right + 3
            elif side == "LEFT":
                ball.velocity.x*=-1
                ball.get_rect().right = brick.get_rect().left - 3  
            brick.lives-=1
            
            if(brick.lives <= 0):
                # Playing sound effect
                play_sound('break', 1)

                # Updating the score
                score += 10 

                # Adding particles effect
                emitter = Emitter("emitter", brick.get_rect().center, 5, 64, 1, 0)
                emitter.set_z_order(10)
                emitter.base_color = brick.color
                
                time.sleep(0.03)
                # Impact circle particle effect
                circle = CircleEmitter("circle effect", brick.get_rect().center, 3, 1, 1, 0)
                circle.base_color = brick.color
                gameobjects.append(circle)

                # Screen shake effect
                shaker.set_properties(12, 10, 0.95)

                # Destroy the brick
                gameobjects.append(emitter)
                gameobjects.remove(brick)
                bricks.remove(brick)
            else:
                play_sound('brique')
                # Screen shake effect
                shaker.set_properties(8, 10, 0.8)

# Check collision between two objects using their Rects
def check_collision(a:GameObject, b:GameObject):
    if a.get_rect().colliderect(b.get_rect()):
        return True
    return False

# Return the collision side of a brick
def get_ball_collision_side(other:pygame.Rect, threshold=20):
    b = ball.get_rect()
    if abs(other.bottom - b.top) < threshold and ball.velocity.y<0:
        return "UNDER"
    elif abs(other.top - b.bottom) < threshold and ball.velocity.y>0:
        return "ABOVE"
    elif abs(other.right - b.left) < threshold and ball.velocity.x<0:
        return "RIGHT"
    elif abs(other.left - b.right) < threshold and ball.velocity.x>0:
        return "LEFT"
    pass     

# Playing a sound effect
def play_sound(sound_id, volume=1):
    if sound_id is None:
        print("Cannot play sound : sound_id is None !")
        return 
    if not sound_id in sounds:
        print(f"Sound effect {sound_id} does not exists !")
        return
    sound_effect = sounds.get(sound_id)
    sound_effect.play()
    sound_effect.set_volume(volume * VOLUME)

# Main menu loop
def main_menu():
    global state
    state = GameState.main
    menu = Menu("main menu", (WIDTH//2, HEIGHT//2), (600, 400))
    running = True
    gameobjects.append(menu)

    play_button = Button("play", (WIDTH//2, HEIGHT//2-34), (300, 32))
    play_button.set_label("PLAY")
    play_button.set_font(roboto_bold.get_font())
    menu.add_button(play_button)
    
    level_button = Button("level", (WIDTH//2, HEIGHT//2), (300, 32))
    level_button.set_label("LEVEL SELECTION")
    level_button.set_font(roboto_bold.get_font())
    menu.add_button(level_button)

    info_button = Button("info", (0, 0), (300, 32))
    info_button.set_label("INFO")
    info_button.set_font(roboto_bold.get_font())
    menu.add_button(info_button)

    quit_button = Button("quit", (WIDTH//2, HEIGHT//2+34), (300, 32))
    quit_button.set_label("QUIT")
    quit_button.set_font(roboto_bold.get_font())
    menu.add_button(quit_button)

    menu.set_layout()
    while running:
        update()
        draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    play_sound('confirm')
                    index = menu.get_selection()
                    if index[1] == 'play':
                        state = GameState.play
                        gameobjects.remove(menu)
                        running = False
                    elif index[1] == 'quit':
                        quit()
                    elif index[1] == 'info':
                        webbrowser.open("https://adrien-pillou.itch.io")
                if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                    play_sound('select')
            menu.receive_event(event)
        clock.tick(TARGET_FPS)

####### ######     #    #     # ####### #     # ####### ######  #    # 
#       #     #   # #   ##   ## #       #  #  # #     # #     # #   #  
#       #     #  #   #  # # # # #       #  #  # #     # #     # #  #   
#####   ######  #     # #  #  # #####   #  #  # #     # ######  ###    
#       #   #   ####### #     # #       #  #  # #     # #   #   #  #   
#       #    #  #     # #     # #       #  #  # #     # #    #  #   #  
#       #     # #     # #     # #######  ## ##  ####### #     # #    #                                                                  

# Use this for initialization
def start():
    goto_level(4)
    main_menu()

# Update is called once per frame
def update():
    if (state != GameState.play):
        return
    manage_inputs()
    if len(bricks) == 0: # Win condition
        global level_index
        level_index+=1
        goto_level(level_index)
    for gameobject in gameobjects:
        gameobject.update()
        if isinstance(gameobject, Ball):
            update_ball(gameobject)
        if isinstance(gameobject, Emitter):
            if not gameobject.is_emitting():
                gameobjects.remove(gameobject)
        if isinstance(gameobject, CircleEmitter):
            if not gameobject.is_emitting():
                gameobjects.remove(gameobject)

# Draw is call once per frame
def draw():
    global surface, screen, gameobjects
    
    # Clear the screen surface
    surface.fill((30, 30, 30)) 
    window.fill((30, 30, 30))

    # Placing interface elements
    lives_label.set_position(player.get_rect().center)
    lives_label.set_text(str(lives))

    score_label.set_text(str(score))
    
    # Drawing all gameobjects 
    gameobjects.sort(key=lambda x:x.z_order) # Ordering rendering queue
    for gameobject in gameobjects:
        gameobject.draw(surface)
    
    # Blitting the entire surface to the window
    shaker.shake(dt)
    window.blit(surface, shaker.offset)
    pygame.display.flip()

# Quit the game by closing the window
def quit():
    RUNNING = False
    pygame.display.quit()
    sys.exit()

 #####     #    #     # #######    #       ####### ####### ######  
#     #   # #   ##   ## #          #       #     # #     # #     # 
#        #   #  # # # # #          #       #     # #     # #     # 
#  #### #     # #  #  # #####      #       #     # #     # ######  
#     # ####### #     # #          #       #     # #     # #       
#     # #     # #     # #          #       #     # #     # #       
 #####  #     # #     # #######    ####### ####### ####### #       
                                                                    
start()
while RUNNING:
    dt = time.time() - last_time
    dt *= TARGET_FPS
    update()
    draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                main_menu()
            elif event.key == pygame.K_f:
                FULLSCREEN = not FULLSCREEN
                if FULLSCREEN:
                    surface = pygame.display.set_mode(GAME_RESOLUTION, pygame.FULLSCREEN)
                else:
                    surface = pygame.display.set_mode(GAME_RESOLUTION)
    last_time = time.time()
    clock.tick(TARGET_FPS)
