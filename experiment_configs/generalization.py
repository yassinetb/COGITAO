import copy 

gen_path = "before_arc_datasets/generalization"

gen_base_config = {
    "min_n_shapes_per_grid": None,
    "max_n_shapes_per_grid": None,
    "n_examples": 1,
    "min_grid_size": None,
    "max_grid_size": None,
    "allowed_combinations": None,
    "allowed_transformations": None,
    "min_transformation_depth": None,
    "max_transformation_depth": None,
    "shape_compulsory_conditionals": ["is_shape_less_than_6_rows", 
                                      "is_shape_less_than_6_cols", 
                                      "is_shape_fully_connected"],
    "saving_path": None,
}

def make_config(transform, grid_size_min, grid_size_max, n_obj_min, n_obj_max, setting, exp_number, split, compulsory_conditions=None):
    config = copy.deepcopy(gen_base_config)
    config["allowed_combinations"] = transform
    config["min_n_shapes_per_grid"] = n_obj_min
    config["max_n_shapes_per_grid"] = n_obj_max
    config["min_grid_size"] = grid_size_min
    config["max_grid_size"] = grid_size_max
    config["saving_path"] = f"{gen_path}/exp_setting_{setting}/experiment_{exp_number}/{split}.json"
    if compulsory_conditions != None:
        config["shape_compulsory_conditionals"] = compulsory_conditions
    return config

generalization_configs = []

# === Setting 1 === N shapes generalization 

exps_1 = [
    ([["translate_up"]],      15, 15, 1, 2, 1, 1, "train"),
    ([["translate_up"]],      15, 15, 3, 4, 1, 1, "test"),
    ([["rot90"]],             15, 15, 1, 2, 1, 2, "train"),
    ([["rot90"]],             15, 15, 3, 4, 1, 2, "test"),
    ([["mirror_horizontal"]], 15, 15, 1, 2, 1, 3, "train"),
    ([["mirror_horizontal"]], 15, 15, 3, 4, 1, 3, "test"),
    ([["crop_top_side"]],     15, 15, 1, 2, 1, 4, "train"),
    ([["crop_top_side"]],     15, 15, 3, 4, 1, 4, "test"),
    ([["extend_contours_same_color"]],         15, 15, 1, 2, 1, 5, "train"),
    ([["extend_contours_same_color"]],         15, 15, 3, 4, 1, 5, "test"),
]

for transform, grid_size_min, grid_size_max, n_obj_min, n_obj_max, setting, exp_number, split in exps_1:
    generalization_configs.append(make_config(transform, grid_size_min, grid_size_max, n_obj_min, n_obj_max, setting, exp_number, split))


# === Setting 2 === Grid size generalization

exps_2 = [
    ([["translate_up"]],      10, 15, 2, 2, 2, 1, "train"),
    ([["translate_up"]],      16, 20, 2, 2, 2, 1, "test"),
    ([["rot90"]],             10, 15, 2, 2, 2, 2, "train"),
    ([["rot90"]],             16, 20, 2, 2, 2, 2, "test"),
    ([["mirror_horizontal"]], 10, 15, 2, 2, 2, 3, "train"),
    ([["mirror_horizontal"]], 16, 20, 2, 2, 2, 3, "test"),
    ([["crop_top_side"]],     10, 15, 2, 2, 2, 4, "train"),
    ([["crop_top_side"]],     16, 20, 2, 2, 2, 4, "test"),
    ([["extend_contours_same_color"]],         10, 15, 2, 2, 2, 5, "train"),
    ([["extend_contours_same_color"]],         16, 20, 2, 2, 2, 5, "test"),
]

for transform, grid_size_min, grid_size_max, n_obj_min, n_obj_max, setting, exp_number, split in exps_2:
    generalization_configs.append(make_config(transform, grid_size_min, grid_size_max, n_obj_min, n_obj_max, setting, exp_number, split))


# === Setting 3 === Object Dimension Generalization 

