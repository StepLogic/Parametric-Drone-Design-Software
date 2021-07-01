from time import time

from Helper import resource_path, absolute_path


class Camera(object):
    """An emulated camera implementation that streams a repeated sequence of
    files 1.jpg, 2.jpg and 3.jpg at a rate of one frame per second."""

    def __init__(self):
        self.frames = open(f'{resource_path(absolute_path+"/Server/")}2.jpg', 'rb').read()

    def get_frame(self):
        val=[self.frames,self.frames,self.frames]
        return val[int(time()) % 3]
