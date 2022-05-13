import pygame, sys

clock = pygame.time.Clock()

from pygame.locals import *
pygame.init()

#Screen--------------------------------------   
windowSize = (800, 800)
screen = pygame.display.set_mode(windowSize)
#display = pygame.Surface((768, 768))
pygame.display.set_caption("Alpha 0.0.4")

#Sprites--------------------------------------
playerImage = pygame.image.load("player.png").convert_alpha()
grassImage = pygame.image.load("grass.png").convert()
dirtImage = pygame.image.load("dirt.png").convert()

#Values---------------------------------------
movingRight = False
movingLeft = False

playerYspeed = 0
playerRect = pygame.Rect(0, 0, playerImage.get_width(), playerImage.get_height())
playerMovement = []

tileSize = grassImage.get_width()
tileRects = []

display = pygame.Surface((160, 160))

airTimer = 0
scrollValue = [0,0]

#funcions--------------------------------------
def collisionTest(rect, tiles) :
    hitList = []
    for tile in tiles :
        if rect.colliderect(tile) :
            hitList.append(tile)
    return hitList

def move(rect, movement, tiles) :
    collisionTypes = {"top": False, "bottom": False, "right": False, "left": False}
    rect.x += movement[0]
    hitList = collisionTest(rect, tiles)
    for tile in hitList :
        if movement[0] > 0 :
            rect.right = tile.left
            collisionTypes['right'] = True
        elif movement[0] < 0 :
            rect.left = tile.right
            collisionTypes['left'] = True
    rect.y += movement[1]
    hitList = collisionTest(rect, tiles)
    for tile in hitList :
        if movement[1] > 0 :
            rect.bottom = tile.top
            collisionTypes['bottom'] = True
        elif movement[1] < 0 :
            rect.top = tile.bottom
            collisionTypes['top'] = True
    return rect, collisionTypes

def loadMap(path) :
    f = open(path + ".txt", "r")
    data = f.read()
    f.close()
    data = data.split("\n")
    gameMap = []
    for row in data :
        gameMap.append(list(row))
    return gameMap

gameMap = loadMap("map")

#Game Loop---\/\/
while True :

    print(clock.get_fps())

#Render---------------------------------------
    display.fill((140, 230, 210))
    #display.blit(backgroundImage, (0 , 0))

    scrollValue[0] += (playerRect.x - scrollValue[0]-80)/10
    scrollValue[1] += (playerRect.y - scrollValue[1]-80)/10

    y = 0
    for row in gameMap :
        x = 0
        for tile in row :
            x += 1

            if (x * tileSize - scrollValue[0] - tileSize) < 160 and (x * tileSize - scrollValue[0]) > 0 :

                if tile == "1" :
                    display.blit(dirtImage, (x * tileSize - tileSize - scrollValue[0], y * tileSize - scrollValue[1]))

                if tile == "2" :
                    display.blit(grassImage, (x * tileSize - tileSize - scrollValue[0], y * tileSize - scrollValue[1]))        

                if tile != "0" :
                    tileRects.append(pygame.Rect(x * tileSize - tileSize, y * tileSize, tileSize, tileSize))


        y += 1

    #playerYspeed += 0.2

    playerMovement = [0, 0]
    if movingRight :
        playerMovement[0] += 1
    if movingLeft :
        playerMovement[0] -= 1
    playerMovement[1] += playerYspeed
    playerYspeed += 0.2
    if playerYspeed > 4 :
        playerYspeed = 4

    playerRect, colligions = move(playerRect, playerMovement, tileRects)
    if colligions["bottom"] :
        playerYspeed = 0
        airTimer = 0
    else :
        airTimer += 1

    display.blit(playerImage, (playerRect.x - scrollValue[0], playerRect.y - scrollValue[1]))

#Quit-----------------------------------------
    for event in pygame.event.get() :
        if event.type == QUIT :
            pygame.quit()
            sys.exit()

#Inputs---------------------------------------
        if event.type == KEYDOWN :
            if event.key == K_RIGHT :
                movingRight = True
            if event.key == K_LEFT :
                movingLeft = True
            if event.key == K_UP :
                if airTimer < 6 :
                    playerYspeed = - 4
        if event.type == KEYUP :
            if event.key == K_RIGHT :
                movingRight = False
            if event.key == K_LEFT :
                movingLeft = False

    surf = pygame.transform.scale(display, windowSize)
    screen.blit(surf, (0, 0))
    pygame.display.update()
    clock.tick(60)