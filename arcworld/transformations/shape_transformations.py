import numpy as np
import scipy
from arcworld.constants import MAX_GRID_SIZE
from arcworld.shapes.base import Shape
from arcworld.conditionals.single_shape_conditionals import is_shape_hollow



#### Each Transform must come with 
#### 1. compatible transforms 2. shape constraints

## Translate Up 1


# - Translation x 4
# - Rotation x 3
# - Shape Filling 
# - Shape Emptying 
# - Mirroring 
# - Shape cropping 
# - Recolor

PADDING_RIGHT = 6
PADDING_LEFT = 7
PADDING_TOP = 8
PADDING_BOTTOM = 9


## Translate Up

constraints_translate_up = {"incompatible_shapes": [], 
                           "incompatible_transforms": [],
                           "application_order": [],
                           "can_be_applied_multiple_times": True,
                           }

def translate_up(shape):
    x, y = shape.current_position
    new_shape = Shape(shape)
    new_shape.move_to_position((x-1, y))
    return new_shape

## Translate Down 

constraints_translate_down = {"incompatible_shapes": [], 
                           "incompatible_transforms": [],
                           "application_order": [],
                           "can_be_applied_multiple_times": True,
                           }

def translate_down(shape):
    x, y = shape.current_position
    new_shape = Shape(shape)
    new_shape.move_to_position((x+1, y))
    return new_shape

## Transle Right

constraints_translate_right = {"incompatible_shapes": [], 
                           "incompatible_transforms": [],
                           "application_order": [],
                           "can_be_applied_multiple_times": True,
                           }

def translate_right(shape):
    x, y = shape.current_position
    new_shape = Shape(shape)
    new_shape.move_to_position((x, y+1))
    return new_shape

## Translate Left

constraints_translate_left = {"incompatible_shapes": [], 
                           "incompatible_transforms": [],
                           "application_order": [],
                           "can_be_applied_multiple_times": True,
                           }

def translate_left(shape):
    x, y = shape.current_position
    new_shape = Shape(shape)
    new_shape.move_to_position((x, y-1))
    return new_shape

## Rot90

constraints_rot90 = {"incompatible_shapes": [], 
                    "incompatible_transforms": [],
                    "application_order": [],
                    "can_be_applied_multiple_times": True,
                    }

def rot90(shape):
    position = shape.current_position
    rotated = Shape(np.rot90(shape.grid, 1))
    rotated.move_to_position(position)
    return rotated

## Shape Filling

constraints_fill_holes_same_color = {"incompatible_shapes": ["is_shape_not_hollow", "is_shape_not_evenly_colored"], 
                        "incompatible_transforms": [],
                        "application_order": [],
                        "can_be_applied_multiple_times": True,
                        }

def fill_holes_same_color(shape): ## Fills hole with the first color
    if is_shape_hollow(shape):
        most_frequent_color = shape.most_frequent_color
        return Shape(scipy.ndimage.binary_fill_holes(shape.grid).astype(int)*most_frequent_color)
    else:
        return shape
    
## Shape Filling Different Color 

constraints_fill_holes_different_color = {"incompatible_shapes": ["is_shape_not_hollow", "is_shape_not_evenly_colored"], 
                        "incompatible_transforms": [],
                        "application_order": [],
                        "can_be_applied_multiple_times": True,
                        }

def fill_holes_different_color(shape): ## Fills hole with the first color
    if is_shape_hollow(shape):
        new_color = (shape.most_frequent_color % 9) + 1
        filled_shape = Shape(scipy.ndimage.binary_fill_holes(shape.grid).astype(int)*shape.colors[0])
        filling_diff = ((filled_shape.grid - shape.grid) != 0) * new_color
        return Shape(filling_diff + shape.grid) 
    else:
        return shape

## Shape Emptying

constraints_empty_inside_pixels = {"incompatible_shapes": ["is_shape_hollow", 
                                                           "is_shape_not_fully_connected",
                                                           "is_shape_less_than_3_rows", 
                                                           "is_shape_less_than_3_cols", 
                                                           "is_shape_less_than_6_cell"], 
                        "incompatible_transforms": [],
                        "application_order": [],
                        "can_be_applied_multiple_times": True,
                        }

