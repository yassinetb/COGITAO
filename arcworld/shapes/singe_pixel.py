import numpy as np

from arcworld.shapes.base import BasicShape


class Single_Pixel(BasicShape):

    def __init__(self, max_n_rows,
                 max_n_cols,
                 color_pattern=None,
                 color=None):
        super().__init__(max_n_rows=None,
                         max_n_cols=None,
                         color_pattern=None)

        self.no_black_pixels = 1

        if color is None:
            self.color = np.random.randint(self.no_black_pixels, 10)
        else:
            self.color = color

        self.grid = self.generate()

    def generate(self):
        return np.array([[self.color]])
