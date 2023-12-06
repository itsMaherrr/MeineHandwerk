import numpy as np


def translate(pos):
    tx, ty, tz = pos
    return np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [tx, ty, tz, 1]
    ])


def rotate_x(theta):
    return np.array([
        [1, 0, 0],
        [0, np.cos(theta), -np.sin(theta)],
        [0, np.sin(theta), np.cos(theta)]
    ])


def rotate_y(theta):
    return np.array([
        [np.cos(theta), 0, np.sin(theta)],
        [0, 1, 0],
        [-np.sin(theta), 0, np.cos(theta)],
    ])


def move_a_d(theta):
    return np.array([
        np.cos(theta), 0, -np.sin(theta)
    ])


def move_w_s(theta):
    return np.array([
        np.sin(theta), 0, np.cos(theta)
    ])


def scale(coef):
    return np.array([
        [coef, 0, 0, 0],
        [0, coef, 0, 0],
        [0, 0, coef, 0],
        [0, 0, 0, 1]
    ])
