from typing import List, Optional, Union
from pydantic import BaseModel, Field, model_validator, field_validator

class ConfigValidator(BaseModel):
    min_n_shapes_per_grid: int = Field(..., ge=1)
    max_n_shapes_per_grid: int = Field(..., ge=1)

    min_grid_size: int = Field(..., ge=1)
    max_grid_size: int = Field(..., ge=1)

    n_examples: int = Field(..., ge=1)

    allowed_transformations: Optional[List[str]] = None
    allowed_combinations: Optional[List[List[str]]] = None

    min_transformation_depth: Optional[int] = None
    max_transformation_depth: Optional[int] = None

    shape_compulsory_conditionals: List[str]

    @field_validator("allowed_transformations")
    def validate_allowed_transformations(cls, v):
        if v is not None and len(v) == 0:
            raise ValueError("allowed_transformations must be a non-empty list or None")
        return v

    @field_validator("allowed_combinations")
    def validate_allowed_combinations(cls, v):
        if v is not None and len(v) == 0:
            raise ValueError("allowed_combinations must be a non-empty list of lists or None")
        return v
    
    @model_validator(mode='after')
    def check_constraints(cls, values):
        min_shapes = values.min_n_shapes_per_grid
        max_shapes = values.max_n_shapes_per_grid
        if max_shapes < min_shapes:
            raise ValueError("max_n_shapes_per_grid must be >= min_n_shapes_per_grid")

        min_grid = values.min_grid_size
        max_grid = values.max_grid_size
        if max_grid < min_grid:
            raise ValueError("max_grid_size must be >= min_grid_size")

        allowed_trans = values.allowed_transformations
        allowed_combs = values.allowed_combinations

        # Check that exactly one of allowed_transformations or allowed_combinations is provided
        if (allowed_trans is None and allowed_combs is None) or (allowed_trans is not None and allowed_combs is not None):
            raise ValueError("Exactly one of allowed_combinations or allowed_transformations must be provided (not both or neither).")

        min_depth = values.min_transformation_depth
        max_depth = values.max_transformation_depth

        if allowed_trans is not None:
            if min_depth is None or max_depth is None:
                raise ValueError("When allowed_transformations is provided, min_transformation_depth and max_transformation_depth must also be set")
            if min_depth < 1 or max_depth < 1:
                raise ValueError("min_transformation_depth and max_transformation_depth must be >= 1")
            if max_depth < min_depth:
                raise ValueError("max_transformation_depth must be >= min_transformation_depth")
        else:
            if min_depth is not None or max_depth is not None:
                raise ValueError("min_transformation_depth and max_transformation_depth must be set to None when allowed_transformations is None")

        return values