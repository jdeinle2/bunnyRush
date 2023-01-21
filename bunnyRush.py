#this is JakeTheHolt - nonoNO this is JUSTIN!
import time
import maze
import cheatcodes
import re
import random

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
PROJECTILE_SPEED = 1.0 # Smaller is faster

unlock = 0

player = Actor("player", anchor=(0, 0), pos=(player_start[LEVEL][0], player_start[LEVEL][1]))
enemy  = Actor("enemy",  anchor=(0, 0), pos=(enemy_start[LEVEL][0], enemy_start[LEVEL][1]))
projectile = Actor("projectile", anchor=(32, 32), pos=(2 * TILE_SIZE, 1 * TILE_SIZE))

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
            if tile=='goal2' or tile=='doorkey' or tile=='castledoor':
                screen.blit('obsidian', (x, y)) # draws obsidian under the goal in level 3
            screen.blit(tile, (x, y)) # Draw the tile as the maze intended
            if tile=='goal4':
                screen.blit('crackedfloor', (x, y)) # draws crackedfloor under the goal in level 4
            screen.blit(tile, (x, y)) # Draw the tile as the maze intended
    for character in VISIBLE:
        character.draw()
    #player.draw()
    #enemy.draw()
    #projectile.draw()

def update(): # Update function is called 60 times a second
    global VISIBLE
    global TIMER
    TIMER = TIMER + 1

    if TIMER%30 == 0: # Every 0.5 seconds, move the enemy
        move_enemy()

    if projectile in VISIBLE: # If projectile is visible, then move it by one space in the direction last perfored
        if projectile.x >= WIDTH or projectile.y >= HEIGHT or projectile.x <= -TILE_SIZE/2.0 or projectile.y <= -TILE_SIZE/2.0:
            VISIBLE.remove(projectile)
        if enemy in VISIBLE and projectile.colliderect(enemy): # Did the projectile collide with the enemy?
            VISIBLE.remove(enemy) # Make enemy go away
            sounds.gotcha.play()  # Play "gotcha" sound

    if enemy in VISIBLE and enemy.colliderect(player): # Check for player/enemy collision
        sounds.that_hurt.play()
        time.sleep(2)
        print("You died")
        exit()

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
        player.image = 'player'
        DIRECTION = [0,-1]
    if key == keys.DOWN:
        row = row + 1
        player.image = 'player'
        DIRECTION = [0,1]
    if key == keys.LEFT:
        column = column - 1
        player.image = 'playerleft'
        DIRECTION = [-1,0]
    if key == keys.RIGHT:
        column = column + 1
        player.image = 'player'
        DIRECTION = [1,0]

    if key == keys.SPACE: #  If projectile isn't visible, then make it visible and snap it to the same coordinate as the player
        throw_projectile()

    check_cheatcode(key)

    tile = tiles[maze[LEVEL][row][column]]
    if tile != 'wall' and tile!='border' and tile!='bunny' and tile!='castledoor' and tile!='lava':
        x = column * TILE_SIZE
        y = row * TILE_SIZE
        animate(player, duration=0.1, pos=(x, y))
    global unlock

    if tile == 'goal':
        complete_stage("Well done")
    elif tile == 'goal2':
        complete_stage("Well done")
    elif tile == 'goal3':
        complete_stage("Be careful in the castle")
        music.stop()
        music.play('castle')
        music.set_volume(100)
    elif tile == 'goal4':
        complete_stage("THE END")
    elif tile == 'carrot':
        unlock = unlock + 1
        maze[LEVEL][row][column] = 0 # 0 is 'path' tile
        sounds.yum.play()
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

# enemy movement
def move_enemy():
    if enemy not in VISIBLE:
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
    if LEVEL == 2:
        sounds.gate.play()
        time.sleep(4)
    print(message)
    if (LEVEL == MAX_LEVEL):
        sounds.winner_chicken_dinner.play()
        time.sleep(3)
        exit()
    else:
        sounds.win.play()
    LEVEL = LEVEL + 1
    animate(player, duration=0.001, pos=(player_start[LEVEL][0], player_start[LEVEL][1]))
    animate(enemy, duration=0.001, pos=(enemy_start[LEVEL][0], enemy_start[LEVEL][1]))
    if LEVEL==MAX_LEVEL:
        print("Defeat the boss bear!")
    if enemy not in VISIBLE:
        VISIBLE.append(enemy)
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

def check_cheatcode(key):
    global CHEATMODE
    global LEVEL
    # Check if secret cheat word is entered, if so, you can skip to any stage you want!
    if not CHEATMODE:
        CHEATMODE = cheatcodes.check_secret_word(key)
    if CHEATMODE and (cheatcodes.validate(key, MAX_LEVEL)):
        LEVEL = cheatcodes.validate(key, MAX_LEVEL) - 1
        complete_stage("CHEATER CHEATER!!!")
