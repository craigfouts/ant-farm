'''
Author(s): Craig fouts
Correspondence: c.fouts25@imperial.ac.uk
License: Apache 2.0 license
'''

from abc import ABCMeta, abstractmethod
from ipycanvas import hold_canvas
from sklearn.utils import check_random_state
from ._base import RunTime
from ..utils.data import make_grid
from ..utils.sugar import attrmethod

class AntFarm(RunTime, metaclass=ABCMeta):
    @attrmethod
    def __init__(self, n_ants=500, ant_size=4., ant_color='white', farm_color='black', inset=.1, scale=0., wrap=True, seed=None, **kwargs):
        super().__init__(**kwargs)

        self._state = check_random_state(seed)
        self._canvas[0].fill_style = farm_color
        self._canvas[0].fill_rect(0, 0, width=self.width, height=self.height)
        self.x = make_grid(n_ants, self.width, self.height, self.inset, self.scale, self._state)

    def _build(self):        
        if self.wrap:
            self.x %= (self.width, self.height)

    @abstractmethod
    def _step(self):
        pass

    def _draw(self, ant_color=None):
        if ant_color is not None:
            self._canvas[1].fill_style = ant_color
        else:
            self._canvas[1].fill_style = self.ant_color

        with hold_canvas():
            self._canvas[1].clear()
            self._canvas[1].fill_circles(*self.x.T, self.ant_size)
