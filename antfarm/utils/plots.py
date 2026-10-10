"""
Author(s): Craig fouts
Correspondence: foutscw@gmail.com
License: Apache 2.0 license
"""

import matplotlib.pyplot as plt
import numpy as np
from IPython.display import clear_output, display, HTML

def grab_plot(close=True):
    """Converts the current Matplotlib canvas into an RGB image array.
    """

    fig = plt.gcf()
    fig.canvas.draw()
    img = np.array(fig.canvas.renderer._renderer)
    opacity = np.float32(img[..., 3:]/255.)
    img = np.uint8(img[..., :3]*opacity + 255.*(1. - opacity))

    if close:
        plt.close()

    return img

def set_background(color='transparent'):
    display(HTML('''
        <style>
            .cell-output-ipywidget-background {
                background-color: %s !important;
            }
        </style>
    ''' % color))
