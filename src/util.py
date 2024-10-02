import imageio
import matplotlib.pyplot as plt
import numpy as np
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
    fig = plt.gcf()
    fig.canvas.draw()
    img = np.array(fig.canvas.renderer._renderer)
    a = np.float32(img[..., 3:]/255.)
    img = np.uint8(255.*(1. - a) + img[..., :3]*a)

    if close:
        plt.close()

    return img

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
    def __init__(self, filename='_autoplay.mp4', size=400, frame_rate=30.):
        self.filename = filename
        self.size = size
        self.frame_rate = frame_rate

        self.frames = []

    def __enter__(self):
        return self
    
    def __exit__(self, *_):
        if self.filename == '_autoplay.mp4':
            self.show()
        else:
            self.save()

    def write(self, frame):
        self.frames.append(frame)

    def save(self):
        with imageio.imopen(self.filename, 'w', plugin='pyav') as out:
            out.init_video_stream('vp9', fps=self.frame_rate)

            for frame in self.frames:
                out.write_frame(frame)
    
    def show(self):
        self.save()
        video = Video(self.filename, width=self.size, height=self.size)
        display(video)