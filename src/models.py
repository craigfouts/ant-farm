import numpy as np

class Vicsek:
    def __init__(self, proximity=20., velocity=3., update_rate=1., variance=.3, canvas_size=500):
        self.proximity = proximity
        self.velocity = velocity
        self.update_rate = update_rate
        self.variance = variance
        self.canvas_size = canvas_size

    def __call__(self, x, v):
        neighborhood = np.sqrt(np.square(x[:, None] - x[None, :])).sum(-1) < self.proximity
        uncertainty = np.random.normal(0, self.variance, size=v.shape)
        v = (neighborhood@v)/neighborhood.sum(-1)[:, None] + uncertainty
        alignment = np.hstack([np.cos(v), np.sin(v)])
        x = (x + self.velocity*self.update_rate*alignment)%(self.canvas_size)
        return x, v
    