def empty_inside_pixels(shape):
    
    shape_grid = shape.grid
    shape_position = shape.current_position
    
    # Create an empty grid of the same shape to store the result
    result = np.zeros_like(shape_grid)

    # Define the shape of the grid
    rows, cols = shape_grid.shape

    # Iterate over each cell in the grid
    for i in range(rows):  # Avoid boundary pixels
        for j in range(cols):  # Avoid boundary pixels
            
            if i == 0 or i == rows - 1 or j == 0 or j == cols - 1: # Edge
                result[i, j] = shape_grid[i, j]
            else:
                # Check if the current cell is part of the shape (non-zero value)
                if shape_grid[i, j] != 0:
                    # Check the neighboring cells (top, bottom, left, right)
                    if (shape_grid[i - 1, j] == 0 or shape_grid[i + 1, j] == 0 or 
                        shape_grid[i, j - 1] == 0 or shape_grid[i, j + 1] == 0):
                        # If any neighbor is zero, it's part of the contour
                        result[i, j] = shape_grid[i, j]
    
    result = Shape(result)
    result.move_to_position(shape_position)
    return result




## Shape Contouring





## Mirroring Horizontal

constraints_mirror_horizontal = {"incompatible_shapes": [], 
                        "incompatible_transforms": [],
                        "application_order": [],
                        "can_be_applied_multiple_times": True,
                        }

def mirror_horizontal(shape):
    position = shape.current_position
    mirrored = Shape(np.flipud(shape.grid))
    mirrored.move_to_position(position)
    return mirrored

## Mirroring Vertical 

constraints_mirror_vertical = {"incompatible_shapes": [], 
                        "incompatible_transforms": [],
                        "application_order": [],
                        "can_be_applied_multiple_times": True,
                        }

def mirror_vertical(shape):
    position = shape.current_position
    mirrored = Shape(np.fliplr(shape.grid))
    mirrored.move_to_position(position)
    return mirrored

## Shape Cropping 

constraints_crop_left_side = {"incompatible_shapes": ["is_shape_less_than_4_cols"], 
                            "incompatible_transforms": [],
                            "application_order": [],
                            "can_be_applied_multiple_times": True,
                            }

def crop_left_side(shape):
    shape_pos = shape.current_position
    shape_grid = shape.as_shape_only_grid
    n_cols_half = shape.n_cols // 2
    pos_x, pos_y = shape_pos

    pc = {
        (i + pos_x, j + pos_y): shape_grid[i, j]
        for i in range(shape_grid.shape[0])
        for j in range(n_cols_half, shape_grid.shape[1])
    }
    return Shape(pc)

constraints_crop_right_side = {"incompatible_shapes": ["is_shape_less_than_4_cols"],
                               "incompatible_transforms": [],
                            "application_order": [],
                            "can_be_applied_multiple_times": True,
                            }

def crop_right_side(shape):
    shape_pos = shape.current_position
    shape_grid = shape.as_shape_only_grid
    n_cols_half = (shape.n_cols + 1) // 2
    pos_x, pos_y = shape_pos

    pc = {
        (i + pos_x, j + pos_y): shape_grid[i, j]
        for i in range(shape_grid.shape[0])
        for j in range(n_cols_half)
    }
    return Shape(pc)

constraints_crop_bottom_side = {"incompatible_shapes": ["is_shape_less_than_4_rows"],
                                    "incompatible_transforms": [],
                                "application_order": [],
                                "can_be_applied_multiple_times": True,
                                }

def crop_bottom_side(shape):
    shape_pos = shape.current_position
    shape_grid = shape.as_shape_only_grid
    n_rows_half = (shape.n_rows + 1) // 2
    pos_x, pos_y = shape_pos

    pc = {
        (i + pos_x, j + pos_y): shape_grid[i, j]
        for i in range(n_rows_half)
        for j in range(shape_grid.shape[1])
    }
    return Shape(pc)

constraints_crop_top_side = {"incompatible_shapes": ["is_shape_less_than_4_rows"],
                                    "incompatible_transforms": [],
                                "application_order": [],
                                "can_be_applied_multiple_times": True,
                                }

def crop_top_side(shape):
    shape_pos = shape.current_position
    shape_grid = shape.as_shape_only_grid
    n_rows_half = shape.n_rows // 2
    pos_x, pos_y = shape_pos

    pc = {
        (i + pos_x, j + pos_y): shape_grid[i, j]
        for i in range(n_rows_half, shape_grid.shape[0])
        for j in range(shape_grid.shape[1])
    }
    return Shape(pc)

## Crop Contours

