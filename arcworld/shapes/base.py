from abc import abstractmethod
from functools import cached_property

from arcworld.point_cloud.point_cloud import PointCloud
from arcworld.shapes.utils import move_to_position, delete_out_of_bounds_points, grid_to_pc


class Shape():

    def __init__(self, data):
        '''create shape from grid or PointCloud'''
        if isinstance(data, Shape):
            self.pc = data.pc
        elif isinstance(data, PointCloud) or isinstance(data, dict) or data is None:
            self.pc = data
        else:
            self.grid = data

    @property
    def x_vals(self):
        return self.pc.x_vals

    @property
    def y_vals(self):
        return self.pc.y_vals

    @property
    def colors(self):
        return self.pc.colors

    @property
    def existing_colors(self):
        return self.pc.existing_colors

    @property
    def bounding_corners(self):
        '''Returns the lower left and the top right corner of the bounding box of the shape'''
        return self.pc.bounding_corners
    
    @property
    def most_frequent_color(self):
        return self.pc.most_frequent_color

    @property
    def current_position(self):
        return self.pc.current_position

    @property
    def num_points(self):
        return self.pc.num_points

    @property
    def n_rows(self):
        return self.pc.n_rows
    
    @property
    def n_cols(self):
        return self.pc.n_cols

    @property
    def min_x(self):
        return self.pc.min_x

    @property
    def max_x(self):
        return self.pc.max_x

    @property
    def min_y(self):
        return self.pc.min_y
    
    @property
    def max_y(self):
        return self.pc.max_y
    
    @property
    def indexes(self):
        return self.pc.indexes

    @property
    def pc(self):
        return self._pc
    
    @property
    def is_null(self):
        return self.pc.num_points == 0

    @property
    def grid(self):
        if hasattr(self, '_grid') and self._grid is not None:
            return self._grid
        self._grid = self.pc.as_grid() if self.pc is not None else None
        return self._grid

    @cached_property
    def as_shape_only_grid(self):
         return self.pc.as_shape_only_grid()
    
    @property
    def as_colorless_shape_only_grid(self):
        return self.pc.as_colorless_shape_only_grid()

    @grid.setter
    def grid(self, grid):
        self._pc = grid_to_pc(grid)

    @pc.setter
    def pc(self, pc):
        if isinstance(pc, PointCloud):
            self._pc = pc.copy()
        elif isinstance(pc, dict):
            self._pc = PointCloud(pc)
        elif pc is None:
            self._pc = PointCloud({})
        else:
            raise ValueError(f"Point cloud can't be set from {pc}")
        self._grid = None
        try:
            del self.as_shape_only_grid
        except AttributeError:
            pass

    def possible_positions(self):
        self.pc.possible_positions()

    def move_to_position(self, position):
        self.pc = move_to_position(self.pc, position)

    def delete_out_of_bounds_points(self):
        self.pc = delete_out_of_bounds_points(self.pc)

class BasicShape(Shape):
    def __init__(self,
                 max_n_rows: int,
                 max_n_cols: int,
                 color_pattern: str):
        self.max_n_rows = max_n_rows
        self.max_n_cols = max_n_cols
        self.color_pattern = color_pattern

    @abstractmethod
    def generate(self):
        pass