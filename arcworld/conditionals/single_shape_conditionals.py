import numpy as np
import scipy
from arcworld.shapes.base import Shape 


####################################################### CONDITIONALS TO ADD #########################################################

## is_shape_cross_like

## is_shape_T_like

## is_shape_L_like

## is_shape_two_lines

## is_sparse (must not be true when object is T or L shape for e.g.)

#################################################### SHAPE SYMMETRY #################################################################



def mirror_horizontal(shape):
    position = shape.current_position
    mirrored = Shape(np.flipud(shape.grid))
    mirrored.move_to_position(position)
    return mirrored

def mirror_vertical(shape):
    position = shape.current_position
    mirrored = Shape(np.fliplr(shape.grid))
    mirrored.move_to_position(position)
    return mirrored

def is_shape_vertically_symmetric(shape):
    new_shape = mirror_vertical(shape)
    return new_shape.indexes == shape.indexes

def is_shape_horizontally_symmetric(shape):
    new_shape = mirror_horizontal(shape)
    return new_shape.indexes == shape.indexes

def is_shape_horizontally_or_vertically_symmetric(shape):
    return is_shape_vertically_symmetric(shape) or is_shape_horizontally_symmetric(shape)

def is_shape_diagonally_symmetric(shape):
    if shape.n_rows != shape.n_cols: # Check if the input array is square
        return False
    return np.array_equal(shape.as_shape_only_grid, shape.as_shape_only_grid.T)

def is_shape_antidiagonally_symmetric(shape):
    if shape.n_rows != shape.n_cols:
        return False
    flipped_cropped_grid = np.fliplr(shape.as_shape_only_grid)
    return is_shape_diagonally_symmetric(Shape(flipped_cropped_grid))

def is_shape_diagonally_or_antidiagonally_symmetric(shape):
    return is_shape_antidiagonally_symmetric(shape) or is_shape_diagonally_symmetric(shape)

def is_shape_symmetric(shape):
    '''checks if shape presents any form of symmetry'''
    return is_shape_diagonally_or_antidiagonally_symmetric(shape) or is_shape_horizontally_or_vertically_symmetric(shape) 

def is_shape_not_symmetric(shape):
    return not is_shape_symmetric(shape)

#################################################### SHAPE COLORING #################################################################

def is_shape_evenly_colored(shape):
    return len(shape.existing_colors) == 1

def is_shape_not_evenly_colored(shape):
    return len(shape.existing_colors) > 1

def is_shape_of_2_colors(shape):
    return len(shape.existing_colors) == 2

def is_shape_of_3_colors(shape):
    return len(shape.existing_colors) == 3

def is_shape_more_than_3_colors(shape):
    return len(shape.existing_colors) > 3

def is_shape_hollow(shape):
    shape_only_grid = shape.as_shape_only_grid
    img_fill_holes = scipy.ndimage.binary_fill_holes(shape_only_grid)
    return not np.array_equal((shape_only_grid!= 0).astype(np.int_), img_fill_holes)

def is_shape_not_hollow(shape):
    return not is_shape_hollow(shape)

################################################### SHAPE "FOOTPRINT" ###############################################################


def is_shape_simple(shape):
    '''Function to check whether this shape is "simple" - it's a combination of 1) evenly colored 2) symmetric 3) more than 2 cell 4) no sparsity
    We want to avoid single pixels or lines of two pixels and have some actual objects here that are not too complicated to the human eye to read and interpret'''
    return is_shape_symmetric(shape) and is_shape_evenly_colored(shape) and is_shape_more_than_2_cell(shape) and is_shape_fully_connected(shape)

def is_shape_not_simple(shape):
    '''Not is_shape_simple'''
    return not is_shape_simple(shape)

def is_shape_line(shape):
    return shape.n_cols == 1 or shape.n_rows == 1

def is_shape_vertical_line(shape):
    return shape.n_cols == 1

def is_shape_horizontal_line(shape):
    return shape.n_rows == 1

def is_shape_diagonal_line(shape):
    for i in range(shape.n_rows):
        for j in range(shape.n_cols):
            if i == j and shape.grid[i,j] == 0:
                return False
            if i != j and shape.grid[i,j] != 0:
                return False
    return True

def is_shape_anti_diagonal_line(shape):
    for i in range(shape.n_rows):
        for j in range(shape.n_cols):
            if i + j == (shape.n_rows - 1) and shape.grid[i,j] == 0:
                return False
            if i + j != (shape.n_rows - 1) and shape.grid[i,j] != 0:
                return False
    return True

