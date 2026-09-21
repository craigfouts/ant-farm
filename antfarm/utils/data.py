import numpy as np
from sklearn.utils import check_random_state

def make_grid(n_pts=100, width=500., height=500., inset=.1, scale=0., seed=None):
    n_cols = np.ceil(np.sqrt(n_pts)).astype(int)
    n_rows = np.ceil(n_pts/n_cols).astype(int)
    x_inset, y_inset = inset*width, inset*height
    x_coords = np.linspace(x_inset, width - x_inset, n_cols)
    y_coords = np.linspace(y_inset, height - y_inset, n_rows)
    x, y = np.meshgrid(x_coords, y_coords)
    data = np.concat((x.ravel()[:, None], y.ravel()[:, None]), 1)[:n_pts]

    if scale > 0.:
        state = check_random_state(seed)
        data += state.normal(0., scale, data.shape)

    return data
