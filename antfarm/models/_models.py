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

        self.V_ = 2.*np.pi*self._seed.random((self.n_ants, 1))

    def _step(self):
        self.V_ += self._seed.normal(0., self.drift_scale**2, self.V_.shape)
        update = np.concat((np.cos(self.V_), np.sin(self.V_)), -1)
        self.X_ += self.step_rate*update

        if self.wrap:
            self.X_ = self.X_%self.farm_size

        return self.X_, self.V_
    
class Vicsek(Colony):
    @attrmethod
    def __init__(self, *args, drift_scale=.1, hood_size=10., **kwargs):
        super().__init__(*args, **kwargs)

        self.V_ = 2.*np.pi*self._seed.random((self.n_ants, 1))

    def _step(self):
        hood = cdist(self.X_, self.X_) < self.hood_size
        drift = self._seed.normal(0., self.drift_scale**2, self.V_.shape)
        self.V_ = (hood@self.V_)/hood.sum(-1)[:, None] + drift
        update = np.concat((np.cos(self.V_), np.sin(self.V_)), -1)
        self.X_ += self.step_rate*update

        if self.wrap:
            self.X_ = self.X_%self.farm_size

        return self.X_, self.V_

class Gravity(Colony):
    @attrmethod
    def __init__(self, n_ants=100, drift_scale=2., gravity=.1, friction=.1, **kwargs):
        super().__init__(n_ants, **kwargs)

        self.V_ = self._seed.normal(0., drift_scale, self.X_.shape)
        self.A_[:, 1] = gravity

    def _check_borders(self, axes=(0, 1)):
        for ax in axes:
            lower_mask = (x := self.X_[:, ax]) < self.ant_size
            upper_mask = x > self.farm_size - self.ant_size
            mask = np.logical_or(lower_mask, upper_mask)
            self.V_[mask, 0] *= (2*ax - 1)*(1. - self.friction)
            self.V_[mask, 1] *= (1 - 2*ax)*(1. - self.friction)
            self.X_[lower_mask, ax] = self.ant_size
            self.X_[upper_mask, ax] = self.farm_size - self.ant_size

    def _step(self):
        self.V_ += self.A_*self.step_rate
        self.X_ += self.V_*self.step_rate + .5*self.A_*self.step_rate**2
        self._check_borders()
