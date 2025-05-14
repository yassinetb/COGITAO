import copy

# Default parameters common to all experiments
cp_path = "before_arc_datasets/compositionality"

cp_base_config = {
    "min_n_shapes_per_grid": 2,
    "max_n_shapes_per_grid": 2,
    "n_examples": 1,
    "min_grid_size": 20,
    "max_grid_size": 20,
    "allowed_combinations": None,
    "allowed_transformations": None,
    "min_transformation_depth": None,
    "max_transformation_depth": None,
    "shape_compulsory_conditionals": ["is_shape_less_than_6_rows", 
                                      "is_shape_less_than_6_cols", 
                                      "is_shape_fully_connected"],
    "saving_path": None,
}

def make_config(combos, setting, exp_number, split, min_size = 15, max_size = 15):
    config = copy.deepcopy(cp_base_config)
    config["allowed_combinations"] = combos
    config["saving_path"] = f"{cp_path}/exp_setting_{setting}/experiment_{exp_number}/{split}.json"
    config["min_grid_size"] = min_size
    config["max_grid_size"] = max_size
    return config

compositionality_configs = []


# # === Setting 1 ===

# Exp 1

compositionality_configs.append(make_config(
    [["translate_up"], ["rot90"], ["mirror_horizontal"],
     ["translate_up", "translate_up"], ["rot90", "rot90"],
     ["mirror_horizontal", "mirror_horizontal"],
     ["translate_up", "mirror_horizontal"],
     ["rot90", "mirror_horizontal"],
     ["mirror_horizontal", "rot90"]],
    1, 1, "train"))

compositionality_configs.append(make_config(
    [["translate_up", "rot90"]],
    1, 1, "test"))

# Exp 2

compositionality_configs.append(make_config(
    [["pad_right"], ["fill_holes_different_color"], ["change_shape_color"],
      ["pad_right", "pad_right"],
      ["fill_holes_different_color", "fill_holes_different_color"],
      ["change_shape_color", "change_shape_color"],
      ["pad_right", "fill_holes_different_color"],
      ["fill_holes_different_color", "change_shape_color"],
      ["change_shape_color", "fill_holes_different_color" ],
      ["change_shape_color", "pad_right"]],
    1, 2, "train"))

compositionality_configs.append(make_config(
    [["pad_right", "change_shape_color"]],
    1, 2, "test"))

# Exp 3 

compositionality_configs.append(make_config(
    [["rot90"], ["pad_top"], ["crop_bottom_side"],
      ["rot90", "rot90"],
      ["pad_top", "pad_top"],
      ["crop_bottom_side", "crop_bottom_side"],
      ["rot90", "pad_top"],
      ["pad_top", "crop_bottom_side"],
      ["crop_bottom_side", "rot90"]],
    1, 3, "train"))

compositionality_configs.append(make_config(
    [["rot90", "crop_bottom_side"]],
    1, 3, "test"))

# Exp 4

compositionality_configs.append(make_config(
    [["extend_contours_different_color"], ["mirror_horizontal"], ["translate_down"],
      ["extend_contours_different_color", "extend_contours_different_color"],
      ["mirror_horizontal", "mirror_horizontal"],
      ["translate_down", "translate_down"],
      ["translate_down", "mirror_horizontal"],
      ["extend_contours_different_color", "mirror_horizontal"],
      ["extend_contours_different_color", "translate_down"]],
    1, 4, "train"))

compositionality_configs.append(make_config(
    [["mirror_horizontal", "extend_contours_different_color"]],
    1, 4, "test"))

# Exp 5

compositionality_configs.append(make_config(
    [["extend_contours_same_color"], ["pad_left"], ["mirror_vertical"],
      ["extend_contours_same_color", "extend_contours_same_color"],
      ["pad_left", "pad_left"],
      ["mirror_vertical", "mirror_vertical"],
      ["mirror_vertical", "pad_left"],
      ["extend_contours_same_color", "pad_left"],
      ["extend_contours_same_color", "mirror_vertical"]],
    1, 5, "train"))

compositionality_configs.append(make_config(
    [["pad_left", "extend_contours_same_color"]],
    1, 5, "test"))



# === Setting 2 ===

# Exp 1

compositionality_configs.append(make_config(
    [["translate_up", "translate_up"],
     ["rot90", "rot90"],
     ["mirror_horizontal", "mirror_horizontal"],
     ["translate_up", "mirror_horizontal"],
     ["rot90", "mirror_horizontal"],
     ["mirror_horizontal", "rot90"]],
    2, 1, "train"))

compositionality_configs.append(make_config(
    [["translate_up", "rot90"]],
    2, 1, "test"))

## Exp 2

compositionality_configs.append(make_config(
    [["pad_right", "pad_right"],
      ["fill_holes_different_color", "fill_holes_different_color"],
      ["change_shape_color", "change_shape_color"],
      ["pad_right", "fill_holes_different_color"],
      ["fill_holes_different_color", "change_shape_color"],
      ["change_shape_color", "fill_holes_different_color" ],
      ["change_shape_color", "pad_right"]],
    2, 2, "train"))

