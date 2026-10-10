"""
Author(s): Craig fouts
Correspondence: foutscw@gmail.com
License: Apache 2.0 license
"""

import pytest
# from .._branch import *
from .._matter import *

@pytest.fixture
def vicsek():
    return Vicsek()

def test_vicsek_step(vicsek):
    vicsek._step()
