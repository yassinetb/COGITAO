import h5py
import sys
import os
from tqdm.auto import tqdm

sys.path.append('../../')

from arcworld.hdf5_utils import save_shape, SHAPE_DATASET_PATH
from arcworld.conditionals.single_shape_conditionals import *
from arcworld.shapes.random_shape import RandomShape

possible_shape_generation_config = {
    "allowed_color_pattern": ["uniform", "top_bot", "left_right", "col_stripes", "row_stripes", "random"],
    "allowed_connectivity": ["4connected", "8connected", "distance"],
    "allowed_max_size": 10,
    "allowed_colors": list(np.arange(1, 10)),
    "allowed_symmetry": ["horizontal", "vertical", "diag_tl_br", "diag_bl_tr", "point", 'no'],
    "allowed_footprints": ["rectangle", "disk", "square", "diamond", "ellipse"]}

def generate_shapes():
    k_obj_per_config = 1
    obj_n = 0
    n_errors = 0
    f = h5py.File(SHAPE_DATASET_PATH, 'a')
    set_of_objects = set()
    
    ## Saving all combinations of objects bigger than single pixel
    for col_p in tqdm(possible_shape_generation_config['allowed_color_pattern'], desc = 'color_pattern', leave = True):
        for foot in tqdm(possible_shape_generation_config['allowed_footprints'], desc = "footprint", leave = False):
            for rows in range(1,15):
                for cols in range(1,15):
                    for k in range(k_obj_per_config):
                        try:
                            s = RandomShape(min_cols = cols, min_rows = rows, max_cols = cols, max_rows = rows,
                                            footprint = foot, color_pattern = col_p, use_footprint = True).as_shape_only_grid
                            

                            hashed_object = hash(s.tobytes())
                            if hashed_object in set_of_objects:
                                continue
                            save_shape(s, obj_n, f)
                            set_of_objects.add(hashed_object)
                            obj_n += 1
                        except Exception as E:
                            n_errors +=1 
                            print('number of errors: ', n_errors, ' -- error: ', E)
                            continue

        for con_p in tqdm(possible_shape_generation_config['allowed_connectivity'], desc = 'connectivity', leave = False):
            for sym in possible_shape_generation_config['allowed_symmetry']:
                for rows in range(1,15):
                    for cols in range(1,15):
                        for k in range(k_obj_per_config):
                            try:
                                s = RandomShape(min_cols = cols, min_rows = rows, max_cols = cols, max_rows = rows,
                                                color_pattern = col_p, connectivity = con_p, symmetry = sym, 
                                                use_footprint = False).as_shape_only_grid
                                hashed_object = hash(s.tobytes())
                                if hashed_object in set_of_objects:
                                    continue
                                save_shape(s, obj_n, f)
                                set_of_objects.add(hashed_object)
                                obj_n += 1
                            except Exception as E:
                                n_errors +=1 
                                print('number of errors: ', n_errors, ' -- error: ', E)
                                continue

    f.close()
    print('successfully generated ', obj_n, ' different shapes')

if __name__ == "__main__":
    generate_shapes()