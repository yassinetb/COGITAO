import numpy as np

from arcworld.shapes.base import BasicShape


class Diamond(BasicShape):
    def __init__(self,
                 max_n_rows,
                 max_n_cols,
                 color_pattern,
                 color=None):
        super(Diamond, self).__init__(
            max_n_rows=max_n_rows,
            max_n_cols=max_n_cols,
            color_pattern=color_pattern,
        )

        if max_n_rows < 3 or max_n_cols < 3:
            print('not possible to draw a diamond becuase grid side is too small')
            self.diamond = np.zeros((1, 1))

        self.max_n_rows = max_n_rows
        self.max_n_cols = max_n_cols

        if color_pattern is None:
            color_pattern = np.random.choice(
                ['uniform', 'first_diagonal_symmetry', 'second_diagonal_symmetry', 'vertical_symmetry', 'random'])

        if color_pattern not in ['uniform', 'first_diagonal_symmetry', 'second_diagonal_symmetry', 'vertical_symmetry',
                                 'random']:
            color_pattern = 'uniform'

        self.color_pattern = color_pattern

        if color is None:
            color = np.random.randint(1, 10)

        self.color = color
        self.no_black_pixels = 1  # If True, then no black pixels are added in the rectangle
        self.grid = self.generate()


    def generate(self):

        shape = np.zeros((3, 3))

        if self.color_pattern == 'uniform':
            col = np.random.randint(self.no_black_pixels, 10)

            shape[0, 1] = col
            shape[1, 0] = col
            shape[1, 2] = col
            shape[2, 1] = col

        if self.color_pattern == 'first_diagonal_symmetry':

            col1 = np.random.randint(self.no_black_pixels, 10)
            col2 = col1
            while col2 == col1:
                col2 = np.random.randint(self.no_black_pixels, 10)

            shape[0, 1] = col1
            shape[1, 0] = col2
            shape[1, 2] = col1
            shape[2, 1] = col2

        if self.color_pattern == 'second_diagonal_symmetry':

            col1 = np.random.randint(self.no_black_pixels, 10)
            col2 = col1
            while col2 == col1:
                col2 = np.random.randint(self.no_black_pixels, 10)

            shape[0, 1] = col1
            shape[1, 0] = col1
            shape[1, 2] = col2
            shape[2, 1] = col2

        if self.color_pattern == 'vertical_symmetry':

            col1 = np.random.randint(self.no_black_pixels, 10)
            col2 = col1
            while col2 == col1:
                col2 = np.random.randint(self.no_black_pixels, 10)

            shape[0, 1] = col1
            shape[1, 0] = col2
            shape[1, 2] = col2
            shape[2, 1] = col1

        if self.color_pattern == 'random':
            shape[0, 1] = np.random.randint(self.no_black_pixels, 10)
            shape[1, 0] = np.random.randint(self.no_black_pixels, 10)
            shape[1, 2] = np.random.randint(self.no_black_pixels, 10)
            shape[2, 1] = np.random.randint(self.no_black_pixels, 10)

        return shape
