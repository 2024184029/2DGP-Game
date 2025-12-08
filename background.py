from pico2d import *
import camera

CANVAS_WIDTH  = 1500
CANVAS_HEIGHT = 1000

class Background:
    def __init__(self):
        # self.image = load_image('background.png')
        self.image = load_image('village.png')

        # 마을 배경 음악 로딩 & 재생
        self.bgm = load_music('village.ogg')
        self.bgm.set_volume(32)
        self.bgm.repeat_play()

        camera.MAP_W = self.image.w
        camera.MAP_H = self.image.h

    def update(self):
        pass

    def draw(self):
        cw, ch = get_canvas_width(), get_canvas_height()

        self.image.clip_draw_to_origin(
            camera.window_left,
            camera.window_bottom,
            cw, ch,
            0, 0
        )