compositionality_configs.append(make_config(
    [["pad_right", "change_shape_color"]],
    2, 2, "test"))

## Exp 3

compositionality_configs.append(make_config(
    [["rot90", "rot90"],
      ["pad_top", "pad_top"],
      ["crop_bottom_side", "crop_bottom_side"],
      ["rot90", "pad_top"],
      ["pad_top", "crop_bottom_side"],
      ["crop_bottom_side", "rot90"]],
    2, 3, "train"))

compositionality_configs.append(make_config(
    [["rot90", "crop_bottom_side"]],
    2, 3, "test"))

# Exp 4

compositionality_configs.append(make_config(
    [["extend_contours_different_color", "extend_contours_different_color"],
      ["mirror_horizontal", "mirror_horizontal"],
      ["translate_down", "translate_down"],
      ["translate_down", "mirror_horizontal"],
      ["extend_contours_different_color", "mirror_horizontal"],
      ["extend_contours_different_color", "translate_down"]],
    2, 4, "train"))

compositionality_configs.append(make_config(
    [["mirror_horizontal", "extend_contours_different_color"]],
    2, 4, "test"))


# Exp 5

compositionality_configs.append(make_config(
    [["extend_contours_same_color", "extend_contours_same_color"],
      ["pad_left", "pad_left"],
      ["mirror_vertical", "mirror_vertical"],
      ["mirror_vertical", "pad_left"],
      ["extend_contours_same_color", "pad_left"],
      ["extend_contours_same_color", "mirror_vertical"]],
    2, 5, "train"))

compositionality_configs.append(make_config(
    [["pad_left", "extend_contours_same_color"]],
    2, 5, "test"))

# === Setting 3 ===

# Exp 1

compositionality_configs.append(make_config(
    [["translate_up"], ["mirror_horizontal"], ["rot90"],
     ["translate_up", "translate_up"], ["mirror_horizontal", "mirror_horizontal"], ["rot90", "rot90"],
     ["translate_up", "mirror_horizontal"], ["translate_up", "rot90"],
     ["mirror_horizontal", "rot90"]],
    3, 1, "train", 20, 20))

compositionality_configs.append(make_config(
    [["translate_up", "translate_up", "translate_up"],
     ["translate_up", "translate_up", "mirror_horizontal"],
     ["translate_up", "translate_up", "rot90"],
     ["translate_up", "mirror_horizontal", "mirror_horizontal"],
     ["translate_up", "mirror_horizontal", "rot90"],
     ["translate_up", "rot90", "rot90"],
     ["mirror_horizontal", "mirror_horizontal", "mirror_horizontal"],
     ["mirror_horizontal", "mirror_horizontal", "rot90"],
     ["mirror_horizontal", "rot90", "rot90"],
     ["rot90", "rot90", "rot90"],
     ["translate_up", "mirror_horizontal", "translate_up"],
     ["translate_up", "rot90", "translate_up"],
     ["mirror_horizontal", "rot90", "translate_up"],
     ["mirror_horizontal", "translate_up", "rot90"],
     ["rot90", "translate_up", "mirror_horizontal"],
     ["rot90", "mirror_horizontal", "translate_up"]],
    3, 1, "test", 20, 20))


# Exp 2

compositionality_configs.append(make_config(
    [["pad_right"], ["fill_holes_different_color"], ["change_shape_color"],
      ["pad_right", "pad_right"], ["fill_holes_different_color", "fill_holes_different_color"], ["change_shape_color", "change_shape_color"],
      ["pad_right", "fill_holes_different_color"], ["pad_right", "change_shape_color"],
      ["fill_holes_different_color", "change_shape_color"]],
    3, 2, "train", 20, 20))

compositionality_configs.append(make_config(
    [["pad_right", "pad_right", "pad_right"],
      ["pad_right", "pad_right", "fill_holes_different_color"],
      ["pad_right", "pad_right", "change_shape_color"],
      ["pad_right", "fill_holes_different_color", "fill_holes_different_color"],
      ["pad_right", "fill_holes_different_color", "change_shape_color"],
      ["pad_right", "change_shape_color", "change_shape_color"],
      ["fill_holes_different_color", "fill_holes_different_color", "fill_holes_different_color"],
      ["fill_holes_different_color", "fill_holes_different_color", "change_shape_color"],
      ["fill_holes_different_color", "change_shape_color", "change_shape_color"],
      ["change_shape_color", "change_shape_color", "change_shape_color"],
      ["pad_right", "fill_holes_different_color", "pad_right"],
      ["pad_right", "change_shape_color", "pad_right"],
      ["fill_holes_different_color", "change_shape_color", "pad_right"],
      ["fill_holes_different_color", "pad_right", "change_shape_color"],
      ["change_shape_color", "pad_right", "fill_holes_different_color"],
      ["change_shape_color", "fill_holes_different_color", "pad_right"]],
    3, 2, "test", 20, 20))

# Exp 3

