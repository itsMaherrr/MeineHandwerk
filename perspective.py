import pygame
import numpy as np
from transformation_matrices import *

focal = 3
alpha = beta = 100
moving_speed = 0.05
rotation_speed = 0.01
mouse_sensitivity = 0.002


@staticmethod
def project_points(points):
    points_z = points[..., 2][..., None]
    points_z[points_z < 1e-1] = 1e-1
    return points / points_z


class Perspective:
    def __init__(self, renderer, position):
        self.__renderer = renderer
        self.__position = np.array([*position])
        self.__u, self.__v, self.__k = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        self.__focal = focal
        self.__alpha = alpha
        self.__beta = beta
        self.__moving_speed = moving_speed
        self.__rotation_speed = rotation_speed

        self.__angle_v = 0
        self.__angle_h = 0

    def control(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_d]:
            print(self.__moving_speed * move_a_d(self.__angle_h))
            self.__position += self.__moving_speed * move_a_d(self.__angle_h)
        if key[pygame.K_q]:
            self.__position -= self.__moving_speed * move_a_d(self.__angle_h)
        if key[pygame.K_s]:
            self.__position -= self.__moving_speed * move_w_s(self.__angle_h)
        if key[pygame.K_z]:
            self.__position += self.__moving_speed * move_w_s(self.__angle_h)
        if key[pygame.K_LCTRL]:
            self.__position += self.__v * self.__moving_speed
        if key[pygame.K_SPACE]:
            self.__position -= self.__v * self.__moving_speed

        if key[pygame.K_RIGHT]:
            self.__angle_h += self.__rotation_speed
        if key[pygame.K_LEFT]:
            self.__angle_h -= self.__rotation_speed
        if key[pygame.K_UP]:
            self.__angle_v += self.__rotation_speed
        if key[pygame.K_DOWN]:
            self.__angle_v -= self.__rotation_speed

        dx, dy = pygame.mouse.get_rel()

        mouse_pos = pygame.mouse.get_pos()
        screen_center = self.__renderer.get_center()

        if mouse_pos != screen_center:
            self.__angle_h += dx * mouse_sensitivity
            self.__angle_v -= dy * mouse_sensitivity
            self.__angle_v = max(min(self.__angle_v, 90), -90)

            pygame.mouse.set_pos(screen_center)

    def get_position(self):
        return self.__position

    def get_focal(self):
        return self.__focal

    def get_alpha(self):
        return self.__alpha

    def get_beta(self):
        return self.__beta

    def translation_matrix(self):
        x, y, z, w = self.__position
        return np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [-x, -y, -z, 1]
        ])

    def get_angle_y(self):
        return self.__angle_v

    def get_angle_x(self):
        return self.__angle_h

    def rotation_matrix(self):
        ux, uy, uz = self.__u[:3]
        vx, vy, vz = self.__v[:3]
        kx, ky, kz = self.__k[:3]
        return np.array([
            [ux, vx, kx, 0],
            [uy, vy, ky, 0],
            [uz, vz, kz, 0],
            [0, 0, 0, 1]
        ])