def is_shape_diagonal_or_antidiagonal_line(shape):
    return is_shape_diagonal_line(shape) or is_shape_anti_diagonal_line(shape)

def is_shape_filled_square(shape):
    return shape.n_rows == shape.n_cols and is_shape_evenly_colored(shape) == True

def is_shape_filled_rectangle(shape):
    return shape.n_rows != shape.n_cols and is_shape_evenly_colored(shape) == True

def is_shape_filled_square(shape):
    return shape.n_rows == shape.n_cols and is_shape_evenly_colored(shape) == True

def is_shape_filled_rectangle(shape):
    return shape.n_rows != shape.n_cols and is_shape_evenly_colored(shape) == True

def is_shape_fully_connected(shape):
    '''check if shape is fully connected (i.e. not sparse // with different disconnected bits)'''
    footprint = scipy.ndimage.generate_binary_structure(2,2)
    _, num_connected = scipy.ndimage.label(shape.grid, footprint)
    return num_connected == 1

def is_shape_not_fully_connected(shape):
    return not is_shape_fully_connected(shape)

####################################################### SHAPE SIZE ##################################################################

def is_shape_higher_than_wide(shape):
    return shape.n_rows > shape.n_cols

def is_shape_wider_than_high(shape):
    return shape.n_rows < shape.n_cols

def is_shape_same_height_width(shape):
    return shape.n_rows == shape.n_cols

def is_shape_of_two_cols(shape):
    return shape.n_cols == 2

def is_shape_of_three_cols(shape):
    return shape.n_cols == 3

def is_shape_of_four_cols(shape):
    return shape.n_cols == 4

def is_shape_of_five_cols(shape):
    return shape.n_cols == 5

def is_shape_of_two_rows(shape):
    return shape.n_rows == 2

def is_shape_of_three_rows(shape):
    return shape.n_rows == 3

def is_shape_of_four_rows(shape):
    return shape.n_rows == 4

def is_shape_of_five_rows(shape):
    return shape.n_rows == 5

def is_shape_more_than_1_cell(shape):
    return shape.num_points > 1

def is_shape_more_than_2_cell(shape):
    return shape.num_points > 2

def is_shape_more_than_3_cell(shape):
    return shape.num_points > 3

def is_shape_more_than_4_cell(shape):
    return shape.num_points > 4

def is_shape_more_than_5_cell(shape):
    return shape.num_points > 5

def is_shape_more_than_6_cell(shape):
    return shape.num_points > 6

def is_shape_less_than_2_cell(shape):
    return shape.num_points < 2

def is_shape_less_than_3_cell(shape):
    return shape.num_points < 3

def is_shape_less_than_4_cell(shape):
    return shape.num_points < 4

def is_shape_less_than_5_cell(shape):
    return shape.num_points < 5

def is_shape_less_than_6_cell(shape):
    return shape.num_points < 6

def is_shape_less_than_6_rows(shape):
    return shape.n_rows < 6

def is_shape_less_than_5_rows(shape):
    return shape.n_rows < 5

def is_shape_less_than_4_rows(shape):
    return shape.n_rows < 4

def is_shape_less_than_3_rows(shape):
    return shape.n_rows < 3

def is_shape_less_than_2_rows(shape):
    return shape.n_rows < 2

def is_shape_less_than_6_cols(shape):
    return shape.n_cols < 6

def is_shape_less_than_5_cols(shape):
    return shape.n_cols < 5

def is_shape_less_than_4_cols(shape):
    return shape.n_cols < 4

def is_shape_less_than_3_cols(shape):
    return shape.n_cols < 3

def is_shape_less_than_2_cols(shape):
    return shape.n_cols < 2

def is_shape_small(shape):
    return shape.n_cols < 9 and shape.n_rows < 9

def is_shape_more_than_5_rows(shape):
    return shape.n_rows > 5

def is_shape_more_than_5_cols(shape):
    return shape.n_cols > 5

def is_shape_less_than_11_rows(shape):
    return shape.n_rows < 11

def is_shape_less_than_11_cols(shape):
    return shape.n_cols < 11

def is_shape_less_than_9_rows(shape):
    return shape.n_rows < 9

def is_shape_less_than_9_cols(shape):
    return shape.n_cols < 9


########################################################## CONDITIONAL DICT WITH ALL FUNCTION POINTERS ######################################################

