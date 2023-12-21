

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
initial_position = [0.5, 0, 0]
radius = 2
width, height = 1540, 866


class Renderer:
    def __init__(self):
        pygame.init()
        pygame.mouse.set_visible(False)
        self.__resolution = self.__width, self.__height = width, height
        self.__center = self.__width // 2, self.__height // 2
        self.__fps = fps
        self.__screen = pygame.display.set_mode(self.__resolution)

        self.__clock = pygame.time.Clock()

        self.__crosshair = pygame.image.load('assets/pictures/crosshair.png').convert_alpha()
        self.__sky = pygame.image.load('assets/pictures/sky.jpg').convert()

        self.__objects = []
        self.__perspective = None
        self.__projector = None
        self.set_map()
        self.set_perspective()
        self.set_projector()
        self.create_object([-4.5, 5.5, 25], stone.convert_alpha())
        self.create_object([1.5, 5.5, 25], stone.convert_alpha())
        self.create_object([7.5, 5.5, 25], stone.convert_alpha())
        self.create_object([13.5, 5.5, 25], stone.convert_alpha())
        self.create_object([19.5, 5.5, 25], stone.convert_alpha())
        self.create_object([25.5, 5.5, 25], stone.convert_alpha())

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

    def __get_clock(self):
        return self.__clock

    def get_sky(self):
        return self.__sky

    def get_map(self):
        return self.__map

    def get_radius(self):
        return radius

    def get_cubes(self):
        return self.__objects

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
        self.__show_fps()

    def __draw_crosshair(self):
        self.__screen.blit(self.get_crosshair(), np.array(self.get_center()) - np.array(self.get_crosshair().get_size()) / 2)

    def __draw_sky(self):
        self.__screen.blit(self.get_sky(), (0, 0))

    def __show_fps(self):
        fps = round(self.__get_clock().get_fps())
        font = pygame.font.Font("assets/fonts/28DaysLater.ttf", 24)
        fps_text = font.render(f"FPS {fps}", True, "white")
        self.__screen.blit(fps_text, (10, 15))


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
    cProfile.run("app.run()", filename="stats/output.dat")

    with open("stats/output_time.txt", "w") as f:
        p = pstats.Stats("stats/output.dat", stream=f)
        p.sort_stats("time").print_stats()

    with open("stats/output_calls.txt", "w") as f:
        p = pstats.Stats("stats/output.dat", stream=f)
        p.sort_stats("calls").print_stats()
