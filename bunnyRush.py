#this is JakeTheHolt - nonoNO this is JUSTIN!
import time
import maze
import cheatcodes
import re
import random
import timer

tiles        = maze.tiles
player_start = maze.player_start
enemy_start  = maze.enemy_start
maze         = maze.maze

TILE_SIZE = 64
WIDTH = TILE_SIZE * 8
HEIGHT = TILE_SIZE * 8
LEVEL = 1
MAX_LEVEL = 4
CHEATMODE = 0
DIRECTION = [1,0]
TIMER = 0
PLAYER_HEALTH = 1
ENEMY_HEALTH = 1
ENEMY_SPEED = 60 #60 is 1 tile every second!
PROJECTILE_SPEED = 1.0 # Smaller is faster

unlock = 0

player = Actor("player", anchor=(0, 0), pos=(player_start[LEVEL][0], player_start[LEVEL][1]))
enemy  = Actor("enemy",  anchor=(0, 0), pos=(enemy_start[LEVEL][0], enemy_start[LEVEL][1]))
projectile = Actor("projectile", anchor=(32, 32), pos=(2 * TILE_SIZE, 1 * TILE_SIZE))

# Declare Game Timers
enemy_hit_timer  = timer.timer(enemy,  60)  # Create a timer which is only active when the enemy is visible
player_hit_timer = timer.timer(player, 60) # Create a timer which is only active when the player is visible
timers = [enemy_hit_timer, player_hit_timer]

VISIBLE = [player, enemy]

enemy.yv = -1
sounds.welcome.play()
music.play('background')
music.set_volume(0.4)

def draw():
    global LEVEL
    screen.clear()
    for row in range(len(maze[LEVEL])):
        for column in range(len(maze[LEVEL][row])):
            x = column * TILE_SIZE
            y = row * TILE_SIZE
            tile = tiles[maze[LEVEL][row][column]]
            if tile!='path' or tile!='goal2' or tile!='doorkey' or tile!='castledoor' or tile!='goal4':
                screen.blit('path', (x, y)) # This draws a path under everything not a path!
            screen.blit(tile, (x, y)) # Draw the tile as the maze intended
            if tile=='goal2' or tile=='doorkey' or tile=='castledoor' or tile=='goldencarrot':
                screen.blit('obsidian', (x, y)) # draws obsidian under the goal in level 3
            screen.blit(tile, (x, y)) # Draw the tile as the maze intended
            if tile=='goal4':
                screen.blit('crackedfloor', (x, y)) # draws crackedfloor under the goal in level 4
            if not (tile=='goal4' and ENEMY_HEALTH!=0):
                screen.blit(tile, (x, y)) # Draw the tile as the maze intended
    for character in VISIBLE: # Draw all visible characters
        character.draw()
    screen.draw.text("LEVEL:" + str(LEVEL),[5,0],fontname="sans", fontsize=30) # Print level in upper left corner of screen
    if (PLAYER_HEALTH==1):
        screen.blit('health1', (130, 1))
    if (PLAYER_HEALTH==2):
        screen.blit('health1', (130, 1))
        screen.blit('health2', (200, 1))
    if (PLAYER_HEALTH==3):
        screen.blit('health1', (130, 1))
        screen.blit('health2', (200, 1))
        screen.blit('health3', (270, 1))
    if CHEATMODE == 1:
        screen.draw.text("CHEAT MODE ON", [150,0],fontname="sans", fontsize=30, color="darkred")
