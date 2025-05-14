import numpy as np

from arcworld.shapes.base import BasicShape


class StraightLine(BasicShape):

    def __init__(self,
                 max_n_rows,
                 max_n_cols,
                 color_pattern=None,
                 orientation=None,
                 n_colors=None,
                 length=None,
                 color=None):
        super().__init__(
            max_n_rows=max_n_rows,
            max_n_cols=max_n_cols,
            color_pattern=color_pattern
        )

        self.grid_height = max_n_rows
        self.grid_width = max_n_cols

        if color_pattern is None:
            color_pattern = np.random.choice(['uniform', 'symmetric', 'alternated', 'random'])
        if color_pattern not in ['uniform', 'symmetric', 'alternated', 'random']:
            color_pattern = 'uniform'

        self.color_pattern = color_pattern

        # orientation: diagonal/horizontal/vertical
        if orientation is None:
            orientation = np.random.choice(['horizontal', 'vertical', 'diagonal'])

        # when we initialize self.oritentation 
        # we will just create an array of elements: 
        # then we will use the orientation attribute to fill the grid
        self.orientation = orientation

        if length is None:
            if orientation == 'horizontal':
                length = np.random.randint(1, 1 + max_n_cols)
            if orientation == 'vertical':
                length = np.random.randint(1, 1 + max_n_rows)
            if orientation == 'diagonal':
                length = np.random.randint(1, 1 + min(max_n_cols, max_n_rows))

        self.length = length

        if orientation == 'horizontal' and length >= max_n_cols:
            self.length = max_n_cols

        if orientation == 'vertical' and length >= max_n_rows:
            self.length = max_n_rows

        if orientation == 'diagonal' and length >= min(max_n_rows, max_n_cols):
            self.length = min(max_n_cols, max_n_rows)

        if n_colors is None:
            n_colors = np.random.randint(1, 11)
        self.n_colors = n_colors  # number of different colors in the line
        if n_colors >= self.length:
            self.n_colors = self.length

        self.color = color  # we reserve the possibility to select the color deterministically from outside the class (for the moment, just for uniform case)

        self.no_black_pixels = 1

        self.grid = self.generate()

    def generate(self):

        line = np.zeros(self.length)

        if self.color_pattern == 'uniform':

            if self.color is not None:
                line = self.color * np.ones(self.length)

            else:
                col = np.random.randint(self.no_black_pixels, 10, size=1)
                line = col * np.ones(self.length)

        if self.color_pattern == 'symmetric':

            if self.length % 2 == 0:

                col1 = np.random.randint(self.no_black_pixels, 10, size=1)
                col2 = col1
                while col2 == col1:
                    col2 = np.random.randint(self.no_black_pixels, 10, size=1)

                mask1 = np.array(range(self.length)) < self.length / 2
                mask2 = np.array(range(self.length)) >= self.length / 2

                line[mask1] = col1
                line[mask2] = col2

            else:
                col1 = np.random.randint(self.no_black_pixels, 10, size=1)
                col2 = col1
                while col2 == col1:
                    col2 = np.random.randint(self.no_black_pixels, 10, size=1)

                col3 = col2

                while col3 == col2 or col3 == col1:
                    col3 = np.random.randint(self.no_black_pixels, 10, 1)

                mask1 = np.array(range(self.length)) < int(self.length / 2)
                mask2 = np.array(range(self.length)) > int(self.length / 2)
                mask3 = np.array(range(self.length)) == int(self.length / 2)

                line[mask1] = col1
                line[mask2] = col2
                line[mask3] = col3

        if self.color_pattern == 'alternated':

            line = np.zeros(self.length)
            count = 0
            col1 = np.random.randint(self.no_black_pixels, 10)
            colors = [col1]
            not_used_colors = []

            for i in range(self.n_colors - 1):
                if i <= 8:
                    if i >= 7:
                        for j in range(10):
                            if j not in colors:
                                not_used_colors.append(j)

                        col = np.random.choice(not_used_colors)
                        not_used_colors.remove(col)
                        colors.append(col)

                    else:
                        col = col1
                        while col in colors:
                            col = np.random.randint(self.no_black_pixels, 10)
                        colors.append(col)

            for i in range(self.length):

                line[i] = colors[count]

                count += 1
                if count % len(colors) == 0:
                    count = 0

        if self.color_pattern == 'random':

            line = np.zeros(self.length)

            for i in range(self.length):
                line[i] = np.random.randint(self.no_black_pixels, 10, size=1)

        if self.orientation == 'horizontal':
            line = line.reshape((1, len(line)))

        if self.orientation == 'vertical':
            line = line.reshape((len(line), 1))

        if self.orientation == 'diagonal':
            line = np.diag(line)

        return line
