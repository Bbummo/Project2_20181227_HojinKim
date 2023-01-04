## 20181227 HojinKim ##
## Translation/Rotation of Pivot/Anchor - Solar System ##
# Project 2: A Solar System

## - Defined Value --------------------------------------------##
import pygame
import os
import numpy as np 

## - Defined Variable -----------------------------------------##
# 색 정의
BLACK = (0, 0, 0)
GREY = (127, 127, 127)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)

## - Class ----------------------------------------------------##
class OrbitNode:
    def __init__(self, _pivotPoint, _anchorPoint):
        pivotPoint_temp = _pivotPoint.copy()
        pivotPoint_temp.append(1)
        self.pivotPoint_ = np.array(pivotPoint_temp).T
        anchorPoint_temp = _anchorPoint.copy()
        anchorPoint_temp.append(1)
        self.anchorPoint_ = np.array(anchorPoint_temp).T
    
    def rotate(self, _degree, _pivotPoint):
        H = Tmat(_pivotPoint[0], _pivotPoint[1]) @ Rmat(_degree) @ Tmat(-_pivotPoint[0], -_pivotPoint[1])
        self.pivotPoint_ = H @ self.pivotPoint_
        self.anchorPoint_ = H @ self.anchorPoint_

    def move(self,_pivotXY):
        difference = _pivotXY - self.pivotPoint_[:2]
        difference_ = difference.tolist()
        difference_.append(0)
        pivotPoint_temp = self.pivotPoint_.T
        anchorPoint__temp =self.anchorPoint_.T
        self.pivotPoint_ = (pivotPoint_temp + np.array(difference_)).T
        self.anchorPoint_ = (anchorPoint__temp + np.array(difference_)).T

## - Function -------------------------------------------------##
def Rmat(_deg):
    radian = np.deg2rad(_deg)
    c = np.cos(radian)
    s = np.sin(radian)
    R = np.array( [[ c, -s, 0], [s, c, 0], [0, 0, 1] ] )
    return R

def Tmat(_a,_b):
    H = np.eye(3)
    H[0,2] = _a
    H[1,2] = _b
    return H
    
## - Variable -------------------------------------------------##
frameTime = 0

## - Setup ----------------------------------------------------##
# Pygame 초기화
pygame.init()
info = pygame.display.Info()
pygame.display.set_caption("P2_solarSystem_20181227_HojinKim")
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WINDOW_WIDTH, WINDOW_HEIGHT = pygame.display.get_surface().get_size()
clock = pygame.time.Clock()

# Asset path
assets_path = os.path.join(os.path.dirname(__file__), '_assets')

# Image init
img_sun = pygame.image.load(os.path.join(assets_path, '0.png'))
img_venus = pygame.image.load(os.path.join(assets_path, '1.png'))
img_venus = pygame.transform.scale(img_venus, (50, 50))
img_earth = pygame.image.load(os.path.join(assets_path, '2.png'))
img_earth = pygame.transform.scale(img_earth, (70, 70))
img_saturn = pygame.image.load(os.path.join(assets_path, '3.png'))
img_saturn = pygame.transform.scale(img_saturn, (250, 100))
img_moon = pygame.image.load(os.path.join(assets_path, '4.png'))
img_moon = pygame.transform.scale(img_moon, (30, 30))
img_titan = pygame.image.load(os.path.join(assets_path, '5.png'))
img_titan = pygame.transform.scale(img_titan, (30, 30))
img_ship = pygame.image.load(os.path.join(assets_path, '6.png'))
img_ship = pygame.transform.scale(img_ship, (105, 30))

# Class init
window_centerX = WINDOW_WIDTH/2
window_centerY = WINDOW_HEIGHT/2

