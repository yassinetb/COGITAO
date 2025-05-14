import random
from matplotlib import pyplot as plt
import scipy
import json
import os
import copy
import numpy as np
from arcworld.constants import COLORMAP, NORM, DoesNotFitException
from arcworld.shapes.base import Shape
from arcworld.shapes.utils import grid_to_cropped_grid, shift_indexes, grid_to_pc
from scipy.ndimage import binary_dilation

###################################################### PLOTTING ######################################################

def plot_grid(grid, title = '', size = (10,10), save_path = None):
    '''Plot a single grid. Possibly, save it to a file, with high resolution.'''

    fig, ax = plt.subplots(1, 1, figsize= size, dpi=300)
    ax.imshow(grid, cmap=COLORMAP, norm=NORM)
    ax.grid(True, which='both', color='lightgrey', linewidth=0.5)
    ax.set_yticks([x - 0.5 for x in range(1 + len(grid))])
    ax.set_xticks([x - 0.5 for x in range(1 + len(grid[0]))])
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_title(title)
    if type(save_path) == str:
        plt.savefig(save_path)

    

def plot_task(task, size = (18,8)):
    '''Plot full task (input and output examples) with appropriate title'''
    fig, axs = plt.subplots(2, len(task["pairs"]), figsize=size)

        
    if len(task['pairs']) == 1:
        for i in range(len(task['pairs'])):     
            axs[0].imshow(task['pairs'][i]['input'], cmap=COLORMAP, norm=NORM)
            axs[0].grid(True,which='both',color='lightgrey', linewidth=0.5)    
            axs[0].set_yticks([x-0.5 for x in range(1+task['pairs'][i]['input'].shape[0])])
            axs[0].set_xticks([x-0.5 for x in range(1+task['pairs'][i]['input'].shape[1])])    
            axs[0].set_xticklabels([])
            axs[0].set_yticklabels([])
            axs[0].set_title('Input ' + str(i+1))
        for i in range(len(task["pairs"])):     
            axs[1].imshow(task['pairs'][i]['output'], cmap=COLORMAP, norm=NORM)
            axs[1].grid(True,which='both',color='lightgrey', linewidth=0.5)
            axs[1].set_yticks([x-0.5 for x in range(1+task['pairs'][i]['output'].shape[0])])
            axs[1].set_xticks([x-0.5 for x in range(1+task['pairs'][i]['output'].shape[1])])   
            axs[1].set_xticklabels([])
            axs[1].set_yticklabels([])
            axs[1].set_title('Output ' + str(i+1))
    
    elif len(task['pairs']) > 1:
        for i in range(len(task['pairs'])):     
            axs[0,i].imshow(task['pairs'][i]['input'], cmap=COLORMAP, norm=NORM)
            axs[0,i].grid(True,which='both',color='lightgrey', linewidth=0.5)    
            axs[0,i].set_yticks([x-0.5 for x in range(1+task['pairs'][i]['input'].shape[0])])
            axs[0,i].set_xticks([x-0.5 for x in range(1+task['pairs'][i]['input'].shape[1])])    
            axs[0,i].set_xticklabels([])
            axs[0,i].set_yticklabels([])
            axs[0,i].set_title('Input ' + str(i+1))
        for i in range(len(task["pairs"])):     
            axs[1,i].imshow(task['pairs'][i]['output'], cmap=COLORMAP, norm=NORM)
            axs[1,i].grid(True,which='both',color='lightgrey', linewidth=0.5)
            axs[1,i].set_yticks([x-0.5 for x in range(1+task['pairs'][i]['output'].shape[0])])
            axs[1,i].set_xticks([x-0.5 for x in range(1+task['pairs'][i]['output'].shape[1])])   
            axs[1,i].set_xticklabels([])
            axs[1,i].set_yticklabels([])
            axs[1,i].set_title('Output ' + str(i+1))

    
    fig.suptitle(task["transformation_suite"])
    plt.tight_layout()
    plt.show()

def plot_json_ARC_task(file_path: str, title = None):
    """
    Plots a task in the json format given by the original ARC dataset.
    Args:
        file: Path to the json file containing the task.
    """

    with open(file_path) as f:
        data = json.load(f)

    n_train = len(data["train"])
    samples = data["train"] + data["test"]

    fig, axes = plt.subplots(2, len(samples))

    for i, subtask in enumerate(samples):
        for j, grid in enumerate([subtask["input"], subtask["output"]]):
            h = len(grid)
            w = len(grid[0])

            grid_title = ""

            if i < n_train:
                if j == 0:
                    grid_title += f"input {i}"
                else:
                    grid_title += f"output {i}"
            else:
                if j == 0:
                    grid_title += "test input"
                else:
                    grid_title += "test output"

            axes[j, i].imshow(grid, cmap=COLORMAP, norm=NORM)
            axes[j, i].grid(True, which="both", color="lightgrey", linewidth=0.5)
            axes[j, i].set_xticks([x - 0.5 for x in range(w)])
            axes[j, i].set_yticks([x - 0.5 for x in range(h)])
            axes[j, i].set_yticklabels([])
            axes[j, i].set_xticklabels([])

            axes[j, i].set_title(grid_title)

    if title == None: 
        fig.suptitle(f"{os.path.basename(file_path)}")
    else: 
        fig.suptitle(title)
    plt.show()

