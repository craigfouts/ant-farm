'''
Author(s): Craig fouts
Correspondence: c.fouts25@imperial.ac.uk
License: Apache 2.0 license
'''

from ipycanvas import MultiCanvas
from IPython.display import display
from ipywidgets import Button, HBox, Layout, VBox
from ..utils.plots import set_background
from ..utils.sugar import attrmethod

class Canvas(MultiCanvas):
    @attrmethod
    def __init__(self, width=500., height=500., color='black'):
        super().__init__(2, width=width, height=height)

        self.set_color(color)
        self.shape = (width, height)
        self.toggle = Button(icon='play', layout=Layout(width=f'{width/2.}px'))
        self.reset = Button(icon='rotate-left', layout=self.toggle.layout)
        self.io = HBox((self.toggle, self.reset), layout=Layout(justify_content='center'))
        self.body = VBox((self, self.io), layout=Layout(width=f'{width}px'))
        set_background('transparent')

    def set_color(self, color='black'):
        self[0].fill_style = color
        self[0].fill_rect(0, 0, width=self.width, height=self.height)

    def show(self):
        display(self.body)
