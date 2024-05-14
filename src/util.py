import imageio
import matplotlib.pyplot as plt
import numpy as np
import tqdm
from IPython.display import display, Video

def grab_plot(close=True):
    fig = plt.gcf()
    fig.canvas.draw()
    img = np.array(fig.canvas.renderer._renderer)
    a = np.float32(img[..., 3:]/255.)
    img = np.uint8(255.*(1. - a) + img[..., :3]*a)
    if close:
        plt.close()
    return img

class VideoWriter:
    def __init__(self, filename='_autoplay.mp4', size=400, fps=30.):
        self.filename = filename
        self.size = size
        self.fps = fps

        self.frames = []

    def __enter__(self):
        return self
    
    def __exit__(self, *_):
        if self.filename == '_autoplay.mp4':
            self.show()
        else:
            self.save()

    def write(self, frame):
        frame = np.uint8(frame.clip(0, 1)*255.)
        self.frames.append(frame)

    def save(self):
        with imageio.imopen(self.filename, 'w', plugin='pyav') as out:
            out.init_video_stream('vp9', fps=self.fps)
            for frame in self.frames:
                out.write_frame(frame)
    
    def show(self):
        self.save()
        video = Video(self.filename, width=self.size, height=self.size)
        display(video)
