'''
Author(s): Craig fouts
Correspondence: c.fouts25@imperial.ac.uk
License: Apache 2.0 license
'''

from abc import ABCMeta, abstractmethod
from copy import deepcopy
from sklearn.utils import check_random_state
from threading import Timer
from ._canvas import Canvas
from ..utils import get_kwargs
from ..utils.sugar import attrmethod, buildmethod

class RunTime(metaclass=ABCMeta):
    @attrmethod
    def __init__(self, frame_rate=2e-2, step_rate=2., seed=None, **kwargs):
        self._state = check_random_state(seed)
        self._canvas = Canvas(**kwargs)
        self._canvas.toggle.on_click(self.toggle)
        self._canvas.reset.on_click(self.reset)
        self._running = False

    @buildmethod
    def __step(self, *args, **kwargs):
        if self._running:
            step_kwargs, draw_kwargs = get_kwargs(self._step, self._draw, *args, **kwargs)
            self._step(**step_kwargs)
            self._draw(**draw_kwargs)
            self._timer = Timer(self.frame_rate, self.__step, args=args, kwargs=kwargs)
            self._timer.start()

    @abstractmethod
    def _step(self):
        pass

    @abstractmethod
    def _draw(self):
        pass

    def copy(self, state=None):
        if state is None:
            state = self.__dict__

        copy = {k: deepcopy(v) for k, v in state.items() if type(v) != Canvas}
        copy['_canvas'] = self._canvas

        return copy

    def start(self):
        self._init = self.copy()

        if self._running:
            self.stop()

        self._canvas.show()
        self._draw()

    def stop(self):
        self._running = False
        self._canvas.toggle.icon = 'play'

        if hasattr(self, '_timer'):
            self._timer.cancel()

    def toggle(self, *_):
        if self._running:
            self.stop()
        else:
            self._canvas.toggle.icon = 'pause'
            self._running = True
            self.__step()

    def reset(self, *_):
        self.stop()

        if hasattr(self, '_init'):
            init = self.copy(self._init)
            self.__dict__ = self.copy(self._init)
            self._init = init
            self._draw()
