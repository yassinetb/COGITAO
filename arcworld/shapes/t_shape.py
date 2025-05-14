import numpy as np

from arcworld.shapes import StraightLine
from arcworld.shapes.base import BasicShape


class TShape(BasicShape):
    def __init__(self,
                 max_n_rows,
                 max_n_cols,
                 color_pattern=None,
                 orientation=None,
                 color_pattern_hor=None,
                 color_pattern_ver=None,
                 length_hor=None,
                 length_ver=None,
                 uniform_color=False,
                 displacement=-1):
        super().__init__(
            max_n_rows=max_n_rows,
            max_n_cols=max_n_cols,
            color_pattern=None
        )
        self.max_n_rows = max_n_rows
        self.max_n_cols = max_n_cols

        if self.max_n_rows <= 1 or self.max_n_cols <= 1:
            print('not possible to generate a T-shape-object')
            self.T_shape = np.zeros((1, 1))

        if orientation is None:
            orientation = np.random.choice(np.array([0, 90, 180, 270]), 1)  # 0 corresponds to vertical T

        if orientation not in [0, 90, 180, 270]:
            orientation = 0

        self.orientation = orientation

        if color_pattern_hor is None:
            color_pattern_hor = np.random.choice(['uniform', 'symmetric', 'alternated', 'random'])

        if color_pattern_hor not in ['uniform', 'symmetric', 'alternated', 'random']:
            self.color_pattern_hor = 'uniform'

        self.color_pattern_hor = color_pattern_hor

        if color_pattern_ver is None:
            color_pattern_ver = np.random.choice(['uniform', 'symmetric', 'alternated', 'random'])

        if color_pattern_ver not in ['uniform', 'symmetric', 'alternated', 'random']:
            self.color_pattern_ver = 'uniform'

        self.color_pattern_ver = color_pattern_ver

        if length_hor is None:
            length_hor = np.random.randint(1, max_n_cols + 1)
        if length_ver is None:
            length_ver = np.random.randint(1, max_n_rows)

        self.length_hor = length_hor
        self.length_ver = length_ver

        if max_n_cols <= self.length_hor:
            self.length_hor = self.max_n_cols

        if max_n_rows <= self.length_ver + 1:
            self.length_ver = max_n_rows - 1

        if displacement < 0 or displacement >= self.length_hor or displacement is None:
            if self.orientation == 0 or self.orientation == 180:
                displacement = np.random.randint(0, self.length_hor)
            else:
                displacement = np.random.randint(0, self.length_ver)

        # where we want to position the vertical bar wrt horizontal one
        self.displacement = displacement

        self.uniform_color = uniform_color

        self.no_black_pixels = 1

        self.grid = self.generate()

    def generate(self):

        if self.orientation == 0:

            tshape = np.zeros((self.length_ver + 1, self.length_hor))

            if self.uniform_color:
                color = np.random.randint(self.no_black_pixels, 10)
                tshape[0, :] = StraightLine(
                    self.max_n_rows,
                    self.max_n_cols,
                    orientation='horizontal',
                    color_pattern=self.color_pattern_hor,
                    length=self.length_hor,
                    color=color).grid[0, :]
                tshape[1::, self.displacement] = StraightLine(
                    self.max_n_rows,
                    self.max_n_cols,
                    orientation='vertical',
                    color_pattern=self.color_pattern_ver,
                    length=self.length_ver,
                    color=color).grid[:, 0]
            else:
                tshape[0, :] = StraightLine(
                    self.max_n_rows,
                    self.max_n_cols,
                    orientation='horizontal',
                    color_pattern=self.color_pattern_hor,
                    length=self.length_hor).grid[0, :]
                tshape[1::, self.displacement] = StraightLine(
                    self.max_n_rows,
                    self.max_n_cols,
                    orientation='vertical',
                    color_pattern=self.color_pattern_ver,
                    length=self.length_ver).grid[:, 0]

        if self.orientation == 90:

            tshape = np.zeros((self.length_ver, self.length_hor + 1))

            if self.uniform_color:
                color = np.random.randint(self.no_black_pixels, 10)
                tshape[self.displacement, 1::] = StraightLine(
                    self.max_n_rows,
                    self.max_n_cols,
                    orientation='horizontal',
                    color_pattern=self.color_pattern_hor,
                    length=self.length_hor,
                    color=color).grid[0, :]
                tshape[:, 0] = StraightLine(
                    self.max_n_rows,
                    self.max_n_cols,
                    orientation='vertical',
                    color_pattern=self.color_pattern_ver,
                    length=self.length_ver,
                    color=color).grid[:, 0]

            else:
                tshape[self.displacement, 1::] = StraightLine(
                    self.max_n_rows,
                    self.max_n_cols,
                    orientation='horizontal',
                    color_pattern=self.color_pattern_hor,
                    length=self.length_hor).grid[0, :]
                tshape[:, 0] = StraightLine(
                    self.max_n_rows,
                    self.max_n_cols,
                    orientation='vertical',
                    color_pattern=self.color_pattern_ver,
                    length=self.length_ver).grid[:, 0]

        if self.orientation == 180:

            tshape = np.zeros((self.length_ver + 1, self.length_hor))

            if self.uniform_color:
                color = np.random.randint(self.no_black_pixels, 10)
                tshape[self.length_ver, :] = StraightLine(
                    self.max_n_rows,
                    self.max_n_cols,
                    orientation='horizontal',
                    color_pattern=self.color_pattern_hor,
                    length=self.length_hor,
                    color=color).grid[0, :]
                tshape[0:self.length_ver, self.displacement] = StraightLine(
                    self.max_n_rows,
                    self.max_n_cols,
                    orientation='vertical',
                    color_pattern=self.color_pattern_ver,
                    length=self.length_ver,
                    color=color).grid[:, 0]
            else:
                tshape[self.length_ver, :] = StraightLine(
                    self.max_n_rows,
                    self.max_n_cols,
                    orientation='horizontal',
                    color_pattern=self.color_pattern_hor,
                    length=self.length_hor).grid[0, :]
                tshape[0:self.length_ver, self.displacement] = StraightLine(
                    self.max_n_rows,
                    self.max_n_cols,
                    orientation='vertical',
                    color_pattern=self.color_pattern_ver,
                    length=self.length_ver).grid[:, 0]

        if self.orientation == 270:

            tshape = np.zeros((self.length_ver, self.length_hor + 1))

            if self.uniform_color:
                color = np.random.randint(self.no_black_pixels, 10)
                tshape[self.displacement, 0:self.length_hor] = StraightLine(
                    self.max_n_rows,
                    self.max_n_cols,
                    orientation='horizontal',
                    color_pattern=self.color_pattern_hor,
                    length=self.length_hor,
                    color=color).grid[0, :]
                tshape[:, self.length_hor] = StraightLine(
                    self.max_n_rows,
                    self.max_n_cols,
                    orientation='vertical',
                    color_pattern=self.color_pattern_ver,
                    length=self.length_ver,
                    color=color).grid[:, 0]
            else:
                tshape[self.displacement, 0:self.length_hor] = StraightLine(
                    self.max_n_rows,
                    self.max_n_cols,
                    orientation='horizontal',
                    color_pattern=self.color_pattern_hor,
                    length=self.length_hor).grid[0, :]
                tshape[:, self.length_hor] = StraightLine(
                    self.max_n_rows,
                    self.max_n_cols,
                    orientation='vertical',
                    color_pattern=self.color_pattern_ver,
                    length=self.length_ver).grid[:, 0]

        return tshape
