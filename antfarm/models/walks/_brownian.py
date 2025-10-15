'''
Author(s): Craig Fouts
Correspondence: c.fouts25@imperial.ac.uk
License: Apache 2.0 license
'''

import numpy as np
from ...base import Colony

class Brownian(Colony):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _step(self, step_rate=5., step_scale=.5):
        self.V_ += self._seed.normal(0, step_scale**2, self.V_.shape)
        update = np.concat((np.cos(self.V_), np.sin(self.V_)), -1)
        self.X_ += step_rate*update

        if self.wrap:
            self.X_ = self.X_%self.farm_size

        return self.X_, self.V_
