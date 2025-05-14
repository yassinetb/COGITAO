import os
import h5py

current_path = os.getcwd()

SHAPE_DATASET_PATH = os.path.join(current_path, '../before-arc/arcworld', 'datasets', 'shapes.h5')

def load_h5(f, filename):
    return f[filename][()]

def load_shape(idx, f=None):
    if not f:
        with h5py.File(SHAPE_DATASET_PATH) as f:
            return load_h5(f, f'shapes/{idx}')
    return load_h5(f, f'shapes/{idx}')

def save_h5(data, filename, f, dtype='i8'):
    try:
        del f[filename]
    except KeyError:
        pass
    f.create_dataset(filename, data=data, dtype=dtype)

def save_shape(data, idx, f = None):
    if not f:
        with h5py.File(SHAPE_DATASET_PATH, 'a') as f:
            save_h5(data, f'shapes/{idx}', f)
            return
    save_h5(data, f'shapes/{idx}', f)

def save_conditions(data, colnames):
    with h5py.File(SHAPE_DATASET_PATH, 'a') as f:
        save_h5(colnames, 'condition_names', f, dtype=None)
        save_h5(data, 'conditions', f)

def load_conditions():
    with h5py.File(SHAPE_DATASET_PATH) as f:
        names = [str(x, 'utf-8') for x in load_h5(f, 'condition_names')]
        return load_h5(f, 'conditions'), names

def get_nr_of_shapes():
    with h5py.File(SHAPE_DATASET_PATH) as f:
        num_shapes = len(f['shapes'].keys())
    return num_shapes



