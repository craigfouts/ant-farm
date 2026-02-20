'''
Author(s): Craig Fouts
Correspondence: c.fouts25@imperial.ac.uk
License: Apache 2.0 license
'''

import numpy as np
from scipy.spatial.distance import cdist
from ..core import Colony
from ..utils.sugar import attrmethod

class Brownian(Colony):
    @attrmethod
    def __init__(self, *args, drift_scale=.5, **kwargs):
        super().__init__(*args, **kwargs)

    def _step(self):
        self.V_ += self._seed.normal(0, self.drift_scale**2, self.V_.shape)
        update = np.concat((np.cos(self.V_), np.sin(self.V_)), -1)
        self.X_ += self.step_rate*update

        if self.wrap:
            self.X_ = self.X_%self.farm_size

        return self.X_, self.V_
    
class Vicsek(Colony):
    def __init__(self, *args, drift_scale=.1, hood_size=10., **kwargs):
        super().__init__(*args, **kwargs)

    def _step(self):
        hood = cdist(self.X_, self.X_) < self.hood_size
        drift = self._seed.normal(0, self.drift_scale**2, self.V_.shape)
        self.V_ = (hood@self.V_)/hood.sum(-1)[:, None] + drift
        update = np.concat((np.cos(self.V_), np.sin(self.V_)), -1)
        self.X_ += self.step_rate*update

        if self.wrap:
            self.X_ = self.X_%self.farm_size

        return self.X_, self.V_

class Gravity(Colony):
    @attrmethod
    def __init__(self):
        pass
