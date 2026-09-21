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
