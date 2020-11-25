import pygame
import os
import sys
import random
from utils import *

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Mixer setup
pygame.mixer.init(44100, -16, 2, 1024)
sounds = dict()
sounds['bounce'] = pygame.mixer.Sound("./assets/sounds/bounce.wav")
sounds['brique'] = pygame.mixer.Sound("./assets/sounds/brique.wav")

# Levels dictionnary
levels = dict()
levels[0] = "./assets/lvl0.csv"
levels[1] = "./assets/lvl1.csv"
levels[2] = "./assets/lvl2.csv"
levels[3] = "./assets/lvl3.csv"
levels[4] = "./assets/lvl4.csv"
level_index = 0

# Constants
TARGET_FPS = 60
WIDTH = 800 # Screen height
HEIGHT = 600 # Screen width
TITLE = "Brique Breaker"
FULLSCREEN = False 
VOLUME = 1
GAME_RESOLUTION = (WIDTH, HEIGHT) # Base resolution tuple

# Global Variables 
clock = pygame.time.Clock()
playing = False
lives = 3

# Window setup & settings
pygame.init()
monitor_definition = (pygame.display.Info().current_w, pygame.display.Info().current_h)
os.environ['SDL_VIDEO_CENTERED'] = '1'
surface = pygame.display.set_mode(GAME_RESOLUTION)
icon = pygame.image.load(os.path.join('assets', 'icon32.png')) 
pygame.display.set_icon(icon) # Custom window icon
pygame.display.set_caption(TITLE)

gameobjects = []
bricks = []

# Adding the player
player = Player("player1", (WIDTH/2-32, HEIGHT-32), (76, 16))
gameobjects.append(player)

# Adding the ball
ball = Ball("ball1", (WIDTH/2, HEIGHT-64), (16,16))
gameobjects.append(ball)

emitter = Emitter("emitter1", (WIDTH//2, HEIGHT//2), -1, 128, 1)
emitter.set_z_order(10)
print(emitter.z_order)
gameobjects.append(emitter)
tilemap = Tilemap()

def place_bricks():
    # Adding the bricks (10x10 grid)
    padding = 4
    brick_width = 64
    brick_height = 32
    top_offset = 50
    group_width = tilemap.cols*(64+padding)
    for j in range(tilemap.rows):
        for i in range(tilemap.cols):
            tile_key = int(tilemap.get_tile_key((i, j)))
            if tile_key >= 1:
                new_brick = Brick(f"Brick-{i}:{j}", (WIDTH/2-group_width/2+i*(brick_width+padding), top_offset+j*(brick_height+padding)), (brick_width, brick_height))
                new_brick.set_lives(tile_key)
                gameobjects.append(new_brick)
                bricks.append(new_brick)

def start():
    goto_level(4)
    pass

def update():
    manage_inputs()
    # Win condition
    if len(bricks) == 0:
        global level_index
        level_index+=1
        goto_level(level_index)
    for gameobject in gameobjects:
        if isinstance(gameobject, Ball):
            update_ball(gameobject)
        if isinstance(gameobject, Emitter):
            if not gameobject.is_emitting():
                gameobjects.remove(gameobject)
    pass

def draw():
    global surface, gameobjects
    surface.fill((30,30,30)) # Clear the screen surface
    gameobjects.sort(key=lambda x:x.z_order)
    for gameobject in gameobjects:
        gameobject.draw(surface)
    pygame.display.update()

def manage_inputs():
    keys = pygame.key.get_pressed()
    # Player movements
    direction = 0
    movement = player.speed
    if keys[pygame.K_RIGHT]:
        direction = 1    
    elif keys[pygame.K_LEFT]:
        direction = -1
    elif keys[pygame.K_SPACE]:
        global playing
        if(not playing):
            playing = True
            ball.velocity = Vector2(random.choice([-1, 1]), -1)
    movement*=direction
    player.set_position(Vector2(player.position.x + movement, player.position.y))
    if(player.position.x<0):
        player.position.x = 0
    if(player.position.x + player.size.x>=WIDTH):
        player.position.x = WIDTH-player.size.x
    
def quit():
    pygame.display.quit()

def goto_level(index):
    if (index>=len(levels)):
        index = 0
        goto_level(0)
    else:
        global playing
        tilemap.set_file(f"./assets/lvl{index}.csv")
        player.position = Vector2(WIDTH/2-player.size.x/2, HEIGHT-32)
        playing = False
        ball.velocity = Vector2().zero()
        ball.position = player.position + Vector2(player.size.x/2 - ball.size.x/2,- (ball.size.y+player.size.y/2))
        place_bricks()

def remove_bricks():
    global bricks, gameobjects
    for brick in bricks:
        if brick in gameobjects:
            gameobjects.remove(brick)
    bricks = []

def update_ball(ball_object):
    global playing, lives
    if(not playing):
        ball.position = player.position + Vector2(player.size.x/2 - ball.size.x/2,- (ball.size.y+player.size.y/2))
    if(ball.position.x+ball.size.x>=WIDTH or ball.position.x<0):
        ball.velocity.x*=-1
        play_sound('bounce')
    if(ball.position.y<0):
        ball.velocity.y*=-1
        play_sound('bounce')
    if check_collision(ball, player):
        side = get_ball_collision_side(player.get_rect())
        if side=="ABOVE":
            ball.velocity.y*=-1
        elif side =="RIGHT" or side =="LEFT":
            ball.velocity.x*=-1
        play_sound('bounce')

    if(ball.position.y+ball.size.y>=HEIGHT+64):
        lives-=1
        if lives == 0:
            remove_bricks()
            goto_level(0)
            lives = 3
        playing = False
        ball.velocity = Vector2().zero()

    # Handle collisions with bricks
    for brick in bricks:
        if ball.get_rect().colliderect(brick.get_rect()):
            play_sound('brique')
            side = get_ball_collision_side(brick.get_rect())
            if side == "ABOVE" or side == "UNDER":
                ball.velocity.y*=-1
            elif side =="RIGHT" or side == "LEFT":
                ball.velocity.x*=-1
            brick.lives-=1
            if(brick.lives <= 0):
                gameobjects.remove(brick)
                bricks.remove(brick)
    ball.update()

def check_collision(a:GameObject, b:GameObject):
    if a.get_rect().colliderect(b.get_rect()):
        return True
    return False

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

def play_sound(sound_id, volume=1):
    if sound_id is None or not sound_id in sounds:
        print(f"Sound effect {sound_id} does not exists !")
        return
    sound_effect = sounds.get(sound_id)
    sound_effect.play()
    sound_effect.set_volume(volume * VOLUME)

if __name__ == "__main__":
    # execute only if run as a script
    start()
    while True:
        update()
        draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit()
                elif event.key == pygame.K_f:
                    FULLSCREEN = not FULLSCREEN
                    if FULLSCREEN:
                        surface = pygame.display.set_mode(GAME_RESOLUTION, pygame.FULLSCREEN)
                    else:
                        surface = pygame.display.set_mode(GAME_RESOLUTION)
        clock.tick(TARGET_FPS)
