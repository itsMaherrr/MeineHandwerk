import pygame
import numpy as np
from transformation_matrices import *

focal = 4
alpha = beta = 100
moving_speed = 0.2
rotation_speed = np.pi / 180
mouse_sensitivity = 0.002
gravitational_pull = 0.2
height = 1.5


max_jump = 20


def project_points(points):
    #points[..., -1] -= focal
    points_z = points[..., -1][..., None]
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
        self.__height = height

        self.__angle_v = 0
        self.__angle_h = 0

        self.__jump = max_jump

    def control(self):
        key = pygame.key.get_pressed()
        position = self.__position.copy()
        if key[pygame.K_d]:
            position += self.__moving_speed * move_a_d(self.__angle_h)
        if key[pygame.K_q]:
            position -= self.__moving_speed * move_a_d(self.__angle_h)
        if key[pygame.K_s]:
            position -= self.__moving_speed * move_w_s(self.__angle_h)
        if key[pygame.K_z]:
            position += self.__moving_speed * move_w_s(self.__angle_h)
        if key[pygame.K_LCTRL]:
            position += self.__v * self.__moving_speed

        if not self.__renderer.get_map().obstacle_at(position):
            self.__position = position

        if key[pygame.K_SPACE]:
            if (self.__renderer.get_map().on_ground(self.get_position(), self.get_height() + gravitational_pull)
                or self.__renderer.get_map().is_above_cube(self.get_position(), gravitational_pull))\
                    and self.__jump == max_jump:
                if self.__jump == max_jump:
                    self.__jump = 0

        if self.__jump != max_jump:
            position = self.__position - self.__v * self.__moving_speed * 2
            if not self.__renderer.get_map().obstacle_at(position):
                self.__position = position
                self.__jump += 1

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

        self.fall_for_gravity()

    def fall_for_gravity(self):
        position = self.__position + self.__v * gravitational_pull

        # if nothing is intercepting player or not currently jumping
        if not self.__renderer.get_map().on_ground(position, self.get_height())\
                and self.__jump == max_jump\
                and not self.__renderer.get_map().obstacle_at(position):
            self.__position = position

    def can_move(self, new_position):
        pass

    def get_position(self):
        return self.__position

    def get_focal(self):
        return self.__focal

    def get_height(self):
        return self.__height

    def get_alpha(self):
        return self.__alpha

    def get_beta(self):
        return self.__beta

    def get_angle_y(self):
        return self.__angle_v

    def get_angle_x(self):
        return self.__angle_h