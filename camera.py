from matrix_functions import *
import pygame

class Camera:
    def __init__(self,render,position):
        self.render = render 
        self.position = np.array([*position,1.0])
        self.forward = np.array([0,0,1,1])
        self.up = np.array([0,1,0,1])
        self.right = np.array([1,0,0,1])
        self.h_fov = math.pi /3
        self.v_fov = self.h_fov *(render.height / render.width)
        self.near_plane = 0.1
        self.far_plane = 100
        self.moving_speed = 0.3
        self.rotate_speed = 0.008
        self.anglePitch = 0
        self.angleYaw = 0

    def control(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_w]:
            self.position += self.forward * self.moving_speed
        if key[pygame.K_a]:
            self.position -= self.right * self.moving_speed
        if key[pygame.K_s]:
            self.position -= self.forward * self.moving_speed
        if key[pygame.K_d]:
            self.position += self.right * self.moving_speed
        if key[pygame.K_SPACE]:
            self.position += self.up * self.moving_speed
        if key[pygame.K_LSHIFT]:
            self.position -= self.up * self.moving_speed    
        if key[pygame.K_q]:
            self.camera_y(-self.rotate_speed)
        if key[pygame.K_e]:
            self.camera_y(self.rotate_speed)
        if key[pygame.K_r]:
            self.camera_x(-self.rotate_speed)
        if key[pygame.K_f]:
            self.camera_x(self.rotate_speed)

    def camera_y(self, angle):
        self.angleYaw += angle

    def camera_x(self, angle):
        self.anglePitch += angle
   

    def camera_update_axii(self):
        rotate = rotate_x(self.anglePitch) @ rotate_y(self.angleYaw)  # this concatenation gives right visual
        self.forward = np.array([0, 0, 1, 1])
        self.up = np.array([0, 1, 0, 1])
        self.right = np.array([1, 0, 0, 1])
        self.forward = self.forward @ rotate
        self.right = self.right @ rotate
        self.up = self.up @ rotate

    def camera_matrix(self):
        self.camera_update_axii()
        return self.translate_matrix() @ self.rotate_matrix()
    

    def translate_matrix(self):
        x,y,z,w = self.position
        return np.array([
            [1,0,0,0],
            [0,1,0,1],
            [0,0,1,0],
            [-x,-y,-z,1]
        ])
    
    def rotate_matrix(self):
        rx,ry,rz,w = self.right
        fx,fy,fz,w = self.forward
        ux,uy,uz,w = self.up
        return np.array([
            [rx, ux, fx, 0],
            [ry, uy, fy, 0],
            [rz, uz, fz, 0],
            [0, 0, 0, 1]
        ])