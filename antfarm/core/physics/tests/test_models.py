"""
Author(s): Craig fouts
License: Apache 2.0 license
"""

import pytest
from .._engine import *
from .._motion import *

@pytest.fixture
def gravity():
    return Gravity()

@pytest.fixture
def nbody():
    return NBody()

@pytest.fixture
def brownian():
    return Brownian()

def test_gravity_step(gravity):
    gravity._step()

def test_nbody_step(nbody):
    nbody._step()

def test_brownian_step(brownian):
    brownian._step()
