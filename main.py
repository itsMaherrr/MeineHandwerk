

# Full Name : MEBIROUK Maher


import numpy as np
import pygame
import cProfile
import pstats

from object_3d import *
from perspective import *
from projection import *
from map import *
from texture import stone, floor


app_name = 'MeineHandwerk'
fps = 120
sun_position = [0, int(1e3), 0]
initial_position = [0.5, 5.5, 0]
radius = 3
height, width = 1600, 866


class Renderer:
    def __init__(self):
        pygame.init()
        pygame.mouse.set_visible(False)
        self.__resolution = self.__height, self.__width = height, width
        self.__center = self.__height // 2, self.__width // 2
        self.__fps = fps
        self.__screen = pygame.display.set_mode(self.__resolution)

        self.__clock = pygame.time.Clock()

        self.__crosshair = pygame.image.load('assets/crosshair.png').convert_alpha()
        self.__sky = pygame.image.load('assets/sky.jpg').convert()

        self.__objects = []
        self.__perspective = None
        self.__projector = None
        self.set_map()
        self.set_perspective()
        self.set_projector()
        self.create_object([0.5, 5.5, 25], stone.convert_alpha())
        self.create_object([9.5, 5.5, 25], stone.convert_alpha())
        self.create_object([15.5, 5.5, 25], stone.convert_alpha())
        self.create_object([21.5, 5.5, 25], stone.convert_alpha())
        self.create_object([27.5, 5.5, 25], stone.convert_alpha())
        self.create_object([33.5, 5.5, 25], stone.convert_alpha())

    def get_center(self):
        return self.__center

    def get_screen(self):
        return self.__screen

    def get_resolution(self):
        return self.__resolution

    def get_perspective(self):
        return self.__perspective

    def get_projector(self):
        return self.__projector

    def get_height(self):
        return self.__height

    def get_width(self):
        return self.__width

    def get_crosshair(self):
        return self.__crosshair

    def get_sky(self):
        return self.__sky

    def get_map(self):
        return self.__map

    def set_map(self):
        self.__map = Map(self, floor.convert())

    def set_projector(self):
        self.__projector = Projection(self)

    def set_perspective(self):
        self.__perspective = Perspective(self, initial_position)

    def create_object(self, center, texture, radius=radius):
        self.__objects.append(Cube(self, texture, center, radius))

    def __draw(self):
        self.__draw_sky()
        self.__map.draw()
        [cube.draw() for cube in sorted(self.__objects,
                                        key=lambda g: np.linalg.norm(g.get_center() - self.__perspective.get_position()),
                                        reverse=True)]
        self.__draw_crosshair()

    def __draw_crosshair(self):
        self.__screen.blit(self.get_crosshair(), self.get_center())

    def __draw_sky(self):
        self.__screen.blit(self.get_sky(), (0, 0))

    def run(self):
        while True:
            self.__draw()
            self.__perspective.control()
            [exit() for i in pygame.event.get() if i.type == pygame.QUIT]
            pygame.display.set_caption(app_name)
            pygame.display.flip()
            self.__clock.tick(self.__fps)


if __name__ == '__main__':
    app = Renderer()
    app.run()
