import random

import numpy as np

from arcworld.shapes.random_shape import RandomShapeParams, RandomShape
from arcworld.general_utils import plot_grid
from arcworld.general_utils import randomly_add_shape_to_world

RandomShapeParams.allowed_color_pattern = {'uniform': 1, 'top_bot': 2, 'left_right': 2,
                             'col_stripes': 2,
                             'row_stripes': 2}
RandomShapeParams.allowed_connectivity = ['4connected', '8connected']
RandomShapeParams.allowed_max_size = 8
RandomShapeParams.allowed_symmetry = ['horizontal', 'vertical', 'diag_tl_br', 'diag_bl_tr', 'point']

main_grid = np.zeros((30,30))
for i in range(7):
    shape = RandomShape()
    main_grid, shape = randomly_add_shape_to_world(main_grid, shape)

fig = plot_grid(main_grid)
fig.show()

#instance segmentaton
#visual transformer