constraints_crop_contours = {"incompatible_shapes": ["is_shape_less_than_4_rows",
                                                 "is_shape_less_than_4_cols"], 
                           "incompatible_transforms": [],
                           "application_order": [],
                           "can_be_applied_multiple_times": True,
                           }  

def crop_contours(shape):
    shape_original_pos = shape.current_position
    shape_grid = shape.as_shape_only_grid
    shape_grid = shape_grid[1:-1, 1:-1]
    new_shape = Shape(shape_grid)
    new_shape.move_to_position((shape_original_pos[0]+1, shape_original_pos[1]+1))
    return new_shape


## Extend Contours

constraints_extend_contours_same_color = {"incompatible_shapes": [],
                                "incompatible_transforms": [],
                                "application_order": [],
                                "can_be_applied_multiple_times": True,
                                }


def extend_contours_same_color(shape):
    """Extends the contours of the shape by 1 pixel in all directions,
    while keeping the same color.
    """
    shape_grid = shape.as_shape_only_grid
    shape_position = shape.current_position

    # Create a copy of the grid to store the result 
    shape_dim = shape_grid.shape

    new_shape = np.zeros((shape_dim[0]+2, shape_dim[1]+2))
    new_shape[1:-1, 1:-1] = shape_grid
    
    new_shape[0, 1:-1] = shape_grid[0, :]
    new_shape[-1, 1:-1] = shape_grid[-1, :]
    new_shape[1:-1, 0] = shape_grid[:, 0]
    new_shape[1:-1, -1] = shape_grid[:, -1]

    new_shape = Shape(new_shape)
    new_shape.move_to_position((shape_position[0]-1, shape_position[1]-1))

    return new_shape

## Extend Contours different color 

constraints_extend_contours_different_color = {"incompatible_shapes": [],
                                "incompatible_transforms": [],
                                "application_order": [],
                                "can_be_applied_multiple_times": True,
                                }


def extend_contours_different_color(shape):
    """Extends the contours of the shape by 1 pixel in all directions,
    color changes following: new_color = (old_color mod 9) + 1.
    """
    shape_grid = shape.as_shape_only_grid
    shape_position = shape.current_position

    # Create a copy of the grid to store the result 
    shape_dim = shape_grid.shape

    new_color = (shape.most_frequent_color % 9) + 1

    new_shape = np.zeros((shape_dim[0]+2, shape_dim[1]+2))
    new_shape[1:-1, 1:-1] = shape_grid
    
    new_shape[0, 1:-1] = (shape_grid[0, :] != 0)*new_color
    new_shape[-1, 1:-1] = (shape_grid[-1, :] != 0)*new_color
    new_shape[1:-1, 0] = (shape_grid[:, 0] != 0)*new_color
    new_shape[1:-1, -1] = (shape_grid[:, -1] != 0)*new_color

    new_shape = Shape(new_shape)
    new_shape.move_to_position((shape_position[0]-1, shape_position[1]-1))

    return new_shape


## Change Shape Color 

constraints_change_shape_color = {"incompatible_shapes": [],
                                "incompatible_transforms": [],
                                "application_order": [],
                                "can_be_applied_multiple_times": True,
                                }


def change_shape_color(shape):
    """Changes the color of the shape to new_color.
    Color changes following: new_color = (old_color mod 9) + 1
    """
    return Shape((shape.grid != 0) * ((shape.grid % 9) + 1))


## Padding 

constraints_pad_top = {"incompatible_shapes": [], 
                           "incompatible_transforms": [],
                           "application_order": [],
                           "can_be_applied_multiple_times": True,
                           }

def pad_top(shape): 
    "pads shape top side of the shape with TRANSFORMATION_PADDING_COLOR"
    shape_grid = shape.as_shape_only_grid
    shape_position = shape.current_position
    shape_dim = shape_grid.shape
    new_shape = np.zeros((shape_dim[0]+1, shape_dim[1]))
    new_shape[1:, :] = shape_grid
    new_shape[0, :] = PADDING_TOP
    new_shape = Shape(new_shape)
    new_shape.move_to_position((shape_position[0]-1, shape_position[1]))
    return new_shape

constraints_pad_bottom = {"incompatible_shapes": [], 
                           "incompatible_transforms": [],
                           "application_order": [],
                           "can_be_applied_multiple_times": True,
                           }

