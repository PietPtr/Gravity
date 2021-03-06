from __future__ import division
import pygame, sys, random, os
from pygame.locals import *

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (700,40)

pygame.init()

windowSurface = pygame.display.set_mode((600, 900), 0, 32) #always 0 and 32
pygame.display.set_caption('Gravity')

basicFont = pygame.font.SysFont(None, 23)

mainClock = pygame.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 100, 0)
BLUE = (0, 0, 255)

ACCELERATION = 0.01
BOUNCE = 1.05

def distance(speed, time):
    distance = time * speed
    return distance

class Rectangle(object):
    global RectList
    def __init__(self, name, position, speed, dropped):
        self.name = name
        self.position = position
        self.speed = speed
        self.dropped = dropped
        self.rect = (int(self.position[0]), int(self.position[1]), 40, 40)
    def render(self, frameTime):
        windowSurface.blit(apple, (self.position[0], self.position[1] - 10))
        self.position[1] = self.position[1] + distance(self.speed, frameTime)
        self.speed = self.speed + ACCELERATION
        if self.position[1] > 860:
            self.speed = (self.speed / BOUNCE) * -1
        elif self.position[1] < 0:
            self.position[1] = 0
        self.rect = pygame.Rect(int(self.position[0]), int(self.position[1]), 40, 40)
    def collision(self):
        for rect in RectList:
            if self.name == rect.name:
                continue
            if self.rect.colliderect(rect.rect) == True:
                self.speed = (self.speed / BOUNCE) * -1

player = pygame.image.load('player.png')
background = pygame.image.load('bg.png')
apple = pygame.image.load('apple.png')

playerX = 300

RectList = []
clicked = False

lastDrop = pygame.time.get_ticks()

loopTrack = 0
while True:
    loopTrack += 1
    frameTime = mainClock.tick(1000)
    FPS = mainClock.get_fps()
    currentTime = pygame.time.get_ticks()
    mousePos = pygame.mouse.get_pos()
    
    windowSurface.blit(background, (0, 0))
    #windowSurface.fill(GREEN)

    if pygame.key.get_pressed()[97] == True:
        playerX = playerX - distance(0.5, frameTime)
    elif pygame.key.get_pressed()[100] == True:
        playerX = playerX + distance(0.5, frameTime)

    if clicked == True and pygame.time.get_ticks() - lastDrop >= 350:
        RectList.append(Rectangle(loopTrack, [playerX, 61], 0.05, pygame.time.get_ticks()))
        clicked = False
        lastDrop = pygame.time.get_ticks()   

    for Rect in RectList:
        Rect.render(frameTime)
        Rect.collision()
        if mousePos[0] >= Rect.position[0] and mousePos[0] <= Rect.position[0] + 40 and mousePos[1] >= Rect.position[1] and mousePos[1] <= Rect.position[1] + 40 and pygame.mouse.get_pressed()[0] == True:
            RectList.remove(Rect)

    windowSurface.blit(player, (playerX, 10))
    
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == KEYUP and event.key == 13:
            clicked = True
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
