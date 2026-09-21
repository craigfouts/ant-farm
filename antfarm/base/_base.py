'''
Author(s): Craig fouts
Correspondence: c.fouts25@imperial.ac.uk
License: Apache 2.0 license
'''

from abc import ABCMeta, abstractmethod
from ipycanvas import MultiCanvas
from ipywidgets import Button, FloatSlider
from IPython.display import HTML, display
from threading import Timer
from ..utils import get_kwargs
from ..utils.sugar import attrmethod, buildmethod

class RunTime(metaclass=ABCMeta):
    @attrmethod
    def __init__(self, width=500., height=500., frame_rate=2e-2, step_rate=2.):
        self.shape = (width, height)
        self._canvas = MultiCanvas(2, width=width, height=height)
        self._toggle = Button(description='Start', width=width)
        self._toggle.on_click(self.toggle)
        self._running = False

    @buildmethod
    def __step(self, *args, **kwargs):
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

        # display(HTML('<style> .cell-output-ipywidget-background { background-color: transparent !important;} </style>'))
        display(self._canvas)
        display(self._toggle)
        self._draw()

    def stop(self):
        self._running = False

        if hasattr(self, '_timer'):
            self._timer.cancel()

    def toggle(self, *_):
        if self._running:
            self._toggle.description = 'Start'
            self.stop()
        else:
            self._toggle.description = 'Stop'
            self._running = True
            self.__step()
