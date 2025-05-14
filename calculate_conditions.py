import sys

import h5py
from tqdm import tqdm

sys.path.append('../../')
import numpy as np
from arcworld.conditionals.single_shape_conditionals import conditionals_dict
from arcworld.hdf5_utils import get_nr_of_shapes, load_shape, save_conditions, load_conditions, SHAPE_DATASET_PATH
from arcworld.shapes.base import Shape


def map_indexes_to_names(names, prev_calculated_conditions):
    next_index = len(prev_calculated_conditions)
    all_conditions = prev_calculated_conditions.copy()
    names_dict = {}
    for name in names:
        try:
            names_dict[name] = prev_calculated_conditions.index(name)
        except ValueError:
            names_dict[name] = next_index
            next_index = next_index +1
            all_conditions.append(name)
    return names_dict, all_conditions


def calculate_conditions(condition_list = None, recalculate = False):

    """Set recalculate to True in order to recalculate all conditions
    Otherwise only conditions specified in condition_list are created/overwritten"""

    if not condition_list and not recalculate:
        print('No conditions specified. Set recalculate to True in order'
              'to recalculate all conditions')
        return

    n_shapes = get_nr_of_shapes()

    if not recalculate:
        #dont recreate the whole table, only update a column
        condition_table, prev_calculated_conditions = load_conditions()
        #get the indexes that need to be updated
        condition_names_idx, all_conditions = map_indexes_to_names(condition_list, prev_calculated_conditions)
        #extend the table in case the condition is new
        prev_max = condition_table.shape[1] - 1
        current_max = max(condition_names_idx.values())
        if current_max > prev_max:
            n_new_cols = current_max - prev_max
            condition_table = np.concatenate((condition_table, np.zeros((n_shapes, n_new_cols))), axis=1)
    else:
        n_conditionals = len(conditionals_dict.keys())
        condition_list = list(conditionals_dict.keys())
        condition_names_idx, all_conditions = map_indexes_to_names(condition_list, [])
        condition_table = np.zeros((n_shapes, n_conditionals))

    f = h5py.File(SHAPE_DATASET_PATH)
    for shape_idx in tqdm(range(n_shapes)):
        shape = load_shape(shape_idx, f= f)
        shape = Shape(shape)
        for cond, i in condition_names_idx.items():
            if conditionals_dict[cond](shape) == True:
                condition_table[shape_idx][i] = 1

    f.close()
    save_conditions(condition_table, all_conditions)


if __name__ == "__main__":
    # If you only have one condition (e.g. "is_shape_super_cool"), run:
    # calculate_conditions(['is_shape_not_fully_connected'])
    
    # If you would like to recompute the entire set of conditions, run:
    calculate_conditions(recalculate=True)