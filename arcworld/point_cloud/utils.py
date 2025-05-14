import numpy as np

from arcworld.constants import ShapeOutOfBounds, MAX_GRID_SIZE

def pc_to_full_sized_grid(pc, n_cols=MAX_GRID_SIZE, n_rows=MAX_GRID_SIZE) -> np.ndarray:
    '''
    Converts a point cloud into a 
    grid of size (n_cols, n_rows)
    '''
    grid = np.zeros((n_cols, n_rows), dtype=int)
    try:
        for idx, color in pc.items():
            grid[idx] = color
    except IndexError:
        raise ShapeOutOfBounds(f'Can not convert this pc into a grid of size ({n_cols}, {n_rows})')
    return grid

def pc_to_shape_only_grid(pc) -> np.ndarray:
    '''
    Converts a point cloud into
    a grid of size (pc.n_cols, pc.n_rows)
    '''
    grid = np.zeros((pc.n_rows, pc.n_cols), dtype=int)
    dx = pc.min_x
    dy = pc.min_y
    for idx, color in pc.items():
        x,y = idx
        grid[(x-dx,y-dy)] = color
    return grid

