'''
Author(s): Craig Fouts
Correspondence: c.fouts25@imperial.ac.uk
License: Apache 2.0 license
'''

import numpy as np
import torch
import re
from functools import singledispatch
from inspect import signature
from scipy.spatial.distance import cdist

def get_methods(cls, prefix='', suffix='', return_callable=False):
    methods = []

    for attr in dir(cls):
        if callable(method := getattr(cls, attr)) and re.search(f'^{prefix}.*{suffix}$', attr):
            methods.append(method if return_callable else attr)

    return methods

def get_kwargs(*functions, **kwargs):
    function_kwargs = []

    for f in functions:
        keys = signature(f).parameters.keys()
        function_kwargs.append({k: kwargs[k] for k in keys if k in kwargs})

    if len(function_kwargs) == 1:
        return function_kwargs[0]
    return function_kwargs

@singledispatch
def knn(x, k=1, loop=True):
    adj = cdist(x, x).argsort(-1)
    idx = (adj[:, :k] if loop else adj[:, 1:k + 1]).flatten()
    edges = np.vstack((np.arange(x.shape[0]).repeat(k), idx))

    return edges

@knn.register(torch.Tensor)
def _(x, k=1, loop=True):
    adj = torch.cdist(x, x).argsort(-1)
    idx = (adj[:, :k] if loop else adj[:, 1:k + 1]).flatten()
    edges = torch.vstack((torch.arange(x.shape[0]).repeat_interleave(k), idx))

    return edges
