import math
import numpy as np


class Projection:
    def __init__(self, renderer):
        focal = renderer.get_perspective().get_focal()
        alpha, beta = renderer.get_perspective().get_alpha(), renderer.get_perspective().get_beta()

        u0, v0 = renderer.get_width() // 2, renderer.get_height() // 2
        self.__K = np.array([
            [focal * alpha, 0, u0],
            [0, focal * beta, v0]
        ])

    def get_screen_matrix(self):
        return self.__K