compositionality_configs.append(make_config(
    [["rot90"], ["pad_top"], ["crop_bottom_side"],
      ["rot90", "rot90"], ["pad_top", "pad_top"], ["crop_bottom_side", "crop_bottom_side"],
      ["rot90", "pad_top"], ["rot90", "crop_bottom_side"],
      ["pad_top", "crop_bottom_side"]],
    3, 3, "train", 20, 20))

compositionality_configs.append(make_config(
    [["rot90", "rot90", "rot90"],
      ["rot90", "rot90", "pad_top"],
      ["rot90", "rot90", "crop_bottom_side"],
      ["rot90", "pad_top", "pad_top"],
      ["rot90", "pad_top", "crop_bottom_side"],
      ["rot90", "crop_bottom_side", "crop_bottom_side"],
      ["pad_top", "pad_top", "pad_top"],
      ["pad_top", "pad_top", "crop_bottom_side"],
      ["pad_top", "crop_bottom_side", "crop_bottom_side"],
      ["crop_bottom_side", "crop_bottom_side", "crop_bottom_side"],
      ["rot90", "pad_top", "rot90"],
      ["rot90", "crop_bottom_side", "rot90"],
      ["pad_top", "crop_bottom_side", "rot90"],
      ["pad_top", "rot90", "crop_bottom_side"],
      ["crop_bottom_side", "rot90", "pad_top"],
      ["crop_bottom_side", "pad_top", "rot90"]],
    3, 3, "test", 20, 20))


# Exp 4

compositionality_configs.append(make_config(
    [["extend_contours_different_color"], ["mirror_horizontal"], ["translate_down"],
      ["extend_contours_different_color", "extend_contours_different_color"],
      ["mirror_horizontal", "mirror_horizontal"],
      ["translate_down", "translate_down"],
      ["extend_contours_different_color", "mirror_horizontal"],
      ["extend_contours_different_color", "translate_down"],
      ["mirror_horizontal", "translate_down"]],
    3, 4, "train", 20, 20))

compositionality_configs.append(make_config(
    [["extend_contours_different_color", "extend_contours_different_color", "extend_contours_different_color"],
      ["extend_contours_different_color", "extend_contours_different_color", "mirror_horizontal"],
      ["extend_contours_different_color", "extend_contours_different_color", "translate_down"],
      ["extend_contours_different_color", "mirror_horizontal", "mirror_horizontal"],
      ["extend_contours_different_color", "mirror_horizontal", "translate_down"],
      ["extend_contours_different_color", "translate_down", "translate_down"],
      ["mirror_horizontal", "mirror_horizontal", "mirror_horizontal"],
      ["mirror_horizontal", "mirror_horizontal", "translate_down"],
      ["mirror_horizontal", "translate_down", "translate_down"],
      ["translate_down", "translate_down", "translate_down"],
      ["extend_contours_different_color", "mirror_horizontal", "extend_contours_different_color"],
      ["extend_contours_different_color", "translate_down", "extend_contours_different_color"],
      ["mirror_horizontal", "translate_down", "extend_contours_different_color"],
      ["mirror_horizontal", "extend_contours_different_color", "translate_down"],
      ["translate_down", "extend_contours_different_color", "mirror_horizontal"],
      ["translate_down", "mirror_horizontal", "extend_contours_different_color"]],
    3, 4, "test", 20, 20))

# Exp 5

compositionality_configs.append(make_config(
    [["extend_contours_same_color"], ["pad_left"], ["mirror_vertical"],
      ["extend_contours_same_color", "extend_contours_same_color"], ["pad_left", "pad_left"], ["mirror_vertical", "mirror_vertical"],
      ["extend_contours_same_color", "pad_left"], ["extend_contours_same_color", "mirror_vertical"],
      ["pad_left", "mirror_vertical"]],
    3, 5, "train", 20, 20))

compositionality_configs.append(make_config(
    [["extend_contours_same_color", "extend_contours_same_color", "extend_contours_same_color"],
      ["extend_contours_same_color", "extend_contours_same_color", "pad_left"],
      ["extend_contours_same_color", "extend_contours_same_color", "mirror_vertical"],
      ["extend_contours_same_color", "pad_left", "pad_left"],
      ["extend_contours_same_color", "pad_left", "mirror_vertical"],
      ["extend_contours_same_color", "mirror_vertical", "mirror_vertical"],
      ["pad_left", "pad_left", "pad_left"],
      ["pad_left", "pad_left", "mirror_vertical"],
      ["pad_left", "mirror_vertical", "mirror_vertical"],
      ["mirror_vertical", "mirror_vertical", "mirror_vertical"],
      ["extend_contours_same_color", "pad_left", "extend_contours_same_color"],
      ["extend_contours_same_color", "mirror_vertical", "extend_contours_same_color"],
      ["pad_left", "mirror_vertical", "extend_contours_same_color"],
      ["pad_left", "extend_contours_same_color", "mirror_vertical"],
      ["mirror_vertical", "extend_contours_same_color", "pad_left"],
      ["mirror_vertical", "pad_left", "extend_contours_same_color"]],
    3, 5, "test", 20, 20))