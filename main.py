import pygame
import cProfile
import pstats

from object_3d import *
from perspective import *
from projection import *


app_name = 'MeineHandwerk'
fps = 120
initial_position = [0.5, 5.5, 5]
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
        self.__crosshair = pygame.image.load('assets/crosshair.png')
        self.__object = None
        self.__perspective = None
        self.__projector = None
        self.set_perspective()
        self.set_projector()
        self.create_objects()

    def get_center(self):
        return self.__center

    def get_screen(self):
        return self.__screen

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

    def set_projector(self):
        self.__projector = Projection(self)

    def set_perspective(self):
        self.__perspective = Perspective(self, initial_position)

    def create_objects(self):
        self.__object = Cube(self, [0.5, 6.5, 12], radius)

    def __draw(self):
        self.__screen.fill(pygame.Color('darkslategray'))
        self.__object.draw()

    def __draw_crosshair(self):
        self.__screen.blit(self.get_crosshair(), self.get_center())

    def run(self):
        while True:
            self.__draw()
            self.__perspective.control()
            self.__draw_crosshair()
            [exit() for i in pygame.event.get() if i.type == pygame.QUIT]
            pygame.display.set_caption(app_name)
            pygame.display.flip()
            self.__clock.tick(self.__fps)


if __name__ == '__main__':
    app = Renderer()
    app.run()
