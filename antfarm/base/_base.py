'''
Author(s): Craig fouts
Correspondence: c.fouts25@imperial.ac.uk
License: Apache 2.0 license
'''

from abc import ABCMeta, abstractmethod
from threading import Timer
from ._canvas import Canvas
from ..utils import get_kwargs
from ..utils.sugar import attrmethod, buildmethod

class RunTime(metaclass=ABCMeta):
    @attrmethod
    def __init__(self, frame_rate=2e-2, step_rate=2., **kwargs):
        self._canvas = Canvas(**kwargs)
        self._canvas.toggle.on_click(self.toggle)
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

    def start(self):
        if self._running:
            self.stop()

        self._canvas.show()
        self._draw()

    def stop(self):
        self._running = False

        if hasattr(self, '_timer'):
            self._timer.cancel()

    def toggle(self, *_):
        if self._running:
            self._canvas.toggle.icon = 'play'
            self.stop()
        else:
            self._canvas.toggle.icon = 'pause'
            self._running = True
            self.__step()

    def reset(self, *_):
        pass