###################################################### GRID ASSEMBLY ##################################################

def find_possible_positions_diagonal(world, grid, allow_holes = True) -> list([(int, int), ]):

    '''Finds all possible positions for the grid in the world, using 4-connectivity'''
    '''This function thus returns all possible positions for the grid in the world, *including diagonal touch* '''

    world = world.copy()
    grid = grid_to_cropped_grid(grid)
    world[world != 0] = 1
    grid[grid != 0] = 1

    if allow_holes == False:
        grid = scipy.ndimage.binary_fill_holes(grid).astype(int)
        world = scipy.ndimage.binary_fill_holes(world).astype(int)
    if world.shape[0] < grid.shape[0] or world.shape[1] < world.shape[1]:
        return []

    res = (scipy.signal.correlate2d(world, grid, mode='same', fillvalue=1) == 0).astype(int)
    # values that are 0 are possible positions, but they use the middle as position
    # and not the top left corner, so shift to get top left corners
    dx = (grid.shape[0] - 1) // 2 * -1
    dy = (grid.shape[1] - 1) // 2 * -1
    indexes = shift_indexes(grid_to_pc(res).indexes, dx, dy)

    return indexes

def find_possible_positions_no_diagonal(original_grid, object_to_position):
    '''Finds all possible positions for the grid in the world, using 8-connectivity'''
    '''This function thus returns all possible positions for the grid in the world, *NOT including diagonal touch* '''
    # Slower version that checks for 8-connectivity
    m, n = original_grid.shape
    h, w = object_to_position.shape
    
    # Precompute valid search space
    safe_positions = []
    object_mask = (object_to_position != 0)
    
    # Create a binary dilation of non-zero grid cells for faster neighbor checking
    
    # Create a 3x3 structuring element for 8-connectivity
    structure = np.ones((3, 3), dtype=bool)
    # Dilate non-zero cells to mark their 8-connected neighborhood
    danger_zone = binary_dilation(original_grid != 0, structure=structure)
    
    # Vectorize the position checking
    valid_i = np.arange(m - h + 1)
    valid_j = np.arange(n - w + 1)
    jj, ii = np.meshgrid(valid_j, valid_i)
    
    # Flatten for iteration
    positions = np.column_stack((ii.ravel(), jj.ravel()))
    
    for i, j in positions:
        # Check if any part of the object would overlap with danger zone
        region = danger_zone[i:i+h, j:j+w]
        if not np.any(region & object_mask):
            safe_positions.append((i, j))
    
    return safe_positions


def randomly_add_shape_to_world(world, shape, background = 0, allow_touching_objects = False):
    '''Randomly chooses position for the shape in the grid'''
    shape = Shape(shape)
    zeroedworld = world.copy()
    zeroedworld[world == background] = 0

    positions = find_possible_positions_no_diagonal(zeroedworld, shape.as_shape_only_grid)

    if len(positions) == 0:
        raise DoesNotFitException('Shape does not fit')
    
    position = random.choice(positions)
    shape.move_to_position(position)
    shape_grid_at_world_size = shape.grid[:world.shape[0], :world.shape[1]]
    world[shape_grid_at_world_size > 0] = shape_grid_at_world_size[shape_grid_at_world_size>0]
    return world, shape

def position_shape_in_world(world, shape, check_for_overlap = True):
    new_world = copy.deepcopy(world)
    if check_for_overlap:
        if check_if_shape_can_be_positionned_in_world(new_world, shape):
            for idx in shape.pc:
                new_world[idx] = shape.pc[idx]
            return new_world
        raise DoesNotFitException
    else:
        for idx in shape.pc:
            new_world[idx] = shape.pc[idx]
        return new_world


def check_if_shape_can_be_positionned_in_world(world, shape):
    '''assesses whether the shape new current position can be positionned in the world'''
    return shape.current_position in find_possible_positions_diagonal(world, shape.as_shape_only_grid)

################################################## TASK GENERATION ########################################################

def generate_key(key_length = 9):
    """ generates a random task identifier """
    key = ''
    for i in range(key_length):
        if random.choice((True, False)):
            key += chr(random.randint(48, 57))
        else:
            key += chr(random.randint(97, 122))
    return key

def from_generated_task_to_arc_json_format(ex):
    dic_to_export = {'train': [], 'test': []}
    n_examples = len(ex)
    for i, e in enumerate(ex):
        input = (np.int_(e['input'])).tolist()
        output = (np.int_(e['output'])).tolist()
        dic_to_append = {'input': input, 'output': output}
        if i < (n_examples-1):
            dic_to_export['train'].append(dic_to_append)
        elif i == n_examples-1:
            dic_to_export['test'].append(dic_to_append)
    return dic_to_export
    
