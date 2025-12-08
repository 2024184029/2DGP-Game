from pico2d import *
import camera

mask_level = 1
MAX_MASK_LEVEL = 3

_mask_images = [None, None, None, None]


class Mask:
    def __init__(self, boy):
        global _mask_images
        self.boy = boy

        if _mask_images[1] is None:
            _mask_images[1] = load_image('mask1.png')
            _mask_images[2] = load_image('mask2.png')
            _mask_images[3] = load_image('mask3.png')

    def update(self):
        pass

    def draw(self):

        global mask_level, _mask_images

        img = _mask_images[mask_level]
        if img is None:
            return

        sx, sy = camera.world_to_screen(self.boy.x, self.boy.y)
        img.draw(sx, sy)


def increase_mask_level():
    global mask_level
    if mask_level < MAX_MASK_LEVEL:
        mask_level += 1


def reset_mask_level():

    global mask_level
    mask_level = 1
