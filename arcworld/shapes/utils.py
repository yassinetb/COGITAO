
from arcworld.point_cloud.point_cloud import PointCloud
from arcworld.point_cloud.utils import pc_to_shape_only_grid
import numpy as np


def add_contour_to_shape(shape, contour_dict = {"up": 0, "down": 0, "left": 0, "right": 0}):
    
    return new_shape

def pc_from_indexes_and_colors(indexes, colors) -> PointCloud:
    pc = dict(zip(indexes, colors))
    return PointCloud(pc)

def shift_indexes(indexes: list([(int, int)]), dx: int = 0, dy: int = 0) -> list([(int, int)]):
    new_indexes = []
    for x, y in indexes:
        new_indexes.append((x + dx, y + dy))
    return new_indexes

def move_to_position(pc, position):
    dx = position[0] - pc.current_position[0]
    dy = position[1] - pc.current_position[1]
    indexes = shift_indexes(pc.indexes, dx, dy)
    return pc_from_indexes_and_colors(indexes, pc.colors)

def is_idx_within_bounds(idx):
    if idx[0] >= 0 and idx[0] < 30 and idx[1] >= 0 and idx[1] < 30:
        return True
    else:
        return False

def delete_out_of_bounds_points(pc):
    indexes = pc.indexes
    colors = pc.colors
    new_indexes = []
    new_colors = []
    for i, idx in enumerate(indexes):
        if is_idx_within_bounds(idx):
            new_indexes.append(idx)
            new_colors.append(colors[i])
    return pc_from_indexes_and_colors(new_indexes, new_colors)

def grid_to_pc(grid) -> PointCloud:
    pc = {}
    indexes = np.transpose(np.nonzero(grid))
    for idx in indexes:
        idx = tuple(idx)
        pc[idx] = grid[idx]
    return PointCloud(pc)

def grid_to_cropped_grid(grid) -> np.ndarray:
    pc = grid_to_pc(grid)
    grid = pc_to_shape_only_grid(pc)
    return grid
