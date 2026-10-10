"""
Author(s): Craig fouts
Correspondence: foutscw@gmail.com
License: Apache 2.0 license
"""

import numpy as np
from ...base import AntFarm
from ...utils.sugar import attrmethod

class NBody(AntFarm):
    @attrmethod
    def __init__(self, n_ants=100, size=8., mass=1e3, dt=.1, **kwargs):
        super().__init__(n_ants, size, dt=dt, **kwargs)

        self.v = np.zeros((n_ants, 2))
        self.m = mass*np.ones(n_ants)
        self._eye = np.eye(n_ants)

    def _step(self):
        dx = (x := self.x + self.dt*self.v) - x[:, None]
        r = (r2 := np.square(dx).sum(-1)**(3./2.) + self._eye)**(1./3.)
        a, mask = self.m@(dx/r2[..., None]), (r <= 2.*self.size) - self._eye
        a += self.m[:, None]*(mask[..., None]*dx/r[..., None]**2.).sum(0)
        self.v += self.dt*a/2.
        self.x += self.dt*self.v

class Gravity(AntFarm):
    @attrmethod
    def __init__(self, n_ants=50, size=16., mass=1e2, gravity=2., friction=.1, dt=.1, **kwargs):
        super().__init__(n_ants, size, dt=dt, **kwargs)

        self.v = np.zeros((n_ants, 2))
        self.a = np.zeros((n_ants, 2))
        self.a = gravity*np.tile(np.arange(2), (n_ants, 1))
        self.m = mass*np.ones(n_ants)
        self._eye = np.eye(n_ants, dtype=np.int32)

    def _check_walls(self):
        for ax in (0, 1):
            lower = (x := self.x[:, ax]) < self.size
            upper = x > (wall := self._canvas.shape[ax] - self.size)
            self.v[lower | upper, ax] *= -1.*(1. - self.friction)
            self.x[lower, ax], self.x[upper, ax] = self.size, wall

    def _step(self):
        dx = (x := self.x + self.dt*self.v) - x[:, None]
        r = (np.square(dx).sum(-1)**(3./2.) + self._eye)**(1./3.)
        mask = (r <= 2*self.size) - self._eye
        a = self.a + self.m[:, None]*(mask[..., None]*dx/r[..., None]).sum(0)
        self.v += self.dt*a/2.
        self.x += self.dt*self.v
        self._check_walls()
