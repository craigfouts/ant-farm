'''
Author(s): Craig Fouts
Correspondence: c.fouts25@imperial.ac.uk
License: Apache 2.0 license
'''

import numpy as np
from abc import ABCMeta, abstractmethod
from ipycanvas import Canvas
from IPython.display import display
from sklearn.utils import check_random_state
from ..utils import attrmethod

class Farm(metaclass=ABCMeta):
    timer = None
    running = False

    @attrmethod
    def __init__(self, farm_size=500.):
        self._canvas = Canvas(width=farm_size, height=farm_size)
        self._canvas.on_mouse_down(self._toggle)

    def _toggle(self, *_):
        if Farm.running:
            Farm.stop()
        else:
            Farm.running = True
            self._step()

    @abstractmethod
    def _draw(self):
        pass

    @abstractmethod
    def _step(self):
        pass

    def start(self):
        if Farm.running:
            Farm.stop()

        display(self._canvas)
        self._draw()

    @classmethod
    def stop(cls):
        if cls.timer is not None:
            cls.timer.cancel()

        cls.running = False

class Colony(metaclass=ABCMeta):
    @attrmethod
    def __init__(self, n_ants=500, *, farm_size=500, wrap=True, seed=None):
        self._seed = check_random_state(seed)
        self.X_ = self._seed.random((n_ants, 2))*farm_size
        self.V_ = 2*np.pi*self._seed.random((n_ants, 1))

    def __call__(self, *args, **kwargs):
        return self._step(*args, **kwargs)
    
    @abstractmethod
    def _step(self):
        pass

    # def record()

# """
# Craig Fouts (craig.fouts@igp.uu.se)
# """

# import imageio
# import matplotlib.pyplot as plt
# import numpy as np
# import os
# from functools import partial
# from ipycanvas import hold_canvas
# from IPython.display import display, Video
# from threading import Timer

# def draw(x, canvas, canvas_size=500, farm_color='black', ant_color='red', ant_size=3.):
#     with hold_canvas():
#         canvas.clear()
#         canvas.fill_style = farm_color
#         canvas.fill_rect(0, 0, width=canvas_size, height=canvas_size)
#         canvas.fill_style = ant_color
#         canvas.fill_circles(*x.T, ant_size)

# def plot(x, canvas_size=500, farm_color='black', ant_color='red', ant_opacity=1., ant_size=30.):
#     plt.tight_layout()
#     fig, ax = plt.subplots(1, 1, facecolor=farm_color, constrained_layout=True)
#     ax.scatter(*x.T, c=ant_color, alpha=ant_opacity, s=ant_size)
#     ax.axis([0, canvas_size, 0, canvas_size])
#     ax.invert_yaxis()
#     ax.set_axis_off()

#     return fig

# def grab_plot(close=True):
#     figure = plt.gcf()
#     figure.canvas.draw()
#     image = np.array(figure.canvas.renderer._renderer)
#     alpha = np.float32(image[..., 3:]/255.)
#     image = np.uint8(255.*(1. - alpha) + image[..., :3]*alpha)

#     if close:
#         plt.close()

#     return image

# class RunTime:
#     def __init__(self, function, interval=.02, *args, **kwargs):
#         self.function = function
#         self.interval = interval
#         self.args = args
#         self.kwargs = kwargs

#         self.timer = None
#         self.running = False

#     def _step(self):
#         self.running = False
#         self.start()
#         self.function(*self.args, **self.kwargs)

#     def start(self):
#         if not self.running:
#             self.timer = Timer(self.interval, self._step)
#             self.timer.start()
#             self.running = True

#     def stop(self):
#         self.timer.cancel()
#         self.running = False

# class VideoWriter:
#     def __init__(self, size=500, rate=30., path='../videos/_autoplay.mp4'):
#         self.size = size
#         self.rate = rate
#         self.path = path

#         self.frames = []

#     def __enter__(self):
#         return self
    
#     def __exit__(self, *_):
#         self.save()

#         if self.path[-13:] == '_autoplay.mp4':
#             self.show()

#     def write(self, image):
#         self.frames.append(image)

#     def save(self):
#         with imageio.imopen(self.path, 'w', plugin='pyav') as out:
#             out.init_video_stream('vp9', fps=self.rate)

#             for f in self.frames:
#                 out.write_frame(f)

#     def show(self):
#         self.save()
#         video = Video(self.path, width=self.size, height=self.size, embed=True)
#         display(video)

# class Farm:
#     def __init__(self, n_ants=500, farm_size=500, warn=True):
#         self.farm_size = farm_size
#         self.warn = warn

#         positions = np.random.rand(n_ants, 2)*farm_size
#         velocities = 2*np.pi*np.random.rand(n_ants, 1)
#         self.ants = np.hstack([positions, velocities])

#     def __call__(self, **kwargs):
#         if hasattr(self, 'forward'):
#             return self.forward(**kwargs)
        
#         if self.warn:
#             warnings.warn('Forward method not implemented.')

#         return self.ants
    
#     def plot(self, ant_size=10., ant_color='black', farm_color='white', return_plot=False):
#         fig, ax = plt.subplots(1, 1, facecolor=farm_color)
#         fig.subplots_adjust(left=.01, right=.99, bottom=.01, top=.99)
#         ax.scatter(*self.ants[:, :2].T, ant_size, ant_color)
#         ax.axis([0, self.farm_size, 0, self.farm_size])
#         ax.set_axis_off()

#         if return_plot:
#             return fig, ax

#     def record(self, n_steps=500, path='ant_farm.mp4', show=False, verbosity=1, plot_kwargs={}, **kwargs):
#         description = path.split('/')[-1].split('.')[0]
#         video = VideoWriter(self.farm_size, path=path)
        
#         for _ in tqdm(range(n_steps), desc=description) if verbosity > 0 else range(n_steps):
#             self.plot(**plot_kwargs)
#             video.write(grab_plot())
#             self(**kwargs)

#         if show:
#             video.show()