def pad_bottom(shape):
    "pads shape bottom side of the shape with TRANSFORMATION_PADDING_COLOR"
    shape_grid = shape.as_shape_only_grid
    shape_position = shape.current_position
    shape_dim = shape_grid.shape
    new_shape = np.zeros((shape_dim[0]+1, shape_dim[1]))
    new_shape[:-1, :] = shape_grid
    new_shape[-1, :] = PADDING_BOTTOM
    new_shape = Shape(new_shape)
    new_shape.move_to_position((shape_position[0], shape_position[1]))
    return new_shape

constraints_pad_left = {"incompatible_shapes": [], 
                           "incompatible_transforms": [],
                           "application_order": [],
                           "can_be_applied_multiple_times": True,
                           }

def pad_left(shape):
    "pads shape left side of the shape with TRANSFORMATION_PADDING_COLOR"
    shape_grid = shape.as_shape_only_grid
    shape_position = shape.current_position
    shape_dim = shape_grid.shape
    new_shape = np.zeros((shape_dim[0], shape_dim[1]+1))
    new_shape[:, 1:] = shape_grid
    new_shape[:, 0] = PADDING_LEFT
    new_shape = Shape(new_shape)
    new_shape.move_to_position((shape_position[0], shape_position[1]-1))
    return new_shape

constraints_pad_right = {"incompatible_shapes": [], 
                           "incompatible_transforms": [],
                           "application_order": [],
                           "can_be_applied_multiple_times": True,
                           }                

def pad_right(shape):
    "pads shape right side of the shape with TRANSFORMATION_PADDING_COLOR"
    shape_grid = shape.as_shape_only_grid
    shape_position = shape.current_position
    shape_dim = shape_grid.shape
    new_shape = np.zeros((shape_dim[0], shape_dim[1]+1))
    new_shape[:, :-1] = shape_grid
    new_shape[:, -1] = PADDING_RIGHT
    new_shape = Shape(new_shape)
    new_shape.move_to_position((shape_position[0], shape_position[1]))
    return new_shape

constraints_pad_shape = {"incompatible_shapes": [], 
                           "incompatible_transforms": [],
                           "application_order": [],
                           "can_be_applied_multiple_times": True,
                           }  

def pad_shape(shape):
    """Pads the shape with TRANSFORMATION_PADDING_COLOR in all directions.
    """
    shape_grid = shape.as_shape_only_grid
    shape_position = shape.current_position
    shape_dim = shape_grid.shape
    new_shape = np.zeros((shape_dim[0]+2, shape_dim[1]+2))
    new_shape[1:-1, 1:-1] = shape_grid
    new_shape[0, :] = PADDING_TOP
    new_shape[-1, :] = PADDING_BOTTOM
    new_shape[:, 0] = PADDING_LEFT
    new_shape[:, -1] = PADDING_RIGHT
    new_shape = Shape(new_shape)
    new_shape.move_to_position((shape_position[0]-1, shape_position[1]-1))
    return new_shape

## Double Shape 

constraints_double_right = {"incompatible_shapes": [], 
                           "incompatible_transforms": [],
                           "application_order": [],
                           "can_be_applied_multiple_times": True,
                           }  

def double_right(shape):
    """Doubles the shape to the right"""
    new_shape = np.zeros((shape.n_rows, shape.n_cols*2))
    new_shape[:, :shape.n_cols] = shape.as_shape_only_grid
    new_shape[:, shape.n_cols:] = shape.as_shape_only_grid
    new_shape = Shape(new_shape)
    new_shape.move_to_position((shape.current_position[0], shape.current_position[1]))
    return new_shape

constraints_double_down = {"incompatible_shapes": [], 
                           "incompatible_transforms": [],
                           "application_order": [],
                           "can_be_applied_multiple_times": True,
                           }  

def double_down(shape):
    """Doubles the shape down"""
    new_shape = np.zeros((shape.n_rows*2, shape.n_cols))
    new_shape[:shape.n_rows, :] = shape.as_shape_only_grid
    new_shape[shape.n_rows:, :] = shape.as_shape_only_grid
    new_shape = Shape(new_shape)
    new_shape.move_to_position((shape.current_position[0], shape.current_position[1]))
    return Shape(new_shape)

constraints_double_up = {"incompatible_shapes": [], 
                           "incompatible_transforms": [],
                           "application_order": [],
                           "can_be_applied_multiple_times": True,
                           }  

