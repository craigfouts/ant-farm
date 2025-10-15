'''
Author(s): Craig Fouts
Correspondence: c.fouts25@imperial.ac.uk
License: Apache 2.0 license
'''

from ipycanvas import hold_canvas, Canvas
from IPython.display import display
from threading import Timer
from .._utils import attrmethod
from ...base import Farm

class AntFarm(Farm):
    @attrmethod
    def __init__(self, colony, *, step_rate=.02, farm_color='black', ant_color='white', ant_size=3.):
        super().__init__(colony.farm_size)

    def _draw(self):
        with hold_canvas():
            self._canvas.clear()
            self._canvas.fill_style = self.farm_color
            self._canvas.fill_rect(0, 0, width=self.farm_size, height=self.farm_size)
            self._canvas.fill_style = self.ant_color
            self._canvas.fill_circles(*self.colony.X_.T, self.ant_size)

    def _step(self):  # TODO: add colony _step parameters
        self.colony()
        self._draw()
        Farm.timer = Timer(self.step_rate, self._step)
        Farm.timer.start()
