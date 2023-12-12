import pygame
from matrix_functions import *
from numba import njit


@njit(fastmath=True)
def any_func(arr, a, b):
    return np.any((arr == a) | (arr == b))


class Object3D:
    def __init__(self, render, vertices='', faces=''):
        self.render = render
        self.vertices = np.array(vertices)
        self.faces = faces
        self.xvelocity = 0
        self.yvelocity = 0
        self.zvelocity = 0
        self.color_faces = [(pygame.Color('purple'), face) for face in self.faces]
        

    
    def draw(self):
        self.screen_projection()
        
    #리지드바디 정의
    def RigidBody(self,gravity,isgravity,mass,iskinematic):
        self.isgravity = isgravity
        self.gravity = gravity
        self.mass = mass
        #중력 적용
        self.iskinematic = iskinematic

    #순간적인 힘을 통한 가속도 추가
    def Apply_Impulseforce(self,xforce,yforce,zforce):
        if(self.mass == 0):
            return False
        xacc = xforce/self.mass
        yacc = yforce/self.mass
        zacc = zforce/self.mass

        
        if self.iskinematic ==True:
                self.xvelocity += xacc 
                self.yvelocity += yacc 
                self.zvelocity += zacc 

    def velocity(self):
        #속도 적용
        if(self.iskinematic == True):
            for vertex in self.vertices:
                vertex[0] -= self.xvelocity 
            for vertex in self.vertices:
                vertex[1] -= self.yvelocity 
            for vertex in self.vertices:
                vertex[2] -= self.zvelocity 


    def screen_projection(self):
        vertices = self.vertices @ self.render.camera.camera_matrix()
        vertices = vertices @ self.render.projection.projection_matrix
        vertices /= vertices[:, -1].reshape(-1, 1)
        vertices[(vertices > 2) | (vertices < -2)] = 0
        vertices = vertices @ self.render.projection.to_screen_matrix
        vertices = vertices[:, :2]

        for index, color_face in enumerate(self.color_faces):
            color, face = color_face
            polygon = vertices[face]
            if not any_func(polygon, self.render.H_WIDTH, self.render.H_HEIGHT):
                pygame.draw.polygon(self.render.screen, color, polygon, 2)
                

        
        for vertex in vertices:
            if not any_func(vertex, self.render.H_WIDTH, self.render.H_HEIGHT):
                pygame.draw.circle(self.render.screen, pygame.Color('white'), vertex, 2)

    def translate(self, pos):
        self.vertices = self.vertices @ translate(pos)

    def scale(self, scale_to):
        self.vertices = self.vertices @ scale(scale_to)

    def rotate_x(self, angle):
        self.vertices = self.vertices @ rotate_x(angle)

    def rotate_y(self, angle):
        self.vertices = self.vertices @ rotate_y(angle)

    def rotate_z(self, angle):
        self.vertices = self.vertices @ rotate_z(angle)
    

