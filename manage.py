import pygame, random

GREEN = (0,200,0)
RED =  (200,0,0)
WINDOW_HEIGHT = 800
WINDOW_WIDTH = 800

BLOCK_SIZE = WINDOW_WIDTH // 20
MAP_SIZE = 20

snake = [(3,2),(3,3),(3,4),(3,5),(2,5)]

food = {
    "x" : 0,
    "y" : 0        
}


global SCREEN
pygame.init()
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
MOVE_SNAKE = pygame.USEREVENT
pygame.time.set_timer(MOVE_SNAKE, 100) # 500ms = 0.5s
directions = {
    "x" : 1,
    "y" : 0
}
keyqueue = []

game = {
    "shouldSpawnFood" : True
}

def updateSnakePositionInMap(gameMap):
    for i in snake:
        gameMap[i[0]][i[1]] = 1

def updateFoodPositionInMap(gameMap):
    gameMap[food["y"]][food["x"]] = 2

def drawSnakeAndMap(gameMap):
    blockSize = BLOCK_SIZE
    for y in range(len(gameMap)):
        for x in range(len(gameMap[y])):
            rect = pygame.Rect(x*blockSize, y*blockSize, blockSize,blockSize)
            if(gameMap[y][x] == 1):
                pygame.draw.rect(SCREEN, GREEN, rect)
            elif(gameMap[y][x] == 2):
                pygame.draw.rect(SCREEN, RED, rect , 10)
            else:
                pygame.draw.rect(SCREEN, GREEN, rect, 1)

def moveSnakeBodyToHead():
    for i in range(len(snake)-1):
        snake[i] = snake[i+1]
        
def checkIfDead():
    snakeHead = snake[-1]
    for i in range(len(snake)-1):
        if(snake[i] == snakeHead):
            return True
    return False

def feedSnake():
    foodPos = (food["y"],food["x"])
    if(snake[-1] == foodPos):
        snake.insert(0, snake[0])
        game["shouldSpawnFood"] = True

def spawnFood(gameMap):
    while(True):
        x = random.randint(0,len(gameMap)-1)
        y = random.randint(0,len(gameMap)-1)
        
        if(gameMap[y][x] == 0):
            food["x"] = x
            food["y"] = y
            return
    
def moveSnake(gameMap,directions):
    moveSnakeBodyToHead()
    nextXpos = snake[-1][1] + directions["x"]
    nextYpos = snake[-1][0] + directions["y"]
    if(nextXpos < 0):
        snake[-1] = (snake[-1][0], len(gameMap[0])-1)
    elif(nextXpos > len(gameMap[0])-1):
        snake[-1] = (snake[-1][0], 0)
    elif(nextYpos < 0):
        snake[-1] = (len(gameMap)-1, snake[-1][1])
    elif(nextYpos > len(gameMap)-1):
        snake[-1] = (0, snake[-1][1])
    else:
        snake[-1] = (snake[-1][0] + directions["y"], snake[-1][1] + directions["x"])

while True:
    SCREEN.fill((0, 0, 0),(0,0,WINDOW_WIDTH,WINDOW_HEIGHT))
    gameMap = [[0 for j in range(MAP_SIZE)] for i in range(MAP_SIZE)]
    updateSnakePositionInMap(gameMap)
    updateFoodPositionInMap(gameMap)
    drawSnakeAndMap(gameMap)
    feedSnake()
    if(checkIfDead()):
        pygame.quit()
    
    if(game["shouldSpawnFood"]):
        spawnFood(gameMap)
        game["shouldSpawnFood"] = False
    for event in pygame.event.get():
        if event.type == pygame.KEYUP:
            if(len(keyqueue) > 3):
                keyqueue.pop()
            if(event.key == pygame.K_LEFT):
                def fnc():
                    if(directions["x"] == 0):
                        directions["x"] = -1
                        directions["y"] = 0
                keyqueue.insert(0,fnc)
            if(event.key == pygame.K_RIGHT):
                def fnc():
                    if directions["x"] == 0:
                        directions["x"] = 1
                        directions["y"]  = 0
                keyqueue.insert(0,fnc)
            if(event.key == pygame.K_UP):
                def fnc():
                    if(directions["y"] == 0):
                        directions["y"] = -1
                        directions["x"] = 0
                keyqueue.insert(0,fnc)
            if(event.key == pygame.K_DOWN):
                def fnc():
                    if directions["y"] == 0:
                        directions["y"] = 1
                        directions["x"] = 0
                keyqueue.insert(0,fnc)
        if event.type == MOVE_SNAKE:
            if(len(keyqueue)):
                keyqueue.pop()()
            moveSnake(gameMap,directions)
        if event.type == pygame.QUIT:
            pygame.quit()
    pygame.display.update()
    
