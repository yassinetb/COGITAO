from matplotlib import colors

MAX_GRID_SIZE = 100
MIN_GRID_SIZE = 1 
ALLOWED_COLORS = [0,1,2,3,4,5,6,7,8,9]
PADDING = -1

COLORMAP = colors.ListedColormap(
    ['#000000', '#0074D9','#FF4136','#2ECC40','#FFDC00',
    '#AAAAAA', '#F012BE', '#FF851B', '#7FDBFF', '#870C25'])
NORM = colors.Normalize(vmin=0, vmax=9)


class DoesNotFitException(Exception):
    pass

class ShapeOutOfBounds(Exception):
    pass