def update(): # Update function is called 60 times a second
    global VISIBLE
    global TIMER
    global ENEMY_HEALTH
    global ENEMY_SPEED
    global PLAYER_HEALTH
    TIMER = TIMER + 1

    advance_timers() # Function to advance all active timers

    if TIMER%ENEMY_SPEED == 0: # Every 0.5 seconds, move the enemy
        move_enemy()

    if projectile in VISIBLE: # If projectile is visible, then move it by one space in the direction last perfored
        if projectile.x >= WIDTH or projectile.y >= HEIGHT or projectile.x <= -TILE_SIZE/2.0 or projectile.y <= -TILE_SIZE/2.0:
            VISIBLE.remove(projectile)
        if enemy in VISIBLE and projectile.colliderect(enemy) and not enemy_hit_timer.is_active(): # Did the projectile collide with the enemy?
            ENEMY_HEALTH -= 1
            enemy_hit_timer.start() # start the timer for the enemy
            if (ENEMY_HEALTH == 0):
                enemy.image = 'enemy_hit'
            if (ENEMY_HEALTH == 2):
                enemy.image = 'enemy_hurt'
            if (ENEMY_HEALTH == 1):
                enemy.image = 'enemy_hurt2'
            sounds.gotcha.play()  # Play "gotcha" sound

    if enemy in VISIBLE:
        if (enemy_hit_timer.is_expired() and (ENEMY_HEALTH == 0)): # Only after the timer has expired, and health is 0, remove the enemy
            VISIBLE.remove(enemy)
        elif enemy.colliderect(player) and not player_hit_timer.is_active() and not enemy_hit_timer.is_active(): # Cannot get hit again if the player hit timer is active
            PLAYER_HEALTH -= 1
            sounds.that_hurt.play()
            player_hit_timer.start()
            print ("YOU GOT HIT!!" + " HEALTH:", PLAYER_HEALTH )
            if (PLAYER_HEALTH == 0):
                game_exit("YOU DIED!")

def on_key_down(key):
    # player movement
    global LEVEL
    global MAX_LEVEL
    global DIRECTION
    global PROJECTILE_DIRECTION
    global VISIBLE

    row = int(player.y / TILE_SIZE)
    column = int(player.x / TILE_SIZE)

    if key == keys.UP:
        row = row - 1
        player.image = 'playerup'
        DIRECTION = [0,-1]
    if key == keys.DOWN:
        row = row + 1
        player.image = 'playerdown'
        DIRECTION = [0,1]
    if key == keys.LEFT:
        column = column - 1
        player.image = 'playerleft'
        DIRECTION = [-1,0]
    if key == keys.RIGHT:
        column = column + 1
        player.image = 'player'
        DIRECTION = [1,0]

    #if LEVEL == 4 or CHEATMODE == 1: #only throw if level is 4
    if key == keys.SPACE:
        throw_projectile()

    check_cheatcode(key)

    tile = tiles[maze[LEVEL][row][column]]
    if tile != 'wall' and tile!='border' and tile!='bunny' and tile!='castledoor' :
        x = column * TILE_SIZE
        y = row * TILE_SIZE
        animate(player, duration=0.1, pos=(x, y))
    global unlock
    global PLAYER_HEALTH

    if tile == 'goal':
        complete_stage("Well done")
    elif tile == 'goal2':
        complete_stage("Well done")
    elif tile == 'goal3':
        complete_stage("Be careful in the castle")
        music.stop()
        music.play('castle')
        music.set_volume(0.2)
    elif tile == 'goal4' and ENEMY_HEALTH==0:
        complete_stage("THE END")
    elif tile == 'carrot':
        unlock = unlock + 1
        maze[LEVEL][row][column] = 0 # 0 is 'path' tile
        sounds.yum.play()
    elif tile == 'goldencarrot':
        PLAYER_HEALTH+=2
        sounds.yum.play()
        maze[LEVEL][row][column] = 5 # 5 is 'obsidian' tile
    elif tile == 'bunny' and unlock > 0:
        unlock = unlock - 1
        maze[LEVEL][row][column] = 0 # 0 is 'path' tile
        sounds.thank_you.play()
    elif tile == 'doorkey':
        unlock = unlock + 1
        maze[LEVEL][row][column] = 5 # 0 is 'path' tile
        sounds.yum.play()
    elif tile == 'castledoor' and unlock > 0:
        unlock = unlock - 1
        maze[LEVEL][row][column] = 5 # 0 is 'path' tile
        sounds.dooropening.play()

    if CHEATMODE == 1:
        PLAYER_HEALTH = 100
