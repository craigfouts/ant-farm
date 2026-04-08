'''
Author(s): Craig Fouts
Correspondence: c.fouts25@imperial.ac.uk
License: Apache 2.0 license
'''

import numpy as np
import torch
from functools import singledispatch
from scipy.spatial.distance import cdist

__all__ = [
    'knn'
]

@singledispatch
def knn(X, k=1, loop=True):
    adj = cdist(X, X).argsort(-1)
    idx = (adj[:, :k] if loop else adj[:, 1:k + 1]).flatten()
    edges = np.vstack((np.arange(len(X)).repeat(k), idx))

    return edges

@knn.register(torch.Tensor)
def _(X, k=1, loop=True):
    adj = torch.cdist(X, X).argsort(-1)
    idx = (adj[:, :k] if loop else adj[:, 1:k + 1]).flatten()
    edges = torch.vstack((torch.arange(len(X)).repeat_interleave(k), idx))

    return edges
