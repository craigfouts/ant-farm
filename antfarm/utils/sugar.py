'''
Author(s): Craig Fouts
Correspondence: c.fouts25@imperial.ac.uk
License: Apache 2.0 license
'''

from functools import singledispatch, wraps
from inspect import getcallargs

@singledispatch
def attrmethod(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        method_kwargs = dict(getcallargs(method, self, *args, **kwargs))
        del method_kwargs['self']

        for key, val in method_kwargs.items():
            setattr(self, key, val)

        return method(self, *args, **kwargs)
    return wrapper

@attrmethod.register(str)
def _(prefix):
    def decorator(method):
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            method_kwargs = dict(getcallargs(method, self, *args, **kwargs))
            del method_kwargs['self']

            for key, val in method_kwargs.items():
                setattr(self, prefix + key, val)

            return method(self, *args, **kwargs)
        return wrapper
    return decorator