# enemy movement
def move_enemy():
    if enemy not in VISIBLE or enemy_hit_timer.is_active():
        return # Return from function if enemy is no longer visible
    x = enemy.x
    y = enemy.y
    if LEVEL==4: # Move towards player for boss level
        if random.randint(0, 1): # randomly choose number (0 or 1), if 1, move enemy in x direction closer to player, if 0, move enemy in y direction closer to player
            if player.x < enemy.x:
                x -= TILE_SIZE
            else:
                x += TILE_SIZE
        else:
            if player.y < enemy.y:
                y -= TILE_SIZE
            else:
                y += TILE_SIZE
    else:
        y += (enemy.yv * TILE_SIZE)

    row    = int(y / TILE_SIZE)
    column = int(x / TILE_SIZE)
    tile = tiles[maze[LEVEL][row][column]]
    if tile!='wall' and tile!='border':
        animate(enemy, duration=0.1, pos=(x, y))
    else:
        enemy.yv = enemy.yv * -1

def complete_stage(message):
    global LEVEL
    global ENEMY_HEALTH
    global PLAYER_HEALTH
    print(message)
    ENEMY_HEALTH = 1
    if LEVEL == 2: #Castle Level
        sounds.gate.play()
        time.sleep(4)
    elif (LEVEL == MAX_LEVEL-1): #boss level
        ENEMY_HEALTH = 3
    elif (LEVEL == MAX_LEVEL):
        sounds.winner_chicken_dinner.play()
        game_exit("YOU WIN!")

    else:
        sounds.win.play()
    LEVEL = LEVEL + 1
    if LEVEL==MAX_LEVEL:
        print("Defeat the boss bear!")
    if enemy not in VISIBLE: # Reinitialize enemy if it was killed
        VISIBLE.append(enemy)
        enemy.image = 'enemy'
        enemy_hit_timer.reset()
    animate(player, duration=0.001, pos=(player_start[LEVEL][0], player_start[LEVEL][1]))
    animate(enemy, duration=0.001, pos=(enemy_start[LEVEL][0], enemy_start[LEVEL][1]))
    unlock = 0

def throw_projectile():
    if projectile in VISIBLE:
        return
    VISIBLE.append(projectile)
    projectile.x = player.x + (TILE_SIZE/2.0)
    projectile.y = player.y + (TILE_SIZE/2.0)
    if DIRECTION == [0,-1]: # UP
        projectile.angle = 180
        x = projectile.x
        y = -TILE_SIZE
        duration = ((player.y+TILE_SIZE) / HEIGHT) * PROJECTILE_SPEED
    elif DIRECTION == [0,1]: # DOWN
        projectile.angle = 0
        x = projectile.x
        y = HEIGHT
        duration = ((HEIGHT-player.y) / HEIGHT) * PROJECTILE_SPEED
    elif DIRECTION == [-1,0]: # LEFT
        projectile.angle = 270
        x = -TILE_SIZE
        y = projectile.y
        duration = ((player.x+TILE_SIZE) / WIDTH) * PROJECTILE_SPEED
    elif DIRECTION == [1,0]: # RIGHT
        projectile.angle = 90
        x = WIDTH
        y = projectile.y
        duration = ((WIDTH-player.x) / WIDTH) * PROJECTILE_SPEED
    animate(projectile, duration=(duration), pos=(x, y))
    sounds.throw.play()

# Advance all of the timers, but only if their actors are visible and they are active
def advance_timers():
    for t in timers:
        #print ("name:" + t.actor.image + " count:", t.count, " visible:", t.actor in VISIBLE," active:", t.is_active())
        if (t.actor in VISIBLE) and t.is_active():
            t.advance()

def check_cheatcode(key):
    global CHEATMODE
    global LEVEL
    # Check if secret cheat word is entered, if so, you can skip to any stage you want!
    if not CHEATMODE:
        CHEATMODE = cheatcodes.check_secret_word(key)
    if CHEATMODE and (cheatcodes.validate(key, MAX_LEVEL)):
        LEVEL = cheatcodes.validate(key, MAX_LEVEL) - 1
        complete_stage("CHEATER CHEATER!!!")

def game_exit(message):
    print (message)
    time.sleep(2)
    exit()
