"""
Author(s): Craig fouts
License: Apache 2.0 license
"""

import imageio
from IPython.display import display, Video
from ..utils.sugar import attrmethod

class VideoWriter:
    """Utility for writing RGB image arrays to a video stream.
    """

    @attrmethod
    def __init__(self, width=500, height=500, fps=30., path='_autoplay.mp4'):
        self._frames = []

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.save()

        if self.path.endswith('_autoplay.mp4'):
            self.show()

    def write(self, img):
        """Adds the given RGB image array to the frame sequence.
        """

        self._frames.append(img)

    def save(self):
        """Converts the current frame sequence into a video stream.
        """

        with imageio.imopen(self.path, 'w', plugin='pyav') as vid:
            vid.init_video_stream('vp9', fps=self.fps)

            for frame in self._frames:
                vid.write_frame(frame)

    def show(self):
        self.save()
        vid = Video(self.path, width=self.width, height=self.height, )
        display(vid)
