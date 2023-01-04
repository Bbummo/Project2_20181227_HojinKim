## 20181227 HojinKim ##
## Translation/Rotation of Pivot/Anchor - Windmill ##
# Project 2: A Windmill

## - Defined Value --------------------------------------------##
import pygame
import os
import numpy as np

## - Defined Variable -----------------------------------------##
# Window info
WINDOW_WIDTH = 1200
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
class Wing:
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

class Body:
    def __init__(self, _pointArr, _anchorPoint, _color):
        pointArr_temp = _pointArr.copy()
        for arr in pointArr_temp:
            arr.append(1)
        self.pointArr_ = np.array(pointArr_temp).T # modified
        anchorPoint_temp = _anchorPoint.copy()
        anchorPoint_temp.append(1)
        self.anchorPoint_ = np.array(anchorPoint_temp).T
        self.color = _color

    def draw(self, _screen):
        pygame.draw.polygon(_screen, self.color, self.pointArr_[:2].T, 0)
        pygame.draw.circle(_screen, (0,0,0), self.anchorPoint_[:2], 5)

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
windSpeed = 1.0

## - Setup ----------------------------------------------------##
# Pygame 초기화
pygame.init()
info = pygame.display.Info()
pygame.display.set_caption("P2_windmill_20181227_HojinKim")
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

# Class init
windmill1_body = Body([[750,700],[700,400],[650,350]
,[550,350],[500,400],[450,700]], [600,400], GREY)
windmill1_wingArr = []
windmill1_num = 4
for i in range(windmill1_num):
    tempWing = Wing([[600,150],[550,170],[550,330],[580,350]
    ,[600,400],[620,350],[650,330],[650,170]]
    , windmill1_body.anchorPoint_.tolist()[:2], [int(255*i/3),0,0])
    tempWing.rotate(360/windmill1_num*i, windmill1_body.anchorPoint_[:2])
    windmill1_wingArr.append(tempWing)

windmill2_body = Body([[230,700],[250,500],[270,450]
,[330,450],[350,500],[370,700]], [300,500], GREY)
windmill2_wingArr = []
windmill2_num = 6
for i in range(windmill2_num):
    tempWing = Wing([[300,500],[320,425],[300,350],[250,320]
    ,[250,430],[290,450]]
    , windmill2_body.anchorPoint_.tolist()[:2], [0,int(255*i/5),0])
    tempWing.rotate(360/windmill2_num*i, windmill2_body.anchorPoint_[:2])
    windmill2_wingArr.append(tempWing)

windmill3_body = Body([[830,700],[850,500],[870,450]
,[930,450],[950,500],[970,700]], [900,500], GREY)
windmill3_wingArr = []
windmill3_num = 5
for i in range(windmill3_num):
    tempWing = Wing([[900,500],[910,460],[930,450],[920,400],[930,350]
    ,[900,330],[870,350],[880,400],[870,450],[890,460]]
    , windmill3_body.anchorPoint_.tolist()[:2], [0,0,int(255*i/4)])
    tempWing.rotate(360/windmill3_num*i, windmill3_body.anchorPoint_[:2])
    windmill3_wingArr.append(tempWing)

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
    screen.fill((100, 200, 255))

    # Rotation adjust
    if frameTime % 180 == 0: # change windspeed for every 3 seconds
        windSpeed = np.random.uniform(0,5)

    for wing1 in windmill1_wingArr:
        wing1.rotate(windSpeed, windmill1_body.anchorPoint_[:2])
    for wing2 in windmill2_wingArr:
        wing2.rotate(windSpeed, windmill2_body.anchorPoint_[:2])
    for wing3 in windmill3_wingArr:
        wing3.rotate(windSpeed, windmill3_body.anchorPoint_[:2])

    # Draw
    windmill3_body.draw(screen)
    for wing3 in windmill3_wingArr:
        wing3.draw(screen)
    windmill2_body.draw(screen)
    for wing2 in windmill2_wingArr:
        wing2.draw(screen)
    windmill1_body.draw(screen)
    for wing1 in windmill1_wingArr:
        wing1.draw(screen)

    pygame.draw.rect(screen, (100,180,10), (0,700,1200,100), 0)

    # 화면 업데이트
    pygame.display.flip()
    clock.tick(60)
    frameTime += 1

# 게임 종료
pygame.quit()