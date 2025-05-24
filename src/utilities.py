"""
Craig Fouts (craig.fouts@igp.uu.se)
"""

import imageio
import matplotlib.pyplot as plt
import numpy as np
import os
from functools import partial
from ipycanvas import hold_canvas
from IPython.display import display, Video
from threading import Timer

def draw(x, canvas, canvas_size=500, farm_color='black', ant_color='red', ant_size=3.):
    with hold_canvas():
        canvas.clear()
        canvas.fill_style = farm_color
        canvas.fill_rect(0, 0, width=canvas_size, height=canvas_size)
        canvas.fill_style = ant_color
        canvas.fill_circles(*x.T, ant_size)

def plot(x, canvas_size=500, farm_color='black', ant_color='red', ant_opacity=1., ant_size=30.):
    plt.tight_layout()
    fig, ax = plt.subplots(1, 1, facecolor=farm_color, constrained_layout=True)
    ax.scatter(*x.T, c=ant_color, alpha=ant_opacity, s=ant_size)
    ax.axis([0, canvas_size, 0, canvas_size])
    ax.invert_yaxis()
    ax.set_axis_off()

    return fig

def grab_plot(close=True):
    """Converts the current Matplotlib canvas into an RGB image array.
    
    Parameters
    ----------
    close : bool, default=True
        Whether to close the plot after conversion.

    Returns
    -------
    ndarray
        RGB image array.
    """

    figure = plt.gcf()
    figure.canvas.draw()
    image = np.array(figure.canvas.renderer._renderer)
    alpha = np.float32(image[..., 3:]/255.)
    image = np.uint8(255.*(1. - alpha) + image[..., :3]*alpha)

    if close:
        plt.close()

    return image

class RunTime:
    def __init__(self, function, interval=.02, *args, **kwargs):
        self.function = function
        self.interval = interval
        self.args = args
        self.kwargs = kwargs

        self.timer = None
        self.running = False

    def _step(self):
        self.running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.running:
            self.timer = Timer(self.interval, self._step)
            self.timer.start()
            self.running = True

    def stop(self):
        self.timer.cancel()
        self.running = False

class VideoWriter:
    """Utilitiy that writes RGB image arrays into a video stream.
    
    Parameters
    ----------
    size : int, default=500
        Video canvas width and height.
    rate : float, default=30.0
        Video frame rate.
    path : str, default='_autoplay.mp4'
        Video file path.

    Attributes
    ----------
    frames : list
        Sequence of RGB image arrays.

    Usage
    -----
    >>> with VideoWriter(frame_rate=15) as video:
    >>>     for i in range(1, 100):
    >>>         x = np.arange(i)
    >>>         plt.plot(x, np.sin(x))
    >>>         video.write(grab_plot())
    """

    def __init__(self, size=500, rate=30., path='../videos/_autoplay.mp4'):
        self.size = size
        self.rate = rate
        self.path = path

        self.frames = []

    def __enter__(self):
        return self
    
    def __exit__(self, *_):
        self.save()

        if self.path[-13:] == '_autoplay.mp4':
            self.show()

    def write(self, image):
        """Adds the given RGB image array to the frame sequence.
        
        Parameters
        ----------
        image : ndarray
            RGB image array.

        Returns
        -------
        None
        """

        self.frames.append(image)

    def save(self):
        """Converts the current frame sequence into a video stream.
        
        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        with imageio.imopen(self.path, 'w', plugin='pyav') as out:
            out.init_video_stream('vp9', fps=self.rate)

            for f in self.frames:
                out.write_frame(f)

    def show(self):
        self.save()
        video = Video(self.path, width=self.size, height=self.size, embed=True)
        display(video)
