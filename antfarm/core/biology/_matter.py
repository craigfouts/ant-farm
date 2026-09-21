'''
Author(s): Craig fouts
Correspondence: c.fouts25@imperial.ac.uk
License: Apache 2.0 license
'''

import numpy as np
from scipy.spatial.distance import cdist
from ...base import AntFarm
from ...utils.sugar import attrmethod

class Vicsek(AntFarm):
    @attrmethod
    def __init__(self, n_ants=100, drift=.5, hood=10., **kwargs):
        super().__init__(n_ants, **kwargs)

        self.v = 2.*np.pi*self._state.uniform(size=(n_ants, 1))

    def _step(self):
        edges = cdist(self.x, self.x) < self.hood
        drift = self._state.normal(0., self.drift**2, self.v.shape)
        self.v = (edges@self.v)/edges.sum(1)[:, None] + drift
        update = np.concat((np.cos(self.v), np.sin(self.v)), 1)
        self.x += self.step_rate*update
