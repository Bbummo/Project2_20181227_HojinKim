## 20181227 HojinKim ##
## Translation/Rotation of Pivot/Anchor - Clock ##
# Project 2: A Clock

## - Defined Value --------------------------------------------##
import pygame
import os
import numpy as np
import datetime

## - Defined Variable -----------------------------------------##
# Window info
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

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
class Needle:
    def __init__(self, _pointArr, _pivotPoint, _color):
        pointArr_temp = _pointArr.copy()
        for arr in pointArr_temp:
            arr.append(1)
        self.pointArr_ = np.array(pointArr_temp).T # modified
        pivotPoint_temp = _pivotPoint.copy()
        pivotPoint_temp.append(1)
        self.pivotPoint_ = np.array(pivotPoint_temp).T
        self.color = _color
    
    def rotate(self, _degree, _pivotPoint):
        H = Tmat(_pivotPoint[0], _pivotPoint[1]) @ Rmat(_degree) @ Tmat(-_pivotPoint[0], -_pivotPoint[1])
        self.pointArr_ = H @ self.pointArr_
        self.pivotPoint_ = H @ self.pivotPoint_

    def draw(self, _screen):
        pygame.draw.polygon(_screen, self.color, self.pointArr_[:2].T, 0)
        pygame.draw.circle(_screen, (0,0,0), self.pivotPoint_[:2], 5)

class Shape_Regular:
    def __init__(self, _edge, _radius, _color):
        self.pointArr = [] # original
        self.edge = _edge
        self.radius = _radius
        self.color = _color

        radius = self.radius
        for i in range(self.edge):
            deg = i * 360. / self.edge
            radian = deg * np.pi / 180
            c = np.cos(radian)
            s = np.sin(radian)
            x = radius * c 
            y = radius * s
            self.pointArr.append([x,y])
        self.pointArr += np.array([wcX, wcY])

    def draw(self, _screen):
        for i in range(self.edge):
            pygame.draw.circle(_screen, self.color, self.pointArr[i], self.radius/20)
        pygame.draw.circle(_screen, self.color, [wcX, wcY], self.radius*1.2, 20)
        
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
fps = 60 # Frame per Second

## - Setup ----------------------------------------------------##
# Pygame 초기화
pygame.init()
info = pygame.display.Info()
pygame.display.set_caption("P2_clock_20181227_HojinKim")
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

# Asset path
assets_path = os.path.join(os.path.dirname(__file__), '_assets')

# Class init
wcX = WINDOW_WIDTH/2
wcY = WINDOW_HEIGHT/2

needle_second = Needle([[wcX,wcY+10], [wcX+10,wcY], [wcX+5,wcY-5], [wcX+5,wcY-205]
, [wcX,wcY-325], [wcX-5,wcY-205], [wcX-5,wcY-5], [wcX-10,wcY]]
, [wcX,wcY], GREEN)
needle_minute = Needle([[wcX,wcY+15], [wcX+15,wcY], [wcX+10,wcY-5], [wcX+15,wcY-125]
, [wcX,wcY-275], [wcX-15,wcY-125], [wcX-10,wcY-5], [wcX-15,wcY]]
, [wcX,wcY], BLUE)
needle_hour = Needle([[wcX,wcY+20], [wcX+20,wcY], [wcX+10,wcY-10], [wcX+20,wcY-55]
, [wcX,wcY-175], [wcX-20,wcY-55], [wcX-10,wcY-10], [wcX-20,wcY]]
, [wcX,wcY], RED)
body = Shape_Regular(12, 300, BLACK)

# Rotation speed
speed_second = 360. / fps / 60
speed_minute = 360. / fps / 60 / 60
speed_hour = 360. / fps / 60 / 60 / 60

# Initial Time/Rotation
now = datetime.datetime.now()
h,m,s = now.hour, now.minute, now.second
init_second = 360.0 * s/60.0
init_minute = 360.0 * (m + s/60.0)/60.0
init_hour = 360.0 * (h + m/60.0 + s/60.0)/12.0
needle_second.rotate(init_second, np.array([wcX,wcY]))
needle_minute.rotate(init_minute, np.array([wcX,wcY]))
needle_hour.rotate(init_hour, np.array([wcX,wcY]))

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
    screen.fill(WHITE)

    # Rotation adjust
    needle_second.rotate(speed_second, np.array([wcX,wcY]))
    needle_minute.rotate(speed_minute, np.array([wcX,wcY]))
    needle_hour.rotate(speed_hour, np.array([wcX,wcY]))

    # Draw
    body.draw(screen)
    needle_hour.draw(screen)
    needle_minute.draw(screen)
    needle_second.draw(screen)

    # 화면 업데이트
    pygame.display.flip()
    clock.tick(fps)

# 게임 종료
pygame.quit()