conditionals_dict = {
            'is_shape_vertically_symmetric': is_shape_vertically_symmetric,
            'is_shape_horizontally_symmetric': is_shape_horizontally_symmetric,
            'is_shape_horizontally_or_vertically_symmetric': is_shape_horizontally_or_vertically_symmetric,
            'is_shape_diagonally_symmetric': is_shape_diagonally_symmetric,
            'is_shape_antidiagonally_symmetric': is_shape_antidiagonally_symmetric,
            'is_shape_diagonally_or_antidiagonally_symmetric': is_shape_diagonally_or_antidiagonally_symmetric,
            'is_shape_symmetric': is_shape_symmetric,
            'is_shape_not_symmetric': is_shape_not_symmetric,
            'is_shape_of_2_colors': is_shape_of_2_colors,
            'is_shape_of_3_colors': is_shape_of_3_colors,
            'is_shape_more_than_3_colors': is_shape_more_than_3_colors,
            'is_shape_evenly_colored': is_shape_evenly_colored,
            'is_shape_not_evenly_colored': is_shape_not_evenly_colored,
            'is_shape_simple': is_shape_simple,
            'is_shape_not_simple': is_shape_not_simple,
            'is_shape_hollow': is_shape_hollow,
            'is_shape_not_hollow': is_shape_not_hollow,
            'is_shape_line': is_shape_line,
            'is_shape_vertical_line': is_shape_vertical_line,
            'is_shape_horizontal_line': is_shape_horizontal_line,
            'is_shape_diagonal_line': is_shape_diagonal_line,
            'is_shape_anti_diagonal_line': is_shape_anti_diagonal_line,
            'is_shape_diagonal_or_antidiagonal_line': is_shape_diagonal_or_antidiagonal_line,
            'is_shape_filled_square': is_shape_filled_square,
            'is_shape_filled_rectangle': is_shape_filled_rectangle,            
            'is_shape_fully_connected': is_shape_fully_connected,
            'is_shape_not_fully_connected': is_shape_not_fully_connected,
            'is_shape_higher_than_wide': is_shape_higher_than_wide,
            'is_shape_wider_than_high': is_shape_wider_than_high,
            'is_shape_same_height_width': is_shape_same_height_width,
            'is_shape_of_two_cols': is_shape_of_two_cols,
            'is_shape_of_three_cols': is_shape_of_three_cols,
            'is_shape_of_four_cols': is_shape_of_four_cols,
            'is_shape_of_five_cols': is_shape_of_five_cols,
            'is_shape_of_two_rows': is_shape_of_two_rows,
            'is_shape_of_three_rows': is_shape_of_three_rows,
            'is_shape_of_four_rows': is_shape_of_four_rows, 
            'is_shape_of_five_rows': is_shape_of_five_rows, 
            'is_shape_more_than_1_cell': is_shape_more_than_1_cell,
            'is_shape_more_than_2_cell': is_shape_more_than_2_cell,
            'is_shape_more_than_3_cell': is_shape_more_than_3_cell,
            'is_shape_more_than_4_cell': is_shape_more_than_4_cell,
            'is_shape_more_than_5_cell': is_shape_more_than_5_cell,
            'is_shape_more_than_6_cell': is_shape_more_than_6_cell,
            'is_shape_less_than_2_cell':  is_shape_less_than_2_cell,
            'is_shape_less_than_3_cell':  is_shape_less_than_3_cell,
            'is_shape_less_than_4_cell':  is_shape_less_than_4_cell,
            'is_shape_less_than_5_cell':  is_shape_less_than_5_cell,
            'is_shape_less_than_6_cell':  is_shape_less_than_6_cell,
            'is_shape_less_than_2_rows':  is_shape_less_than_2_rows,
            'is_shape_less_than_3_rows':  is_shape_less_than_3_rows,
            'is_shape_less_than_4_rows':  is_shape_less_than_4_rows,
            'is_shape_less_than_5_rows':  is_shape_less_than_5_rows,
            'is_shape_less_than_6_rows':  is_shape_less_than_6_rows,
            'is_shape_less_than_2_cols':  is_shape_less_than_2_cols,
            'is_shape_less_than_3_cols':  is_shape_less_than_3_cols,
            'is_shape_less_than_4_cols':  is_shape_less_than_4_cols,
            'is_shape_less_than_5_cols':  is_shape_less_than_5_cols,
            'is_shape_less_than_6_cols':  is_shape_less_than_6_cols,
            'is_shape_small': is_shape_small, 
            'is_shape_more_than_5_rows': is_shape_more_than_5_rows,
            'is_shape_more_than_5_cols': is_shape_more_than_5_cols,
            'is_shape_less_than_11_rows': is_shape_less_than_11_rows,
            'is_shape_less_than_11_cols': is_shape_less_than_11_cols, 
            'is_shape_less_than_9_rows': is_shape_less_than_9_rows,
            'is_shape_less_than_9_cols': is_shape_less_than_9_cols,}