orbit_venus = OrbitNode([window_centerX,window_centerY]
, [window_centerX+150,window_centerY])
orbit_earth = OrbitNode([window_centerX,window_centerY]
, [window_centerX+300,window_centerY])
orbit_saturn = OrbitNode([window_centerX,window_centerY]
, [window_centerX+450,window_centerY])
orbit_moon = OrbitNode(orbit_earth.anchorPoint_.tolist()[:2]
, [orbit_earth.anchorPoint_.tolist()[:2][0]+100, orbit_earth.anchorPoint_.tolist()[:2][1]])
orbit_titan = OrbitNode(orbit_saturn.anchorPoint_.tolist()[:2]
, [orbit_saturn.anchorPoint_.tolist()[:2][0]+100, orbit_saturn.anchorPoint_.tolist()[:2][1]])

# Star list init
starList = []
for _ in range(300):
    tempList = [np.random.randint(WINDOW_WIDTH), np.random.randint(WINDOW_HEIGHT)]
    starList.append(tempList)

# Ship init
targetXY = [np.random.randint(WINDOW_WIDTH), np.random.randint(WINDOW_HEIGHT)]
rect_ship = img_ship.get_rect(center = [window_centerX/2, window_centerY/2])

# Orbital speed
# relative value
ratio = 1
speed_venus = ratio / 243.01 * 365.26
speed_earth = ratio / 365.26 * 365.26
speed_saturn = ratio / 10759.22 * 365.26
speed_moon = ratio / 27.32 * 365.26
speed_titan = ratio / 15.94 * 365.26

## - Update ---------------------------------------------------##
# 게임 종료 전까지 반복
done = False

# 게임 반복 구간
while not done:
    # 이벤트 반복 구간
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True

    # 윈도우 화면 채우기
    screen.fill(BLACK)

    # Node adjust
    #saturn adjust
    orbit_saturn_elip = [window_centerX + np.cos(frameTime*speed_saturn/60)*250
    ,window_centerY]

    orbit_venus.rotate(speed_venus, np.array([window_centerX, window_centerY]))
    orbit_earth.rotate(speed_earth, np.array([window_centerX, window_centerY]))
    orbit_saturn.move(orbit_saturn_elip)
    orbit_saturn.rotate(speed_saturn, np.array([window_centerX, window_centerY]))
    orbit_moon.move(orbit_earth.anchorPoint_.tolist()[:2])
    orbit_moon.rotate(speed_moon, orbit_earth.anchorPoint_.tolist()[:2])
    orbit_titan.move(orbit_saturn.anchorPoint_.tolist()[:2])
    orbit_titan.rotate(speed_titan, orbit_saturn.anchorPoint_.tolist()[:2])

    # Image center adjust
    rect_sun = img_sun.get_rect(center = [window_centerX, window_centerY])
    rect_venus = img_venus.get_rect(center = orbit_venus.anchorPoint_.tolist()[:2])
    rect_earth = img_earth.get_rect(center = orbit_earth.anchorPoint_.tolist()[:2])
    rect_saturn = img_saturn.get_rect(center = orbit_saturn.anchorPoint_.tolist()[:2])
    rect_moon = img_moon.get_rect(center = orbit_moon.anchorPoint_.tolist()[:2])
    rect_titan = img_titan.get_rect(center = orbit_titan.anchorPoint_.tolist()[:2])
    rect_ship = img_ship.get_rect(center = [rect_ship.center[0] + (targetXY[0]-rect_ship.center[0])*0.01
    , rect_ship.center[1] + (targetXY[1]-rect_ship.center[1])*0.01])

    # Draw
    for starXY in starList:
        pygame.draw.circle(screen, WHITE, starXY, np.random.randint(5))

    screen.blit(img_sun, rect_sun) # sun
    screen.blit(img_venus, rect_venus) # venus
    screen.blit(img_earth, rect_earth) # earth
    screen.blit(img_saturn, rect_saturn) # saturn
    screen.blit(img_moon, rect_moon) # moon
    screen.blit(img_titan, rect_titan) # titan

    if np.abs(targetXY[0] - rect_ship.center[0]) < 100:
        targetXY = [np.random.randint(WINDOW_WIDTH), np.random.randint(WINDOW_HEIGHT)]
    screen.blit(img_ship, rect_ship) # ship

    # 화면 업데이트
    pygame.display.flip()
    clock.tick(60)
    frameTime += 1

# 게임 종료
pygame.quit()