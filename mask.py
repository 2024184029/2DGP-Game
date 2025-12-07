from pico2d import *
import camera

# 시야 단계 (숫자 커질수록 시야 넓어짐)
mask_level = 1
MAX_MASK_LEVEL = 3

# 마스크 이미지
_mask_images = [None, None, None, None]


class Mask:
    def __init__(self, boy):
        global _mask_images
        self.boy = boy

        # 처음 한 번만 마스크 이미지 로딩
        if _mask_images[1] is None:
            _mask_images[1] = load_image('mask1.png')
            _mask_images[2] = load_image('mask2.png')
            _mask_images[3] = load_image('mask3.png')

    def update(self):
        # 지금은 별도의 애니메이션 없음
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
