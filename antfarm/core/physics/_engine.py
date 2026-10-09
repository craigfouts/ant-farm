'''
Author(s): Craig fouts
Correspondence: c.fouts25@imperial.ac.uk
License: Apache 2.0 license
'''

import numpy as np
from ...base import AntFarm
from ...utils.sugar import attrmethod

class NBody(AntFarm):
    @attrmethod
    def __init__(self, n_ants=100, ant_size=8., ant_mass=1e3, step_rate=.1, **kwargs):
        super().__init__(n_ants, ant_size, step_rate=step_rate, **kwargs)

        self.v = np.zeros((n_ants, 2))
        self.m = ant_mass*np.ones(n_ants)
        self._eye = np.eye(n_ants)

    def _step(self):
        dx = (x := self.x + self.step_rate*self.v) - x[:, None]
        r = (r2 := np.square(dx).sum(-1)**(3./2.) + self._eye)**(1./3.)
        a, mask = self.m@(dx/r2[..., None]), (r <= 2.*self.ant_size) - self._eye
        a += self.m[:, None]*(mask[..., None]*dx/r[..., None]**2.).sum(0)
        self.v += self.step_rate*a/2.
        self.x += self.step_rate*self.v

class Gravity(AntFarm):
    @attrmethod
    def __init__(self, n_ants=50, ant_size=16., ant_mass=1e2, gravity=2., friction=.1, step_rate=.1, **kwargs):
        super().__init__(n_ants, ant_size, step_rate=step_rate, **kwargs)

        self.v = np.zeros((n_ants, 2))
        self.a = np.zeros((n_ants, 2))
        self.a[:, 1] = gravity
        self.m = ant_mass*np.ones(n_ants)
        self._eye = np.eye(n_ants, dtype=np.int32)

    def _check_walls(self):
        for ax in (0, 1):
            lower = (x := self.x[:, ax]) < self.ant_size
            upper = x > (wall := self._canvas.shape[ax] - self.ant_size)
            self.v[lower | upper, ax] *= -1.*(1. - self.friction)
            self.x[lower, ax], self.x[upper, ax] = self.ant_size, wall

    def _step(self):
        dx = (x := self.x + self.step_rate*self.v) - x[:, None]
        r = (np.square(dx).sum(-1)**(3./2.) + self._eye)**(1./3.)
        mask = (r <= 2*self.ant_size) - self._eye
        a = self.a + self.m[:, None]*(mask[..., None]*dx/r[..., None]).sum(0)
        self.v += self.step_rate*a/2.
        self.x += self.step_rate*self.v
        self._check_walls()