def double_up(shape):
    """Doubles the shape up"""
    new_shape = np.zeros((shape.n_rows*2, shape.n_cols))
    new_shape[shape.n_rows:, :] = shape.as_shape_only_grid
    new_shape[:shape.n_rows, :] = shape.as_shape_only_grid
    new_shape = Shape(new_shape)
    new_shape.move_to_position((shape.current_position[0] - shape.n_rows, shape.current_position[1]))
    return new_shape

constraints_double_left = {"incompatible_shapes": [], 
                           "incompatible_transforms": [],
                           "application_order": [],
                           "can_be_applied_multiple_times": True,
                           }  

def double_left(shape):
    """Doubles the shape to the left"""
    new_shape = np.zeros((shape.n_rows, shape.n_cols*2))
    new_shape[:, :shape.n_cols] = shape.as_shape_only_grid
    new_shape[:, shape.n_cols:] = shape.as_shape_only_grid
    new_shape = Shape(new_shape)
    new_shape.move_to_position((shape.current_position[0], shape.current_position[1] - shape.n_cols))
    return Shape(new_shape)


constraints_quadruple_shape = {"incompatible_shapes": [], 
                           "incompatible_transforms": [],
                           "application_order": [],
                           "can_be_applied_multiple_times": True,
                           }  

def quadruple_shape(shape):
    """Doubles the shape to the right"""
    new_shape = np.zeros((shape.n_rows*2, shape.n_cols*2))
    new_shape[:shape.n_rows, :shape.n_cols] = shape.as_shape_only_grid
    new_shape[shape.n_rows:, :shape.n_cols] = shape.as_shape_only_grid
    new_shape[:shape.n_rows, shape.n_cols:] = shape.as_shape_only_grid
    new_shape[shape.n_rows:, shape.n_cols:] = shape.as_shape_only_grid
    new_shape = Shape(new_shape)
    new_shape.move_to_position((shape.current_position[0] - shape.n_rows, shape.current_position[1] - shape.n_cols))
    return Shape(new_shape)


transformations_dict = {
    'translate_up': translate_up,
    'translate_down': translate_down,
    'translate_right': translate_right,
    'translate_left': translate_left,
    'rot90': rot90,
    'fill_holes_same_color': fill_holes_same_color,
    'fill_holes_different_color': fill_holes_different_color,
    'mirror_horizontal': mirror_horizontal,
    'mirror_vertical': mirror_vertical,
    'crop_top_side': crop_top_side,
    'crop_bottom_side': crop_bottom_side,
    'crop_left_side': crop_left_side,
    'crop_right_side': crop_right_side, 
    'empty_inside_pixels': empty_inside_pixels,
    'extend_contours_same_color': extend_contours_same_color,
    'extend_contours_different_color': extend_contours_different_color,
    'change_shape_color': change_shape_color,
    'pad_top': pad_top,
    'pad_bottom': pad_bottom,
    'pad_left': pad_left,
    'pad_right': pad_right,
    'pad_shape': pad_shape,
    'double_right': double_right,
    'double_down': double_down,
    'double_up': double_up,
    'double_left': double_left,
    'quadruple_shape': quadruple_shape,
    'crop_contours': crop_contours,
}

transformations_constraints = {
    'translate_up': constraints_translate_up,
    'translate_down': constraints_translate_down,
    'translate_right': constraints_translate_right,
    'translate_left': constraints_translate_left,
    'rot90': constraints_rot90,
    'fill_holes_same_color': constraints_fill_holes_same_color,
    'fill_holes_different_color': constraints_fill_holes_same_color,
    'mirror_horizontal': constraints_mirror_horizontal,
    'mirror_vertical': constraints_mirror_vertical,
    'crop_top_side': constraints_crop_top_side,
    'crop_bottom_side': constraints_crop_bottom_side,
    'crop_left_side': constraints_crop_left_side,
    'crop_right_side': constraints_crop_right_side,
    'empty_inside_pixels': constraints_empty_inside_pixels,
    'extend_contours_same_color': constraints_extend_contours_same_color, 
    'extend_contours_different_color': constraints_extend_contours_different_color,
    'change_shape_color': constraints_change_shape_color,
    'pad_top': constraints_pad_top,
    'pad_bottom': constraints_pad_bottom,
    'pad_left': constraints_pad_left,
    'pad_right': constraints_pad_right,
    'pad_shape': constraints_pad_shape,
    'double_right': constraints_double_right,
    'double_down': constraints_double_down,
    'double_up': constraints_double_up,
    'double_left': constraints_double_left,
    'quadruple_shape': constraints_quadruple_shape,
    'crop_contours': constraints_crop_contours,
}