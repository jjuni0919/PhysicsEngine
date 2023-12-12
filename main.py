import pygame
import sys
import math
import numpy as np
from object_3d import*
from camera import*
from projection import*

# 초기화
pygame.init()
 # 시계 설정
clock = pygame.time.Clock()


class Rendering:
    def __init__(self):
        # 파이게임 창 생성
        self.width, self.height = 1800, 1000

        self.H_WIDTH = self.width
        self.H_HEIGHT = self.height
        #창 크기 설정
        self.screen = pygame.display.set_mode((self.width, self.height)) 
        #오브젝트 관련 정의
        self.objects()
        
        

    #시뮬에 들어가는 요소들
    def objects(self):
        #카메라 위치 조정
        self.camera = Camera(self,[15,0,-100])
        self.projection = Projection(self)
        #파일 열기
        self.object = self.get_object('resources/cat.obj')
        #리지드바디 추가
        self.object.RigidBody(0.01,False,1000,True)
        #크기 조정
        self.object.scale(0.1)
        #회전 조정
        self.object.rotate_y(90)
        
    #파일로부터 vertex,face값 읽어오기
    def get_object(self,filename):
        vertex , face = [],[]
        with open(filename) as f:
            for line in f:
                if line.startswith('v '):
                    vertex.append([float(i) for i in line.split()[1:]] + [1])
                    
                elif line.startswith('f'):
                    faces = line.split()[1:]
                    face.append([int(face_.split('/')[0]) - 1 for face_ in faces])
        
        return Object3D(self,vertex,face)
         
    #메인 루프 실행
    def Loop(self):
        while (True):
            self.screen.fill(pygame.Color('skyblue'))
            self.object.draw()
            self.camera.control()
            if(self.object.isgravity):
                self.object.yvelocity+=self.object.gravity
            
            self.object.velocity()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F1:
                        self.object.Apply_Impulseforce(180,0,0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F2:
                        self.object.Apply_Impulseforce(-200,0,0)

             # 초당 프레임 수 설정
            pygame.display.flip()
            clock.tick(60)
            
    
                
                
                
                
            

        
        
        

    
app = Rendering()

app.Loop()
