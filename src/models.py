import numpy as np

class Farm:
    def __init__(self, velocity=3., variance=.3, proximity=20., canvas_size=500):
        self.velocity = velocity
        self.variance = variance
        self.proximity = proximity
        self.canvas_size = canvas_size

    def __call__(self, x, v):
        return x, v

class RandomFarm(Farm):
    def __call__(self, x, v):
        v += np.random.normal(0, self.variance, size=v.shape)
        alignment = np.hstack([np.cos(v), np.sin(v)])
        x = (x + self.velocity*alignment)%self.canvas_size

        return x, v
    
class VicsekFarm(Farm):
    def __call__(self, x, v):
        neighborhood = np.sqrt(np.square(x[:, None] - x[None, :])).sum(-1) < self.proximity
        uncertainty = np.random.normal(0, self.variance, size=v.shape)
        v = (neighborhood@v)/neighborhood.sum(-1)[:, None] + uncertainty
        alignment = np.hstack([np.cos(v), np.sin(v)])
        x = (x + self.velocity*alignment)%self.canvas_size

        return x, v
    