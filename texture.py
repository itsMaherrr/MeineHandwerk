import pygame

stone = pygame.image.load('textures/stone.png')
floor = pygame.image.load('textures/floor.jpg')


def __lerp(p1, p2, f):
    return p1 + f * (p2 - p1)


def __lerp2d(p1, p2, f):
    return tuple(__lerp(p1[i], p2[i], f) for i in range(2))


def draw_quad(surface, quad, img):
    points = dict()

    for i in range(img.get_size()[1] + 1):
        b = __lerp2d(quad[1], quad[2], i / img.get_size()[1])
        c = __lerp2d(quad[0], quad[3], i / img.get_size()[1])
        for u in range(img.get_size()[0] + 1):
            a = __lerp2d(c, b, u / img.get_size()[0])
            points[(u, i)] = a

    for x in range(img.get_size()[0]):
        for y in range(img.get_size()[1]):
            pygame.draw.polygon(
                surface,
                img.get_at((x, y)),
                [points[(a, b)] for a, b in [(x, y), (x, y + 1), (x + 1, y + 1), (x + 1, y)]]
            )
