#this is JakeTheHolt - nonoNO this is JUSTIN!
import time

TILE_SIZE = 64
WIDTH = TILE_SIZE * 8
HEIGHT = TILE_SIZE * 8
LEVEL = 0
MAX_LEVEL = 1

tiles = ['path', 'wall', 'goal', 'door', 'key', 'blah']
unlock = 0

maze = [
[
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 2, 0, 1],
    [1, 0, 1, 0, 1, 1, 3, 1],
    [1, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 1],
    [1, 0, 1, 4, 1, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1]
],
[
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 2, 0, 1],
    [1, 0, 1, 0, 1, 1, 3, 1],
    [1, 0, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 4, 0, 1],
    [1, 1, 1, 0, 1, 0, 0, 1],
    [1, 1, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1]
]
]

player = Actor("player", anchor=(0, 0), pos=(1 * TILE_SIZE, 1 * TILE_SIZE))
enemy  = Actor("enemy",  anchor=(0, 0), pos=(3 * TILE_SIZE, 6 * TILE_SIZE))
enemy.yv = -1
sounds.welcome.play()
#music.play('background')
#music.set_volume(0.2)

def draw():
    global LEVEL
    screen.clear()
    for row in range(len(maze[LEVEL])):
        for column in range(len(maze[LEVEL][row])):
            x = column * TILE_SIZE
            y = row * TILE_SIZE
            tile = tiles[maze[LEVEL][row][column]]
            if tile!='path':
                screen.blit('path', (x, y)) # This draws a path under everything not a path!
            screen.blit(tile, (x, y)) # Draw the tile as the maze intended
    player.draw()
    enemy.draw()

def on_key_down(key):
    # player movement
    global LEVEL
    global MAX_LEVEL
    row = int(player.y / TILE_SIZE)
    column = int(player.x / TILE_SIZE)
    if key == keys.UP:
        row = row - 1
        player.image = 'player'
    if key == keys.DOWN:
        row = row + 1
        player.image = 'player'
    if key == keys.LEFT:
        column = column - 1
        player.image = 'playerleft'
    if key == keys.RIGHT:
        column = column + 1
        player.image = 'player'
    tile = tiles[maze[LEVEL][row][column]]
    if tile != 'wall' and tile != 'door':
        x = column * TILE_SIZE
        y = row * TILE_SIZE
        animate(player, duration=0.1, pos=(x, y))
    global unlock
    if tile == 'goal':
        print("Well done")
        LEVEL = LEVEL + 1
        animate(player, duration=1.0, pos=(64, 64))
        unlock = 0
        if (LEVEL > MAX_LEVEL):
            sounds.winner_chicken_dinner.play()
            time.sleep(3)
        else:
            sounds.win.play()

        #exit()
    elif tile == 'key':
        unlock = unlock + 1
        maze[LEVEL][row][column] = 0 # 0 is 'path' tile
        sounds.yum.play()
    elif tile == 'door' and unlock > 0:
        unlock = unlock - 1
        maze[LEVEL][row][column] = 0 # 0 is 'path' tile
        sounds.thank_you.play()

    # enemy movement
    row    = int(enemy.y / TILE_SIZE)
    column = int(enemy.x / TILE_SIZE)
    row = row + enemy.yv
    tile = tiles[maze[LEVEL][row][column]]
    if not tile == 'wall':
        x = column * TILE_SIZE
        y = row * TILE_SIZE
        animate(enemy, duration=0.1, pos=(x, y))
    else:
        enemy.yv = enemy.yv * -1
    if enemy.colliderect(player):
        sounds.that_hurt.play()
        time.sleep(2)
        print("You died")
        exit()
