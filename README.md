## Install dependencies 

We use [poetry](https://python-poetry.org/) as our dependency manager and build
system framework. Please install it using:
```shell
$ pip install poetry
```
and install the dependencies by running:
```shell
$ poetry update
```

Install the library in editable mode so that changes in the codebase
can be tested easily.

```shell
$ pip install -e .
```

## Run code 

Use of our generator is demonstrated in the `demo.ipynb` jupyter notebook. 

<!-- 

### To mention: 

- [ ] What the point cloud and shape classes are for
- [ ] How does generating shapes work, and why it's the first step to using the generator
- [ ] How one should pre-compute conditionals for shapes 

# Installation 

# Demos 

# Algorithm 

# Shapes 

# Transforms 

# Conditionals 

# Before-ARC Dataset 

# Cite 

The generator relies on pre-created set of shapes stored in a dedicated .h5py file. Furthermore, the conditionals for the shapes are 
also pre-computed. This simplifies the generation process as generation shapes on the fly based on conditionals can be complex. 

For simplicity, you can use our lightweight precomputed set of shapes with precomputed conditionals "arcworld/datasets/shapes.h5py".

For extended use:

* If you'd like to extend the set of shapes, you can run the "shapes.py" file in the shapes folder, which in the published form maximizes 
diversity of generated shapes patterns. You can extend the number of shapes by modifying the "k_obj_per_config" variable in the "generate_shapes.py file. This will create N different shapes per configuration, as opposed to just one in the demo format. You can specify the file name on the hdf5_utils.py file. 

* If you'd like to add conditionals to the generator, you should simply re-run the "compute_conditions.py" script in the shapes folder. You can re compute the entirety of the conditionals, or simply compute the conditional for your new conditional of interest. 


# Instruction on configuration of the generator: 

## Number of Shapes: x  

Constraints for shapes should be considered in relation to the grid size, and the maximum shape size wanted by the user. For instance, if the maximum shape dimension is 6x6, and the grid size is 10x10, the generator will be forced to randomly sample shapes smaller than 6x6 if it wants them to fit more than one shape into the 10x10 grid. 

## Grid Size

As mentionned above, this should be considered in relation to the number of shapes, as well as to the number of transformations. We recommend having a minimum grid size of 10, as below this grid size, the capabilities of the generator starts to be come difficult to utilize (although it works). 

## Number of Examples

This is the number of examples to return for a given sample transform suite, and is the number of input-output pairs grids return from the `generate_single_task()` function. We always return a dict with two keys: `pairs` and `transformations`. `pairs` is the list of input-output pairs, and  `transformations` is the sampled transformations for this set of pairs. 

## Allowed Combinations, Allowed Transformations and Max Transformation Depth 

Either `allowed_combinations` OR `allowed_transformations` should be specified, not both. If `allowed_combinations` is specified, the generator will randomly sample from the provided list of possible combinations to sample from. If however `allowed_combinations` is set to `None`, and a list is provided for `allowed_transformations`, then the generator will randomly compose transformations, with a depth comprised between `min_transform_depth` and `max_transform_depth` (which must be provided as ints). 

Note: the `min_transformation_depth` and `max_transformation_depth` must also be considered in relation to the grid size and number of objects. 

All transformations (either within `allowed_combinations` or `allowed_transformations`) must be defined in the `transforms.py`. 

## Shape Compulsory Conditionals. 

List of "conditionals" that the shapes must satisfy. Shape constraints would probably have been a better name. Can be empty if all shapes can be sampled from the shape list. 
These must be as defined in `conditionals.py`. 

## Summary of Config Constraints. 

Must be passed to the generator as a dict, similarly to demonstrated in the demo.ipynb. 
The validity of the config is verified entirely in the `Config` class, as implemented in the `config_validation.py` script. 

* `min_n_shapes_per_grid` should be `int` >=1 
* `max_n_shapes_per_grid` should be `int` >= 1 and >= `min_n_shapes_per_grid`

* `min_n_transformations` should be `int` >=1 
* `max_n_transformations` should be `int` >= 1 and >= `min_n_transformations_per_grid`

* `min_grid_size` should be `int` >= 1
* `max_grid_size` should be `int` >= 1 and >= `min_grid_size`
  
* `n_examples` should be `int` and >= 1
  
* `allowed_combinations` should be `list of list` OR `None`. 
* `allowed_transformations` should be `list` or `None`.
  * If `allowed_transformations` is provided, the user must also set 
    * `min_transformation_depth` as `int` >= 1
    * `max_transformation_depth` as `int` >= 1 and >= `max_transformation_depth` 
  * Elif `allowed_transformations` is None - `min_transformations_depth` and `max_transformations` should also be set to None. 
  
* `shape_compulsory_conditionals` should be `list`. Could be empty list if no constraints are required. 

# To-Do 

- [ ] Update README
- [ ] Find sustainable way to not push the big Shapes file onto GH. 
- [x] Extend the experiments 
- [x] STILL TO CHECK: Check for duplicate bug
- [x] Fix bug with round numbers for Klim
- [ ] Add Metadata to all of the subfolders and upload to the README.
- [x] Debug Rotation and some other transformations which seem to be buggy. Especially on large objects. Check the paper_plot.ipynb (Plot Tasks section) to see what I'm talking about 
- [x] Debug Shape Emptying
- [x] Add transformations.
- [x] Change the names to match Klim's and generate in distribution test set. 
- [x] Upload to HF datasets.
- [x] Complete demo.ipynb
- [x] Fix code to not allow shapes to be neighbours! 
- [ ] Improve Figures with new transformations
- [ ] Add function (and experimental setting) where we vary the background of the grid. 
- [ ] Fix Bug for the image dimensions of the .parquet files 
- [ ] The compatible vs non compatible shape constraints in the beginning of `generate_single_task` function
- [ ] Verify that `shape_compulsory_conditionals`, `allowed_combinations` and `allowed_transformations` are within what the relevant files allow for.  
- [ ] Write a demo file to show how to play with the shapes  -->