exps_3 = [                      
    ([["translate_up"]],             15, 15, 2, 2, 3, 1, "train", ["is_shape_less_than_5_rows", "is_shape_less_than_5_cols", "is_shape_fully_connected"]),
    ([["translate_up"]],             15, 15, 2, 2, 3, 1, "test", ["is_shape_less_than_9_rows", "is_shape_less_than_9_cols", "is_shape_more_than_5_rows", "is_shape_more_than_5_cols", "is_shape_fully_connected"]), 
    ([["rot90"]],                    15, 15, 2, 2, 3, 2, "train", ["is_shape_less_than_5_rows", "is_shape_less_than_5_cols", "is_shape_fully_connected"]),
    ([["rot90"]],                    15, 15, 2, 2, 3, 2, "test", ["is_shape_less_than_9_rows", "is_shape_less_than_9_cols", "is_shape_more_than_5_rows", "is_shape_more_than_5_cols", "is_shape_fully_connected"]),
    ([["mirror_horizontal"]],        15, 15, 2, 2, 3, 3, "train", ["is_shape_less_than_5_rows", "is_shape_less_than_5_cols", "is_shape_fully_connected"]),
    ([["mirror_horizontal"]],        15, 15, 2, 2, 3, 3, "test", ["is_shape_less_than_9_rows", "is_shape_less_than_9_cols", "is_shape_more_than_5_rows", "is_shape_more_than_5_cols", "is_shape_fully_connected"]),
    ([["crop_top_side"]],            15, 15, 2, 2, 3, 4, "train", ["is_shape_less_than_5_rows", "is_shape_less_than_5_cols", "is_shape_fully_connected"]),
    ([["crop_top_side"]],            15, 15, 2, 2, 3, 4,"test", ["is_shape_less_than_9_rows", "is_shape_less_than_9_cols",  "is_shape_more_than_5_rows", "is_shape_more_than_5_cols", "is_shape_fully_connected"]),
    ([["extend_contours_same_color"]],                15, 20, 2, 2, 3, 5, "train", ["is_shape_less_than_5_rows", "is_shape_less_than_5_cols", "is_shape_fully_connected"]),
    ([["extend_contours_same_color"]],                15, 20, 2, 2, 3, 5,"test", ["is_shape_less_than_9_rows", "is_shape_less_than_9_cols",  "is_shape_more_than_5_rows", "is_shape_more_than_5_cols", "is_shape_fully_connected"])
]

for transform, grid_size_min, grid_size_max, n_obj_min, n_obj_max, setting, exp_number, split, shape_conditionals in exps_3:
    generalization_configs.append(make_config(transform, grid_size_min, grid_size_max, n_obj_min, n_obj_max, setting, exp_number, split, shape_conditionals))

# === Setting 4 === Object Complexity Generalization

exps_4 = [
    ([["translate_up"]],      15, 15, 2, 2, 4, 1, "train", ["is_shape_symmetric", "is_shape_evenly_colored", "is_shape_fully_connected"]),
    ([["translate_up"]],      15, 15, 2, 2, 4, 1, "test", ["is_shape_not_symmetric", "is_shape_not_evenly_colored", "is_shape_fully_connected"]),
    ([["rot90"]],             15, 15, 2, 2, 4, 2, "train", ["is_shape_symmetric", "is_shape_evenly_colored", "is_shape_fully_connected"]),
    ([["rot90"]],             15, 15, 2, 2, 4, 2, "test", ["is_shape_not_symmetric", "is_shape_not_evenly_colored", "is_shape_fully_connected"]),
    ([["mirror_horizontal"]], 15, 15, 2, 2, 4, 3, "train", ["is_shape_symmetric", "is_shape_evenly_colored", "is_shape_fully_connected"]),
    ([["mirror_horizontal"]], 15, 15, 2, 2, 4, 3, "test", ["is_shape_not_symmetric", "is_shape_not_evenly_colored", "is_shape_fully_connected"]),
    ([["crop_top_side"]],     15, 15, 2, 2, 4, 4, "train", ["is_shape_symmetric", "is_shape_evenly_colored", "is_shape_fully_connected"]),
    ([["crop_top_side"]],     15, 15, 2, 2, 4, 4,"test", ["is_shape_not_symmetric", "is_shape_not_evenly_colored", "is_shape_fully_connected"]),
    ([["extend_contours_same_color"]],         15, 15, 2, 2, 4, 5, "train", ["is_shape_symmetric", "is_shape_evenly_colored", "is_shape_fully_connected"]),
    ([["extend_contours_same_color"]],         15, 15, 2, 2, 4, 5,"test", ["is_shape_not_symmetric", "is_shape_not_evenly_colored", "is_shape_fully_connected"]),
]

