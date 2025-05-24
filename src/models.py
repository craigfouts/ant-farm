"""
Craig Fouts (craig.fouts@uu.igp.se)
"""

import matplotlib.pyplot as plt
import numpy as np
import warnings
from tqdm import tqdm
from utilities import grab_plot, VideoWriter

class Farm:
    def __init__(self, n_ants=500, farm_size=500, warn=True):
        self.farm_size = farm_size
        self.warn = warn

        positions = np.random.rand(n_ants, 2)*farm_size
        velocities = 2*np.pi*np.random.rand(n_ants, 1)
        self.ants = np.hstack([positions, velocities])

    def __call__(self, **kwargs):
        if hasattr(self, 'forward'):
            return self.forward(**kwargs)
        
        if self.warn:
            warnings.warn('Forward method not implemented.')

        return self.ants
    
    def plot(self, ant_size=10., ant_color='black', farm_color='white', return_plot=False):
        fig, ax = plt.subplots(1, 1, facecolor=farm_color)
        fig.subplots_adjust(left=.01, right=.99, bottom=.01, top=.99)
        ax.scatter(*self.ants[:, :2].T, ant_size, ant_color)
        ax.axis([0, self.farm_size, 0, self.farm_size])
        ax.set_axis_off()

        if return_plot:
            return fig, ax

    def record(self, n_steps=500, path='ant_farm.mp4', show=False, verbosity=1, plot_kwargs={}, **kwargs):
        description = path.split('/')[-1].split('.')[0]
        video = VideoWriter(self.farm_size, path=path)
        
        for _ in tqdm(range(n_steps), desc=description) if verbosity > 0 else range(n_steps):
            self.plot(**plot_kwargs)
            video.write(grab_plot())
            self(**kwargs)

        if show:
            video.show()
    
class Brownian(Farm):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def forward(self, rate=5., variance=.5):
        self.ants[:, -1:] += np.random.normal(0, variance, self.ants[:, -1:].shape)
        update = np.hstack([np.cos(self.ants[:, -1:]), np.sin(self.ants[:, -1:])])
        self.ants[:, :2] = (self.ants[:, :2] + update*rate)%self.farm_size

        return self.ants
    
class Vicsek(Farm):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def forward(self, rate=5., variance=.1, radius=10):
        neighborhood = np.sqrt(np.square(self.ants[:, None] - self.ants[None, :])).sum(-1) < radius
        deviation = np.random.normal(0, variance, self.ants[:, -1:].shape)
        self.ants[:, -1:] = (neighborhood@self.ants[:, -1:])/neighborhood.sum(-1)[:, None] + deviation
        update = np.hstack([np.cos(self.ants[:, -1:]), np.sin(self.ants[:, -1:])])
        self.ants[:, :2] = (self.ants[:, :2] + update*rate)%self.farm_size

        return self.ants
    