'''
Author(s): Craig fouts
Correspondence: c.fouts25@imperial.ac.uk
License: Apache 2.0 license
'''

import matplotlib.pyplot as plt
from abc import ABCMeta, abstractmethod
from ipycanvas import hold_canvas
from tqdm import tqdm
from ._base import RunTime
from ._video import VideoWriter
from ..utils.data import make_grid
from ..utils.plots import grab_plot
from ..utils.sugar import attrmethod

class AntFarm(RunTime, metaclass=ABCMeta):
    @attrmethod
    def __init__(self, n_ants=500, size=4., style='white', inset=.1, scale=6., wrap=True, **kwargs):
        super().__init__(**kwargs)

        self.x = make_grid(n_ants, *self._canvas.shape, inset, scale, self._state)

    def _build(self):        
        if self.wrap:
            self.x %= self._canvas.shape

    @abstractmethod
    def _step(self):
        pass

    def _draw(self):
        self._canvas[1].fill_style = self.style

        with hold_canvas():
            self._canvas[1].clear()
            self._canvas[1].fill_circles(*self.x.T, self.size)

    def plot(self, return_plot=False):
        fig, ax = plt.subplots(1, 1, facecolor=self._canvas.color)
        fig.subplots_adjust(left=0.0, right=1.0, bottom=0.0, top=1.0)
        ax.axis([0, self._canvas.width, 0, self._canvas.height])
        ax.yaxis.set_inverted(True)
        ax.set_axis_off()
        ax.scatter(*self.x.T, 2.*self.size**2., self.style)

        if return_plot:
            return fig, ax

    def record(self, n_steps=500, fps=30., path=None, show=False, verbose=True, **kwargs):
        if path is None:
            path = self.__class__.__name__.lower() + '.mp4'

        vid = VideoWriter(*self._canvas.shape, fps, path)

        for _ in tqdm(range(n_steps), desc=path) if verbose else range(n_steps):
            self.plot()
            vid.write(grab_plot())
            self._step(**kwargs)

        if show:
            vid.show()
