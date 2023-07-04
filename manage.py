import pygame, random, time

GREEN = (0,200,0)
RED =  (200,0,0)
WINDOW_HEIGHT = 800
WINDOW_WIDTH = 800

BLOCK_SIZE = WINDOW_WIDTH // 20
MAP_SIZE = 20

global SCREEN
pygame.init()
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
MOVE_SNAKE = pygame.USEREVENT
pygame.time.set_timer(MOVE_SNAKE, 100) # 500ms = 0.5s


directions = {
    "x" : 0,
    "y" : 0
}

keyqueue = []

game = {
    "shouldSpawnFood" : True,
    "gameMap": [],
    "snake" :  [(3,2),(3,3),(3,4),(3,5),(2,5)]
}

food = {
    "x" : 0,
    "y" : 0        
}

def redrawMap():
    game["gameMap"] = [[0 for j in range(MAP_SIZE)] for i in range(MAP_SIZE)]

def updateSnakePositionInMap():
    for i in game["snake"]:
        game["gameMap"][i[0]][i[1]] = 1

def updateFoodPositionInMap():
    game["gameMap"][food["y"]][food["x"]] = 2

def drawSnakeAndMap():
    blockSize = BLOCK_SIZE
    for y in range(len(game["gameMap"])):
        for x in range(len(game["gameMap"][y])):
            rect = pygame.Rect(x*blockSize, y*blockSize, blockSize,blockSize)
            if(game["gameMap"][y][x] == 1):
                pygame.draw.rect(SCREEN, GREEN, rect)
            elif(game["gameMap"][y][x] == 2):
                pygame.draw.rect(SCREEN, RED, rect , 10)
            else:
                pygame.draw.rect(SCREEN, GREEN, rect, 1)

def moveSnakeBodyToHead():
    if(directions["x"] !=0 or directions["y"] !=0):
        for i in range(len(game["snake"])-1):
            game["snake"][i] = game["snake"][i+1]
        
def checkIfDead():
    snakeHead = game["snake"][-1]
    for i in range(len(game["snake"])-1):
        if(game["snake"][i] == snakeHead):
            return True
    return False

def feedSnake():
    foodPos = (food["y"],food["x"])
    if(game["snake"][-1] == foodPos):
        game["snake"].insert(0, game["snake"][0])
        game["shouldSpawnFood"] = True

def spawnFood():
    while(True):
        x = random.randint(0,len(game["gameMap"])-1)
        y = random.randint(0,len(game["gameMap"])-1)
        
        if(game["gameMap"][y][x] == 0):
            food["x"] = x
            food["y"] = y
            return
    
def moveSnake(directions):
    moveSnakeBodyToHead()
    nextXpos = game["snake"][-1][1] + directions["x"]
    nextYpos = game["snake"][-1][0] + directions["y"]
    if(nextXpos < 0):
        game["snake"][-1] = (game["snake"][-1][0], len(game["gameMap"][0])-1)
    elif(nextXpos > len(game["gameMap"][0])-1):
        game["snake"][-1] = (game["snake"][-1][0], 0)
    elif(nextYpos < 0):
        game["snake"][-1] = (len(game["gameMap"])-1, game["snake"][-1][1])
    elif(nextYpos > len(game["gameMap"])-1):
        game["snake"][-1] = (0, game["snake"][-1][1])
    else:
        game["snake"][-1] = (game["snake"][-1][0] + directions["y"], game["snake"][-1][1] + directions["x"])
        
def reset():
    game["snake"] = [(3,2),(3,3),(3,4),(3,5),(2,5)]
    directions["x"] = 0
    directions["y"] = 0
    
while True:
    SCREEN.fill((0, 0, 0),(0,0,WINDOW_WIDTH,WINDOW_HEIGHT))
    redrawMap()
    updateSnakePositionInMap()
    updateFoodPositionInMap()
    drawSnakeAndMap()
    feedSnake()
    
    if(checkIfDead()):
        reset()
    
    if(game["shouldSpawnFood"]):
        spawnFood()
        game["shouldSpawnFood"] = False
    for event in pygame.event.get():
        if event.type == pygame.KEYUP:
            if(len(keyqueue) > 3):
                keyqueue.pop()
            if(event.key in [pygame.K_LEFT, pygame.K_a]):
                def fnc():
                    if(directions["x"] == 0):
                        directions["x"] = -1
                        directions["y"] = 0
                keyqueue.insert(0,fnc)
            if(event.key in [pygame.K_RIGHT, pygame.K_d]):
                def fnc():
                    if directions["x"] == 0:
                        directions["x"] = 1
                        directions["y"]  = 0
                keyqueue.insert(0,fnc)
            if(event.key in [pygame.K_UP, pygame.K_w]):
                def fnc():
                    if(directions["y"] == 0):
                        directions["y"] = -1
                        directions["x"] = 0
                keyqueue.insert(0,fnc)
            if(event.key in [pygame.K_DOWN, pygame.K_s]):
                def fnc():
                    if directions["y"] == 0:
                        directions["y"] = 1
                        directions["x"] = 0
                keyqueue.insert(0,fnc)
        if event.type == MOVE_SNAKE:
            if(len(keyqueue)):
                keyqueue.pop()()
            moveSnake(directions)
        if event.type == pygame.QUIT:
            pygame.quit()
    pygame.display.update()
    
