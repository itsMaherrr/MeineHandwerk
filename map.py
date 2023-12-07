import pygame
import numpy as np

from transformation_matrices import *
from perspective import project_points
from texture import draw_quad

shape = np.array([10, 10])
cell_size = np.array([5, 5])
y = 8.5

CLOSE = 0
FAR = 1


def generate_ground_cells(shape, cell_size, y):
    x_size, z_size = shape
    x = np.arange(-np.ceil(x_size / 2), np.ceil(x_size / 2)).astype(np.int32)
    z = np.arange(-np.ceil(z_size / 2), np.ceil(z_size / 2)).astype(np.int32)
    edges = np.array([
        [[i, j], [i, j + 1], [i + 1, j + 1], [i + 1, j]]
        for j in z
        for i in x
    ])

    return np.insert(edges * cell_size, 1, y, axis=-1)


def get_limits(shape):
    x_size, z_size = shape
    return np.array([
        [-np.ceil(x_size / 2), np.ceil(x_size / 2) - 1],
        [-np.ceil(z_size / 2), np.ceil(z_size / 2) - 1]
    ]).astype(np.int32)


class Map:
    def __init__(self, renderer, texture, y=y, shape=shape, cell_size=cell_size):
        self.__limites = get_limits(shape)
        self.__renderer = renderer
        self.__texture = [pygame.transform.smoothscale(texture, (8, 8)), pygame.transform.smoothscale(texture, (4, 4))]
        self.__cell_size = cell_size
        self.__ground_cells = generate_ground_cells(shape, self.__cell_size, y)

    def get_ground_vertices(self):
        return self.__ground_cells

    def __get_texture(self, index):
        return self.__texture[index]

    def draw(self):
        self.screen_projection()

    def screen_projection(self):
        height, width = self.__renderer.get_resolution()

        position = self.__renderer.get_perspective().get_position()[:3]

        angle_x = self.__renderer.get_perspective().get_angle_x()
        angle_y = self.__renderer.get_perspective().get_angle_y()

        translated_vertices = self.get_ground_vertices() - position

        translated_vertices_x = translated_vertices @ rotate_y(angle_x)
        translated_vertices_f = translated_vertices_x @ rotate_x(angle_y)

        focal = self.__renderer.get_perspective().get_focal()

        translated_vertices_f = translated_vertices_f[np.all(translated_vertices_f[..., -1] >= 0, axis=1)]

        projected_vertices = project_points(translated_vertices_f)

        screen_ground_cells = np.einsum('ijk, kl -> ijl', projected_vertices,
                                 self.__renderer.get_projector().get_screen_matrix().T)

        for cell in screen_ground_cells:
            pygame.draw.polygon(self.__renderer.get_screen(), (0, 143, 0), cell)
            #draw_quad(self.__renderer.get_screen(), cell, self.__get_texture(CLOSE))

    def obstacle_at(self, position):
        pos_x, pos_y, pos_z = position

        # If on ground or on top of a cube (not done yet)
        return np.around(pos_y, decimals=1) == y

    def on_ground(self, position):
        pos_x, pos_y, pos_z = position
        return np.abs(pos_y - y) <= 0.15
