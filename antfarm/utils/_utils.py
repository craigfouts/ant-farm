'''
Author(s): Craig Fouts
Correspondence: c.fouts25@imperial.ac.uk
License: Apache 2.0 license
'''

import re
from inspect import signature

def get_methods(cls, prefix='', suffix='', return_callable=False):
    methods = []

    for attr in dir(cls):
        if callable(method := getattr(cls, attr)) and re.search(f'^{prefix}.*{suffix}$', attr):
            methods.append(method if return_callable else attr)

    return methods

def has_method(cls, method):
    methods = get_methods(cls)

    return method in methods

def get_kwargs(*functions, **kwargs):
    function_kwargs = []

    for f in functions:
        keys = signature(f).parameters.keys()
        function_kwargs.append({k: kwargs[k] for k in keys if k in kwargs})

    if len(function_kwargs) == 1:
        return function_kwargs[0]
    return function_kwargs
