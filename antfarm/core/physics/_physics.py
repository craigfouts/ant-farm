'''
Author(s): Craig fouts
Correspondence: c.fouts25@imperial.ac.uk
License: Apache 2.0 license
'''

import numpy as np
from ...base import AntFarm
from ...utils.sugar import attrmethod

class Brownian(AntFarm):
    @attrmethod
    def __init__(self, n_ants=100, drift=.5, **kwargs):
        super().__init__(n_ants, **kwargs)
    
        self.v = 2.*np.pi*self._state.uniform(size=(n_ants, 1))

    def _step(self):
        self.v += self._state.normal(0., self.drift**2, self.v.shape)
        update = np.concat((np.cos(self.v), np.sin(self.v)), 1)
        self.x += self.step_rate*update

class Gravity(AntFarm):
    @attrmethod
    def __init__(self, n_ants=100, drift=.5, gravity=.1, friction=.1, **kwargs):
        super().__init__(n_ants, **kwargs)

        self.v = self._state.uniform(size=(n_ants, 2))
        self.a = np.zeros((n_ants, 2))
        self.a[:, 1] = gravity

    def _check_walls(self):
        for ax in (0, 1):
            lower = (x := self.x[:, ax]) < self.ant_size
            upper = x > (wall := self.shape[ax] - self.ant_size)
            self.v[lower | upper, ax] *= -1.*(1. - self.friction)
            self.x[lower, ax], self.x[upper, ax] = self.ant_size, wall

    def _check_edges(self):
        pass

    def _step(self):
        self.v += self.step_rate*self.a
        self.x += self.step_rate*self.v + (self.step_rate**2)*self.a/2
        self._check_walls()
        self._check_edges()
