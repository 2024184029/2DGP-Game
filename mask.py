from pico2d import *

class Mask:
    def __init__(self, boy):
        self.image = load_image('mask.png')
        self.boy = boy

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.boy.x, self.boy.y)
