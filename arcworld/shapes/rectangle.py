import numpy as np
from arcworld.shapes.base import BasicShape
class Rectangle(BasicShape):

    def __init__(self,
                 max_n_rows,
                 max_n_cols,
                 color_pattern,
                 color=None,
                 shape_n_rows=-1,
                 shape_n_cols=-1,
                 max_shape_to_grid_ratio=1):
        super().__init__(
            max_n_rows=max_n_rows,
            max_n_cols=max_n_cols,
            color_pattern=color_pattern
        )

        self.shape_n_rows = shape_n_rows
        self.shape_n_cols = shape_n_cols
        self.max_shape_to_grid_ratio = max_shape_to_grid_ratio

        if self.shape_n_rows == -1 or self.shape_n_cols == -1:
            ## Scaling the generation by sqrt(max_ratio) to ensure that product of the two will be smaller than max_ratio * grid size!
            if self.shape_n_rows == -1:
                self.shape_n_rows = int(
                    np.floor(np.random.randint(2, 1 + self.max_n_rows) * np.sqrt(max_shape_to_grid_ratio)))
            if self.shape_n_cols == -1:
                self.shape_n_cols = int(
                    np.floor(np.random.randint(2, 1 + self.max_n_cols) * np.sqrt(max_shape_to_grid_ratio)))
        if color_pattern not in ['uniform', 'diag_symmetry', 'hor_symmetry', 'ver_symmetry', 'chessboard', 'ver_line',
                                 'hor_line', 'diag_line']:
            self.color_pattern = 'uniform'
        elif color_pattern == 'diag_symmetry' and self.shape_n_rows != self.shape_n_cols:
            self.color_pattern = 'uniform'  # does not make sense to talk about diagonal symmetry if the rectangle is not a square
        else:
            self.color_pattern = color_pattern

        self.no_black_pixels = 1  # if 1, then no black pixels will be added in the rectangle
        self.color = color

        grid = self.generate()

        self.grid = grid

    def generate(self):  # modify the grid to create the rectangle

        # upper_left_x_coordinate: coordinate of upper_left corner of the rectangle

        if self.color_pattern == 'uniform':
            return self.uniform_coloring()

        if self.color_pattern == 'ver_symmetry':
            return self.ver_symmetry_coloring()

        if self.color_pattern == 'hor_symmetry':
            return self.hor_symmetry_coloring()

        if self.color_pattern == 'diag_symmetry':
            return self.diag_symmetry_coloring()

        if self.color_pattern == 'chessboard':
            return self.chessboard_coloring()

        if self.color_pattern == 'ver_line':
            return self.ver_line_coloring()

        if self.color_pattern == 'hor_line':
            return self.hor_line_coloring()

        if self.color_pattern == 'diag_line':
            return self.diag_line_coloring()

    def uniform_coloring(self):

        shape = np.zeros((self.shape_n_rows, self.shape_n_cols))
        if self.color is None:
            self.color = np.random.randint(self.no_black_pixels, 10, size=1)
        shape = self.color * np.ones((self.shape_n_rows, self.shape_n_cols))
        return shape

    def ver_symmetry_coloring(self):

        shape = np.zeros((self.shape_n_rows, self.shape_n_cols))

        if self.shape_n_rows % 2 == 0:
            col1 = np.random.randint(self.no_black_pixels, 10, size=1)
            col2 = col1
            while col2 == col1:
                col2 = np.random.randint(self.no_black_pixels, 10, size=1)

            mask1 = np.array(range(self.shape_n_rows)) < self.shape_n_rows / 2
            mask2 = np.array(range(self.shape_n_rows)) >= self.shape_n_rows / 2

            shape[mask1, :] = col1
            shape[mask2, :] = col2

        else:
            col1 = np.random.randint(self.no_black_pixels, 10, size=1)
            col2 = col1
            while col2 == col1:
                col2 = np.random.randint(self.no_black_pixels, 10, size=1)

            col3 = col2

            while col3 == col2 or col3 == col1:
                col3 = np.random.randint(self.no_black_pixels, 10, 1)

            mask1 = np.array(range(self.shape_n_rows)) < int(self.shape_n_rows / 2)
            mask2 = np.array(range(self.shape_n_rows)) > int(self.shape_n_rows / 2)
            mask3 = np.array(range(self.shape_n_rows)) == int(self.shape_n_rows / 2)

            shape[mask1, :] = col1
            shape[mask2, :] = col2
            shape[mask3, :] = col3

        return shape

    def hor_symmetry_coloring(self):

        shape = np.zeros((self.shape_n_rows, self.shape_n_cols))

        if self.shape_n_rows % 2 == 0:
            col1 = np.random.randint(self.no_black_pixels, 10, size=1)
            col2 = col1
            while col2 == col1:
                col2 = np.random.randint(self.no_black_pixels, 10, size=1)

            mask1 = np.array(range(self.shape_n_cols)) < self.shape_n_cols / 2
            mask2 = np.array(range(self.shape_n_cols)) >= self.shape_n_cols / 2

            shape[:, mask1] = col1
            shape[:, mask2] = col2

        else:
            col1 = np.random.randint(self.no_black_pixels, 10, size=1)
            col2 = col1
            while col2 == col1:
                col2 = np.random.randint(self.no_black_pixels, 10, size=1)
            col3 = col2

            while col3 == col2 or col3 == col1:
                col3 = np.random.randint(self.no_black_pixels, 10, 1)

            mask1 = np.array(range(self.shape_n_cols)) < int(self.shape_n_cols / 2)
            mask2 = np.array(range(self.shape_n_cols)) > int(self.shape_n_cols / 2)
            mask3 = np.array(range(self.shape_n_cols)) == int(self.shape_n_cols / 2)

            shape[:, mask1] = col1
            shape[:, mask2] = col2
            shape[:, mask3] = col3

        return shape

    def diag_symmetry_coloring(self):

        shape = np.zeros((self.shape_n_rows, self.shape_n_cols))

        col1 = np.random.randint(self.no_black_pixels, 10, size=1)
        col2 = col1
        while col2 == col1:
            col2 = np.random.randint(self.no_black_pixels, 10, size=1)
        col3 = col2

        while col3 == col2 or col3 == col1:
            col3 = np.random.randint(self.no_black_pixels, 10, 1)

        shape[np.tril_indices(self.shape_n_rows, k=1)] = col1
        shape[np.triu_indices(self.shape_n_rows, k=1)] = col2
        shape[np.diag_indices(self.shape_n_rows)] = col3

        return shape

    def chessboard_coloring(self):

        shape = np.zeros((self.shape_n_rows, self.shape_n_cols))

        col1 = np.random.randint(self.no_black_pixels, 10, size=1)
        col2 = col1
        while col2 == col1:
            col2 = np.random.randint(self.no_black_pixels, 10, size=1)

        for i in range(self.shape_n_rows):
            for j in range(self.shape_n_cols):
                if (i + j) % 2 == 0:
                    shape[i, j] = col1
                else:
                    shape[i, j] = col2

        return shape

    def hor_line_coloring(self):

        shape = np.zeros((self.shape_n_rows, self.shape_n_cols))

        col1 = np.random.randint(self.no_black_pixels, 10, size=1)
        col2 = col1
        while col2 == col1:
            col2 = np.random.randint(self.no_black_pixels, 10, size=1)

        line_index = np.random.randint(0, self.shape_n_rows, size=1)  # randomly selects which line to draw differently

        shape = col1 * np.ones((self.shape_n_rows, self.shape_n_cols))
        shape[line_index, :] = col2

        return shape

    def ver_line_coloring(self):

        shape = np.zeros((self.shape_n_rows, self.shape_n_cols))

        col1 = np.random.randint(self.no_black_pixels, 10, size=1)
        col2 = col1
        while col2 == col1:
            col2 = np.random.randint(self.no_black_pixels, 10, size=1)

        line_index = np.random.randint(0, self.shape_n_cols, size=1)

        shape = col1 * np.ones((self.shape_n_rows, self.shape_n_cols))
        shape[:, line_index] = col2

        return shape

    def diag_line_coloring(self):

        shape = np.zeros((self.shape_n_rows, self.shape_n_cols))

        col1 = np.random.randint(self.no_black_pixels, 10, size=1)
        col2 = col1
        while col2 == col1:
            col2 = np.random.randint(self.no_black_pixels, 10, size=1)

        shape = col1 * np.ones((self.shape_n_rows, self.shape_n_cols))

        min_val = min(self.shape_n_cols, self.shape_n_rows)

        for i in range(min_val):
            shape[i, i] = col2

        return shape
