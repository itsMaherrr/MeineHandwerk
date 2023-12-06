import pygame as pg
import numpy as np


def rotate(cube):
    pass

def save_surfaces(points):
    print('points', points)

def draw_cube(cube, f, k):
    transformed = cube
    save_surfaces(transformed)
    points_2d = np.dot(k, point_transformat(transformed, f).T)
    print('2D points', points_2d)


def point_generator(center, size):
    center = np.array(center)
    half_size = size / 2.0

    vertices = np.array([
        [-half_size, -half_size, -half_size],  # Front bottom left
        [half_size, -half_size, -half_size],  # Front bottom right
        [half_size, half_size, -half_size],  # Front top right
        [-half_size, half_size, -half_size],  # Front top left
        [-half_size, -half_size, half_size],  # Back bottom left
        [half_size, -half_size, half_size],  # Back bottom right
        [half_size, half_size, half_size],  # Back top right
        [-half_size, half_size, half_size]  # Back top left
    ])

    vertices += center

    return vertices


def point_transformat(points, f):
    points_x = points[..., 0]
    points_y = points[..., 1]
    points_z = (points[..., 2] - f)
    for point in points_z:
        if point == 0:
            point += 1e-4

    return np.column_stack((points_x / points_z, points_y / points_z, np.ones(len(points))))


def main():
    cube = [
        {'center': (0, 0, 0),
         'points': point_generator((0, 0, 0), 2),
         'color': (255, 255, 10)
         },
        {'center': (-2, 0, 0),
         'points': point_generator((-2, 0, 0), 2),
         'color': (50, 50, 50)
         }]

    player = [0, 0, -2]

    pg.init()
    f = 0.5
    alpha = 100
    beta = 100
    W, H = 600, 600
    u0 = W // 2
    v0 = H // 2
    k = np.array([[f * alpha, 0, u0], [0, f * beta, v0]])
    screen = pg.display.set_mode((W, H))

    for c in cube:
        draw_cube(c.get('points'), f, k)

    running = True
    while running:
        for event in pg.event.get():
            pass
        screen.fill((0, 0, 0))



if __name__ == '__main__':
    center = (0, 0, 0)
    cube_size = 4
    print(point_generator(center, cube_size))
    main()