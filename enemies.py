from pico2d import *
import random
from random import choice
import camera

FRAME_COLS = 2
FRAME_ROWS = 4
FRAME_W = 100
FRAME_H = 100

DEFAULT_SPEED = 0.10
DEFAULT_MOVE_RADIUS = 30
DEFAULT_FRAME_DELAY = 15

class Enemies:
    def __init__(self, image_file, x, y,
                 move_radius=DEFAULT_MOVE_RADIUS,
                 speed=DEFAULT_SPEED,
                 frame_delay=DEFAULT_FRAME_DELAY):

        self.image = load_image(image_file)
        self.x, self.y = x, y
        self.origin_x, self.origin_y = x, y

        self.move_radius = move_radius
        self.speed = speed
        self.frame_delay = frame_delay

        self.cols = FRAME_COLS
        self.rows = FRAME_ROWS
        self.fw = self.image.w // self.cols    # 100
        self.fh = self.image.h // self.rows    # 100

        self.frame = 0
        self.frame_count = self.cols * self.rows   # 8프레임
        self.frame_hold = 0

        dx, dy = choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        self.vx, self.vy = dx * self.speed, dy * self.speed

        self.next_turn = get_time() + 1.5

        self.scale = 1.0

    def update(self):
        self.x += self.vx
        self.y += self.vy

        if self.x < self.origin_x - self.move_radius: # 좌 우
            self.x = self.origin_x - self.move_radius
            self.vx = -self.vx
        elif self.x > self.origin_x + self.move_radius:
            self.x = self.origin_x + self.move_radius
            self.vx = -self.vx

        if self.y < self.origin_y - self.move_radius: # 위 아래
            self.y = self.origin_y - self.move_radius
            self.vy = -self.vy
        elif self.y > self.origin_y + self.move_radius:
            self.y = self.origin_y + self.move_radius
            self.vy = -self.vy

        t = get_time()
        if t >= self.next_turn:
            dx, dy = choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
            self.vx, self.vy = dx * self.speed, dy * self.speed
            self.next_turn = t + 2.0

        self.frame_hold += 0.5

        if self.frame_hold >= self.frame_delay:
            self.frame_hold = 0
            self.frame = (self.frame + 1) % self.frame_count

    def draw(self):
        col = self.frame % self.cols
        row = self.frame // self.cols

        scale = 0.5

        sx = col * self.fw
        sy = (self.rows - 1 - row) * self.fh

        draw_x, draw_y = camera.world_to_screen(self.x, self.y)

        self.image.clip_draw(
            sx, sy, self.fw, self.fh,
            draw_x, draw_y,
            self.fw * scale, self.fh * scale
        )

        left, bottom, right, top = self.get_bb()  # 월드 좌표
        l, b = camera.world_to_screen(left, bottom)
        r, t = camera.world_to_screen(right, top)
        # draw_rectangle(l, b, r, t)

    def get_bb(self):
        half_w = self.fw * 0.3
        half_h = self.fh * 0.3
        return self.x - half_w, self.y - half_h, self.x + half_w, self.y + half_h


class Corn(Enemies):
    def __init__(self, x, y):
        super().__init__('corn.png', x, y, # 부모 클래스 생성자
                         move_radius=50,
                         speed=0.20,
                         frame_delay=40)


class Snail(Enemies):
    def __init__(self, x, y):
        super().__init__('snail.png', x, y,
                         move_radius=50,
                         speed=0.010,
                         frame_delay=50)


class Bug(Enemies):
    def __init__(self, x, y):
        super().__init__('bug.png', x, y,
                         move_radius=50,
                         speed=0.10,
                         frame_delay=40)