for transform, grid_size_min, grid_size_max, n_obj_min, n_obj_max, setting, exp_number, split, shape_conditionals in exps_4:
    generalization_configs.append(make_config(transform, grid_size_min, grid_size_max, n_obj_min, n_obj_max, setting, exp_number, split, shape_conditionals))

    
# === Setting 5 === All rules mixed Generalization

exps_5 = [
    ([["translate_up"]],      10, 15, 1, 2, 5, 1, "train", ["is_shape_symmetric", "is_shape_evenly_colored", 
                                                            "is_shape_less_than_5_rows", "is_shape_less_than_5_cols", "is_shape_fully_connected"]),
    ([["translate_up"]],      16, 20, 3, 4, 5, 1, "test", ["is_shape_not_symmetric", "is_shape_not_evenly_colored", 
                                                           "is_shape_less_than_9_rows", "is_shape_less_than_9_cols", 
                                                           "is_shape_more_than_5_rows", "is_shape_more_than_5_cols", "is_shape_fully_connected"]),
    ([["rot90"]],             10, 15, 1, 2, 5, 2, "train", ["is_shape_symmetric", "is_shape_evenly_colored", 
                                                            "is_shape_less_than_5_rows", "is_shape_less_than_5_cols", "is_shape_fully_connected"]),
    ([["rot90"]],             16, 20, 3, 4, 5, 2, "test", ["is_shape_not_symmetric", "is_shape_not_evenly_colored", 
                                                           "is_shape_less_than_9_rows", "is_shape_less_than_9_cols", 
                                                           "is_shape_more_than_5_rows", "is_shape_more_than_5_cols", "is_shape_fully_connected"]),
    ([["mirror_horizontal"]], 10, 15, 1, 2, 5, 3, "train", ["is_shape_symmetric", "is_shape_evenly_colored", 
                                                            "is_shape_less_than_5_rows", "is_shape_less_than_5_cols", "is_shape_fully_connected"]),
    ([["mirror_horizontal"]], 16, 20, 3, 4, 5, 3, "test", ["is_shape_not_symmetric", "is_shape_not_evenly_colored", 
                                                           "is_shape_less_than_9_rows", "is_shape_less_than_9_cols", 
                                                           "is_shape_more_than_5_rows", "is_shape_more_than_5_cols", "is_shape_fully_connected"]),
    ([["crop_top_side"]],     10, 15, 1, 2, 5, 4, "train", ["is_shape_symmetric", "is_shape_evenly_colored", 
                                                            "is_shape_less_than_5_rows", "is_shape_less_than_5_cols", "is_shape_fully_connected"]),
    ([["crop_top_side"]],     16, 20, 3, 4, 5, 4, "test", ["is_shape_not_symmetric", "is_shape_not_evenly_colored", 
                                                           "is_shape_less_than_9_rows", "is_shape_less_than_9_cols", 
                                                           "is_shape_more_than_5_rows", "is_shape_more_than_5_cols", "is_shape_fully_connected"]),
    ([["extend_contours_same_color"]],         10, 15, 1, 2, 5, 5, "train", ["is_shape_symmetric", "is_shape_evenly_colored", 
                                                                "is_shape_less_than_5_rows", "is_shape_less_than_5_cols", "is_shape_fully_connected"]),
    ([["extend_contours_same_color"]],         17, 20, 3, 3, 5, 5, "test", ["is_shape_not_symmetric", "is_shape_not_evenly_colored", 
                                                           "is_shape_less_than_9_rows", "is_shape_less_than_9_cols", 
                                                           "is_shape_more_than_5_rows", "is_shape_more_than_5_cols", "is_shape_fully_connected"]),
]

for transform, grid_size_min, grid_size_max, n_obj_min, n_obj_max, setting, exp_number, split, shape_conditionals in exps_5:
    generalization_configs.append(make_config(transform, grid_size_min, grid_size_max, n_obj_min, n_obj_max, setting, exp_number, split, shape_conditionals))
