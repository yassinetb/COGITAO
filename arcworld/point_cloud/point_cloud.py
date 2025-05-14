import collections.abc
from collections import UserDict
import numpy as np
from arcworld.constants import MAX_GRID_SIZE, ALLOWED_COLORS
from arcworld.point_cloud.utils import pc_to_full_sized_grid, pc_to_shape_only_grid

## For this generator, which is shape-centric (object-centric), we define the "PointCloud" class below as a dedicate class with its own 
## method and attributes to facilitate shape manipulation (e.g. moving a shape within a grid). 

class DictWrapper(collections.abc.MutableMapping):

    def __init__(self, data=None, /, **kwargs):
        self._data = {}
        if data is not None:
            self.update(data)
        if kwargs:
            self.update(kwargs)

    def __len__(self):
        return len(self._data)

    def __getitem__(self, key):
        if key in self._data:
            return self._data[key]
        if hasattr(self.__class__, "__missing__"):
            return self.__class__.__missing__(self, key)
        raise KeyError(key)

    def __setitem__(self, key, item):
        self._data[key] = item

    def __delitem__(self, key):
        del self._data[key]

    def __iter__(self):
        return iter(self._data)

    # Modify __contains__ to work correctly when __missing__ is present
    def __contains__(self, key):
        return key in self._data

    # Now, add the methods in dicts but not in MutableMapping
    def __repr__(self):
        return repr(self._data)

    def __or__(self, other):
        if isinstance(other, UserDict):
            return self.__class__(self._data | other._data)
        if isinstance(other, dict):
            return self.__class__(self._data | other)
        return NotImplemented

    def __ror__(self, other):
        if isinstance(other, UserDict):
            return self.__class__(other._data | self._data)
        if isinstance(other, dict):
            return self.__class__(other | self._data)
        return NotImplemented

    def __ior__(self, other):
        if isinstance(other, UserDict):
            self._data |= other._data
        else:
            self._data |= other
        return self

    def __copy__(self):
        inst = self.__class__.__new__(self.__class__)
        inst.__dict__.update(self.__dict__)
        # Create a copy and avoid triggering descriptors
        inst.__dict__["_data"] = self.__dict__["_data"].copy()
        return inst

    def copy(self):
        if self.__class__ is UserDict:
            return UserDict(self._data.copy())
        import copy
        _data = self._data
        try:
            self._data = {}
            c = copy.copy(self)
        finally:
            self._data = _data
        c.update(self)
        return c

    @classmethod
    def fromkeys(cls, iterable, value=None):
        d = cls()
        for key in iterable:
            d[key] = value
        return d


class PointCloud(DictWrapper):

    def __init__(self, data: dict):
        self.check_dict(data)
        super().__init__(data)

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data: dict):
        self.check_dict(data)
        self.clear()
        self.update(data)

    @property
    def indexes(self):
        return self.data.keys()

    @property
    def x_vals(self):
        if self.data:
            return list(list(zip(*self.data.keys()))[0])
        return []

    @property
    def y_vals(self):
        if self.data:
            return list(list(zip(*self.data.keys()))[1])
        return []

    @property
    def max_x(self):
        if self.data:
            return max(self.x_vals)
        return None

    @property
    def min_x(self):
        if self.data:
            return min(self.x_vals)
        return None

    @property
    def max_y(self):
        if self.data:
            return max(self.y_vals)
        return None

    @property
    def min_y(self):
        if self.data:
            return min(self.y_vals)
        return None

    @property
    def n_rows(self): ## Height
        if self.data:
            return self.max_x - self.min_x + 1
        return 0

    @property
    def n_cols(self): ## Width
        if self.data:
            return self.max_y - self.min_y + 1
        return 0

    @property
    def colors(self):
        return list(self.data.values())
    
    @property
    def most_frequent_color(self):
        return max(set(self.colors), key = self.colors.count)
    
    @property
    def existing_colors(self):
        return np.unique(list(self.data.values()))

    @property
    def num_points(self):
        return len(self)

    @property
    def current_position(self):
        min_x = min(self.x_vals)
        min_y = min(self.y_vals)
        return min_x, min_y

    @property
    def bounding_corners(self):
        '''Returns the lower left and the top right corner of the bounding box of the object'''
        max_x = max(self.x_vals)
        max_y = max(self.y_vals)
        top_left = self.current_position
        lower_right = (max_x, max_y)
        return top_left, lower_right

    def as_grid(self):
            return pc_to_full_sized_grid(self)
    
    def as_shape_only_grid(self):
        return pc_to_shape_only_grid(self)
    
    def as_colorless_shape_only_grid(self):
        return np.int_(pc_to_shape_only_grid(self) != 0)

    def possible_positions(self):
        possible_positions = []
        for x in range(MAX_GRID_SIZE - self.rows - 1):
            for y in range(MAX_GRID_SIZE - self.cols - 1):
                possible_positions.append((x, y))
        return possible_positions

    def check_dict(self, pc_dict: dict):
        if not isinstance(pc_dict, dict):
            raise ValueError('Can only create point cloud from dict')
        for idx, color in pc_dict.items():
            if color not in ALLOWED_COLORS:
                raise ValueError('Colors not allowed')
