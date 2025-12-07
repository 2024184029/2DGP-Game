# court.py
from pico2d import *
import camera   # 네 camera.py

class Court:
    def __init__(self, image_path='village.png'):
        self.image = load_image(image_path)

        # 전체 맵 크기
        self.w = self.image.w
        self.h = self.image.h

        # 캔버스 크기 (500 × 500)
        self.cw = get_canvas_width()
        self.ch = get_canvas_height()

        # camera.py가 맵 크기를 알아야 하니까 세팅해줌
        camera.MAP_W = self.w
        camera.MAP_H = self.h

    def update(self):  # target = boy 객체
        import play_mode
        boy = play_mode.boy
        camera.update_camera(boy.x, boy.y)

        # BOY 중심으로 카메라 움직임 계산
        # camera.update_camera(target.x, target.y)

    def draw(self):
        self.image.clip_draw_to_origin(
            camera.window_left,
            camera.window_bottom,
            self.cw, self.ch,
            0, 0
        )
