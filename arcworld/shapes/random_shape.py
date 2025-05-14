import random

import factory
import numpy as np
import scipy
import skimage
from scipy.ndimage import generate_binary_structure

from arcworld.shapes.base import Shape
from arcworld.shapes.utils import grid_to_pc, pc_from_indexes_and_colors, grid_to_cropped_grid


class RandomShape(Shape):
    def __init__(self, params=None, **kwargs):
        self.params = params if params else RandomShapeParamsFactory(**kwargs)
        self.grid = self.generate()

    def grow_horizontal_symmetric_shape(self, max_rows, max_cols, min_rows, min_cols):
        half_row = np.ceil(max_rows / 2).astype(int)
        grid = np.zeros((half_row, max_cols), dtype=int)
        grid[0, max_cols // 2] = 1
        grid = self.grow_shape(grid, min_rows / 2, min_cols)
        mirrored = np.flipud(grid)[:max_rows - half_row]
        grid = np.concatenate((mirrored, grid))
        return grid

    def grow_vertical_symmetric_shape(self, max_rows, max_cols, min_rows, min_cols):
        # just call horizontal with flipped rows/cols
        grid = self.grow_horizontal_symmetric_shape(max_cols, max_rows, min_cols, min_rows)
        grid = np.rot90(grid)
        return grid

    def grow_point_symmetric_shape(self, max_rows, max_cols, min_rows, min_cols):
        # grow horizontal with half cols and flip left
        half_col = np.ceil(self.params.max_cols / 2).astype(int)
        grid = self.grow_horizontal_symmetric_shape(max_rows, half_col, min_rows, min_cols / 2)
        grid = grid_to_cropped_grid(grid)
        mirrored = np.fliplr(grid)[:, :max_cols - half_col]
        grid = np.concatenate((mirrored, grid), axis=1)
        return grid

    def grow_unsymmetric_shape(self, max_rows, max_cols, min_rows, min_cols):
        grid = np.zeros((max_rows, max_cols), dtype=int)
        grid[max_rows // 2, max_cols // 2] = 1
        grid = self.grow_shape(grid, min_rows, min_cols)
        return grid

    def grow_diag_symmetric_shape_tl_br(self, max_rows, max_cols, min_rows, min_cols):
        size = min(max_rows, max_cols)
        grid = np.zeros((size, size), dtype=int)

        # its not trivial how big the grown shape needs to be to fulfill min_row, min_col conditions, ones it is
        # transposed and added to the original, therfore dont constrain it and check after it is built
        while True:
            grid[size // 2, size // 2] = 1

            grid = self.grow_shape(grid, 0, 0)
            lower_tri = np.tril(grid)
            grid = lower_tri | lower_tri.T
            pc = grid_to_pc(grid)
            if pc.n_cols >= min_cols and pc.n_rows >= min_rows:
                # because the lower part of the grid is masked, connectivity is not enforced
                # so manually check here, otherwise dont break (currently only checked for 4 or 8 connected)
                if self.params.connectivity not in ['4connected', '8connected']:
                    break
                _, num_connected = scipy.ndimage.label(grid, self.get_footprint())
                if num_connected == 1:
                    break
        return grid

    def grow_diag_symmetric_shape_bl_tr(self, max_rows, max_cols, min_rows, min_cols):
        # just call the other diag and rotate with switched rows/cols
        grid = self.grow_diag_symmetric_shape_tl_br(max_cols, max_rows, min_cols, min_rows)
        grid = np.rot90(grid)
        return grid

    def generate_from_symmetry(self):
        if self.params.symmetry == 'horizontal':
            grid = self.grow_horizontal_symmetric_shape(self.params.max_rows, self.params.max_cols,
                                                        self.params.min_rows, self.params.min_cols)

        elif self.params.symmetry == 'vertical':
            grid = self.grow_vertical_symmetric_shape(self.params.max_rows, self.params.max_cols, self.params.min_rows,
                                                      self.params.min_cols)

        elif self.params.symmetry == 'point':
            grid = self.grow_point_symmetric_shape(self.params.max_rows, self.params.max_cols, self.params.min_rows,
                                                   self.params.min_cols)

        elif self.params.symmetry == 'no':
            grid = self.grow_unsymmetric_shape(self.params.max_rows, self.params.max_cols, self.params.min_rows,
                                               self.params.min_cols)

        elif self.params.symmetry == 'diag_tl_br':
            grid = self.grow_diag_symmetric_shape_tl_br(self.params.max_rows, self.params.max_cols,
                                                        self.params.min_rows, self.params.min_cols)

        elif self.params.symmetry == 'diag_bl_tr':
            grid = self.grow_diag_symmetric_shape_bl_tr(self.params.max_rows, self.params.max_cols,
                                                        self.params.min_rows, self.params.min_cols)
        else:
            raise ValueError('Symmetry not found')
        return grid

    def generate_from_footprint(self):
        if self.params.footprint == 'rectangle':
            grid = skimage.morphology.rectangle(self.params.min_rows, self.params.min_cols)

        elif self.params.footprint == 'square':
            grid = skimage.morphology.square(self.params.min_rows)

        elif self.params.footprint == 'ellipse':
            r = (self.params.min_rows -1)//2
            c = (self.params.min_cols -1)//2
            grid = skimage.morphology.ellipse(r,c)

        elif self.params.footprint == 'diamond':
            r = self.params.min_rows//2
            grid = skimage.morphology.diamond(r)

        elif self.params.footprint == 'disk':
            r = self.params.min_rows // 2
            grid = skimage.morphology.disk(r)

        return grid

    def generate(self):
        if self.params.use_footprint:
            grid = self.generate_from_footprint()
            if self.params.outline:
                inside = skimage.morphology.erosion(grid)
                diff = grid-inside
                if np.sum(diff)>0:
                    grid = diff
        else:
            grid = self.generate_from_symmetry()
        grid = grid_to_cropped_grid(grid)
        grid = self.do_coloring(grid)
        return grid

    def do_coloring(self, grid):
        # remove all colors from grid
        grid = (grid > 0).astype(int)
        if self.params.color_pattern == 'uniform':
            grid = grid * self.params.colors[0]
        elif self.params.color_pattern == 'col_stripes':
            grid[:, 1::2] *= self.params.colors[0]
            grid[:, ::2] *= self.params.colors[1]
        elif self.params.color_pattern == 'row_stripes':
            grid[1::2] *= self.params.colors[0]
            grid[::2] *= self.params.colors[1]
        elif self.params.color_pattern == 'random':
            indexes = grid_to_pc(grid).indexes
            colors = np.random.choice(self.params.colors, len(indexes))
            grid = pc_from_indexes_and_colors(indexes, colors).as_shape_only_grid()

        elif self.params.color_pattern == 'top_bot':
            uneven = np.random.choice([0, 1], 1, p=[0.5, 0.5]).item()
            half = (grid.shape[0] + uneven) // 2
            grid[half:] *= self.params.colors[0]
            grid[:half] *= self.params.colors[1]
        elif self.params.color_pattern == 'left_right':
            uneven = np.random.choice([0, 1], 1, p=[0.5, 0.5]).item()
            half = (grid.shape[1] + uneven) // 2
            grid[:, half:] *= self.params.colors[0]
            grid[:, :half] *= self.params.colors[1]
        elif self.params.color_pattern == 'diag_tl_br':
            uneven = np.random.choice([0, -1], 1, p=[0.5, 0.5]).item()
            mask = np.tri(grid.shape[0], M=grid.shape[1], k=uneven, dtype=int)
            color_mask = np.where(mask, self.params.colors[1], self.params.colors[0])
            grid = grid * color_mask
        elif self.params.color_pattern == 'diag_bl_tr':
            uneven = np.random.choice([0, -1], 1, p=[0.5, 0.5]).item()
            mask = np.tri(grid.shape[0], M=grid.shape[1], k=uneven, dtype=int)
            mask = np.flipud(mask)
            color_mask = np.where(mask, self.params.colors[1], self.params.colors[0])
            grid = grid * color_mask

        return grid

    def grow_shape(self, grid, min_rows, min_cols):
        p = self.params.grow_probability
        footprint = self.get_footprint()
        already_testet = np.zeros_like(grid)
        while True:
            dilated = skimage.morphology.dilation(grid, footprint)
            current_pixels = dilated & ~grid & ~already_testet
            already_testet = already_testet | current_pixels
            if np.sum(current_pixels) == 0:
                break
            mask = current_pixels & np.random.choice([1, 0], size=grid.shape, p=[p, 1 - p])
            grid = mask | grid
        pc = grid_to_pc(grid)
        if pc.n_cols < min_cols or pc.n_rows < min_rows:
            grid = self.grow_shape(grid, min_rows, min_cols)
        return grid

    def get_footprint(self):
        if self.params.connectivity == '4connected':
            return generate_binary_structure(2, 1).astype(int)
        if self.params.connectivity == '8connected':
            return generate_binary_structure(2, 2).astype(int)
        if self.params.connectivity == 'distance':
            return skimage.morphology.disk(self.params.distance)
        if self.params.connectivity == 'no':
            return skimage.morphology.rectangle(30, 30)


class RandomShapeParams():
    allowed_symmetry = ['horizontal', 'vertical', 'diag_tl_br', 'diag_bl_tr', 'point', 'no']
    allowed_color_pattern = {'uniform': 1, 'diag_tl_br': 2, 'diag_bl_tr': 2, 'top_bot': 2, 'left_right': 2,
                             'col_stripes': 2,
                             'row_stripes': 2, 'random': -1}
    allowed_connectivity = ['4connected', '8connected', 'distance', 'no']
    allowed_colors = list(np.arange(1, 10))
    allowed_footprints = ['rectangle', 'disk', 'square', 'diamond', 'ellipse']

    allowed_max_size = 30

    def __init__(self, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)
        self.clean()

    def clean(self):
        if (self.symmetry in ['diag_tl_br', 'diag_bl_tr'] and not self.use_footprint) or (
                self.footprint in ['square'] and self.use_footprint):

            min_shape = min(self.max_rows, self.max_cols)
            self.min_rows = min_shape if self.min_rows > min_shape else self.min_rows
            self.min_cols = min_shape if self.min_cols > min_shape else self.min_cols


class RandomShapeParamsFactory(factory.Factory):
    class Params:
        set_cols_from_max = False
        set_rows_from_max = False
        set_connectivity_to_dist = False
        set_pattern_from_colors = False

    @factory.lazy_attribute
    def use_footprint(self):
        # return True
        return random.choice([True, False])
    
    @factory.lazy_attribute
    def footprint(self):
        return random.choice(RandomShapeParams.allowed_footprints)

    @factory.lazy_attribute
    def outline(self):
        return random.choice([True, False])

    @factory.lazy_attribute
    def symmetry(self):
        return random.choice(RandomShapeParams.allowed_symmetry)

    @factory.lazy_attribute
    def grow_probability(self):
        sample = scipy.stats.halfnorm.rvs(loc=0.2, scale=0.2)
        return sample

    @factory.lazy_attribute
    def colors(self):
        if not self.set_pattern_from_colors:
            num_cols = RandomShapeParams.allowed_color_pattern[self.color_pattern]
            if num_cols == -1:
                num_cols = np.random.choice(np.arange(1, 10), 1)
            return np.random.choice(RandomShapeParams.allowed_colors, num_cols)
        num_cols = np.random.choice([1, 2, 3, 4], 1)
        return np.random.choice(RandomShapeParams.allowed_colors, num_cols)

    @factory.lazy_attribute
    def color_pattern(self):
        if self.set_pattern_from_colors:
            num_colors = len(self.colors)
            possible_patterns = []
            for pattern, num_colors_for_pattern in RandomShapeParams.allowed_color_pattern.items():
                if num_colors == num_colors_for_pattern or num_colors_for_pattern == -1:
                    possible_patterns.append(pattern)
            return np.random.choice(possible_patterns, 1)
        return random.choice(list(RandomShapeParams.allowed_color_pattern.keys()))

    @factory.lazy_attribute
    def connectivity(self):
        if self.set_connectivity_to_dist:
            return 'distance'
        return random.choice(RandomShapeParams.allowed_connectivity)

    @factory.lazy_attribute
    def distance(self):
        if self.connectivity == 'distance':
            return np.random.choice([2, 3], 1).item()
        return None

    @factory.lazy_attribute
    def min_cols(self):
        if self.set_cols_from_max:
            possible_vals = np.arange(1, self.max_cols + 1)
            return np.random.choice(possible_vals, 1).item()
        possible_vals = np.arange(1, RandomShapeParams.allowed_max_size + 1)
        return np.random.choice(possible_vals, 1).item()

    @factory.lazy_attribute
    def max_cols(self):
        if not self.set_cols_from_max:
            possible_vals = np.arange(self.min_cols, RandomShapeParams.allowed_max_size + 1)
            return np.random.choice(possible_vals, 1).item()
        return np.random.choice(RandomShapeParams.allowed_max_size, 1).item()

    @factory.lazy_attribute
    def min_rows(self):
        if self.set_rows_from_max:
            possible_vals = np.arange(1, self.max_rows + 1)
            return np.random.choice(possible_vals, 1).item()
        possible_vals = np.arange(1, RandomShapeParams.allowed_max_size + 1)
        return np.random.choice(possible_vals, 1).item()

    @factory.lazy_attribute
    def max_rows(self):
        if not self.set_rows_from_max:
            possible_vals = np.arange(self.min_rows, RandomShapeParams.allowed_max_size + 1)
            return np.random.choice(possible_vals, 1).item()
        return np.random.choice(RandomShapeParams.allowed_max_size, 1).item()

    @classmethod
    def build(cls, **kwargs):
        # normally patient for fup is taken from patient field
        # but if fup is given, the patient should be the one from the fup
        for key, value in kwargs.items():
            if key == 'max_rows' and value is not None:
                kwargs = {**kwargs, 'set_rows_from_max': True}
            if key == 'max_cols' and value is not None:
                kwargs = {**kwargs, 'set_cols_from_max': True}
            if key == 'distance' and value is not None:
                kwargs = {**kwargs, 'set_connectivity_to_dist': True}
            if key == 'colors' and value is not None:
                kwargs = {**kwargs, 'set_pattern_from_colors': True}

        return super().build(**kwargs)

    class Meta:
        model = RandomShapeParams
        strategy = factory.BUILD_STRATEGY
