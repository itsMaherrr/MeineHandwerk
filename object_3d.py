import numpy as np
import pygame.draw

from transformation_matrices import *
from perspective import project_points

FBL = 0
FTL = 1
FTR = 2
FBR = 3
BBL = 4
BTL = 5
BTR = 6
BBR = 7


def create_cube_vertices(center, radius):
    return np.array([
        [-radius, -radius, -radius],
        [-radius, radius, -radius],
        [radius, radius, -radius],
        [radius, -radius, -radius],
        [-radius, -radius, radius],
        [-radius, radius, radius],
        [radius, radius, radius],
        [radius, -radius, radius]
    ]) + center


class Cube:
    def __init__(self, renderer, position, radius):
        self.__renderer = renderer
        self.__vertices = create_cube_vertices(position, radius)
        self.__faces = np.array([(FBL, FTL, FTR, FBR), (BBL, BTL, BTR, BBR), (FBL, BBL, BTL, FTL),
                                 (FBR, BBR, BTR, FTR), (FBL, FBR, BBR, BBL), (FTL, FTR, BTR, BTL)])

    def draw(self):
        self.screen_projection()

    def screen_projection(self):
        position = self.__renderer.get_perspective().get_position()[:3]

        angle_x = self.__renderer.get_perspective().get_angle_x()
        angle_y = self.__renderer.get_perspective().get_angle_y()

        translated_vertices = self.__vertices - position

        translated_vertices = translated_vertices @ rotate_x(angle_x)
        translated_vertices = translated_vertices @ rotate_y(angle_y)

        #faces = np.array(sorted(translated_vertices[self.__faces],
        #               key=lambda g: np.linalg.norm(position - np.mean(g, axis=0)))[:3])

        position_z = self.__renderer.get_perspective().get_position()[-1]

        sorted_faces = np.linalg.norm(position - np.mean(translated_vertices[translated_vertices[..., -1] > position_z, self.__faces], axis=1), axis=1)
        apparent_faces = np.argsort(sorted_faces[sorted_faces > self.__renderer.get_perspective().get_focal()])[:3]

        projected_vertices = project_points(translated_vertices)

        screen_faces = np.einsum('ijk, kl -> ijl', projected_vertices[self.__faces[apparent_faces]],
                                    self.__renderer.get_projector().get_screen_matrix().T)

        # get rotation matrices in x and y axis with the angle
        # vertices = self.__vertices @ self.__renderer.get_perspective().camera_matrix()
        # vertices = vertices @ self.__renderer.get_projector().get_projection_matrix()
        # divisor = vertices[:, -1]
        # divisor[divisor == 0] = 1e-4
        # vertices /= divisor.reshape(-1, 1)
        # vertices[(vertices > 2) | (vertices < -2)] = 0
        # vertices = vertices @ self.__renderer.get_projector().get_screen_matrix()
        # vertices = vertices[:, :2]

        colors = {0: (255, 0, 0), 1: (0, 255, 0), 2: (0, 0, 255), 3: (255, 255, 0), 4: (255, 0, 255),
                  5: (128, 128, 128)}

        i = 0
        for face in screen_faces:
            pygame.draw.polygon(self.__renderer.get_screen(), colors[i], face)
            i += 1
            #face = faces[i]
            #polygon = screen_vertices[face]
            #index = np.where(np.all(self.__faces == face, axis=1))[0][0]
            #color = colors.get(index)
            #i += 1
            #if not np.any((polygon == self.__renderer.get_height()) | (polygon == self.__renderer.get_width())):
            #    print(polygon)
            #    pygame.draw.polygon(self.__renderer.get_screen(), color, polygon)

    def translate(self, pos):
        self.__vertices = self.__vertices @ translate(pos)

    def scale(self, coef):
        self.__vertices = self.__vertices @ scale(coef)

    def rotate_x(self, angle):
        self.__vertices = self.__vertices @ rotate_x(angle)

    def rotate_y(self, angle):
        self.__vertices = self.__vertices @ rotate_y(angle)
