from pico2d import *
import game_framework
from mask import Mask
import random
import ui_life
import play_mode

# 전역 변수
room_image = None
player = None
room_mask = None
key = None
has_key = False
room_has_key = False


def set_room_has_key(flag: bool):
    global room_has_key
    room_has_key = flag

class RoomPlayer:
    def __init__(self):
        self.image = load_image('boy.png')
        self.FRAME_COLS = 5
        self.FRAME_ROWS = 3

        self.fw = self.image.w // self.FRAME_COLS
        self.fh = self.image.h // self.FRAME_ROWS

        self.scale = 1.2

        self.x = 750
        self.y = 150

        self.dx = 0
        self.dy = 0

        self.face_dir = 1

        self.frame = 0
        self.frame_hold = 0

        self.SPEED = 0.3


    def update(self):
        # 이동
        nx = self.x + self.dx * self.SPEED
        ny = self.y + self.dy * self.SPEED

        W, H = 1500, 1000
        half_w = int(self.fw * self.scale) // 2
        half_h = int(self.fh * self.scale) // 2

        nx = max(half_w, min(nx, W - half_w))
        ny = max(half_h, min(ny, H - half_h))

        self.x, self.y = nx, ny

        if self.dx > 0:
            self.face_dir = 1
        elif self.dx < 0:
            self.face_dir = -1

        if self.dx != 0 or self.dy != 0:
            self.frame_hold += 1
            if self.frame_hold >= 30:
                self.frame_hold = 0
                self.frame = (self.frame + 1) % 4
        else:
            self.frame = 0
            self.frame_hold = 0



    def draw(self):
        row = 1
        col = self.frame

        sx = col * self.fw
        sy = (self.FRAME_ROWS - 1 - row) * self.fh

        draw_w = int(self.fw * self.scale)
        draw_h = int(self.fh * self.scale)

        if self.face_dir >= 0:
            self.image.clip_draw(
                sx, sy,
                self.fw, self.fh,
                self.x, self.y,
                draw_w, draw_h
            )
        else:
            self.image.clip_composite_draw(
                sx, sy, self.fw, self.fh,
                0, 'h',
                self.x, self.y,
                draw_w, draw_h
            )


import random

class Key:
    def __init__(self):
        self.image = load_image('key.png')

        self.cols = 12
        self.fw = self.image.w // self.cols
        self.fh = self.image.h

        # 키 생성 범위 제한
        min_x = 300
        max_x = 800
        min_y = 300
        max_y = 500

        self.x = random.randint(min_x, max_x)
        self.y = random.randint(min_y, max_y)
        self.scale = 0.3

        self.frame = 0
        self.frame_hold = 0
        self.frame_delay = 30

        margin_x = 150
        margin_y = 150
        self.x = random.randint(margin_x, 1500 - margin_x)
        self.y = random.randint(margin_y, 1000 - margin_y)

        self.pick_radius = 70

    def update(self):
        self.frame_hold += 1
        if self.frame_hold >= self.frame_delay:
            self.frame_hold = 0
            self.frame = (self.frame + 1) % self.cols

    def draw(self):
        sx = self.frame * self.fw
        sy = 0

        dw = int(self.fw * self.scale)
        dh = int(self.fh * self.scale)

        self.image.clip_draw(
            sx, sy,
            self.fw, self.fh,
            self.x, self.y,
            dw, dh
        )


def init():
    global room_image, player, room_mask, key, has_key

    room_image = load_image('room.png')
    player = RoomPlayer()
    room_mask = Mask(player)

    if room_has_key:
        key = Key()
    else:
        key = None

    has_key = False

def finish():
    global room_image, player, room_mask, key, has_key, room_has_key

    room_image = None
    player = None
    room_mask = None
    key = None
    has_key = False
    room_has_key = False


def update():
    global key, has_key

    if player:
        player.update()

    if key and not has_key:
        key.update()   # 프레임 애니메이션

        dx = player.x - key.x
        dy = player.y - key.y
        if dx * dx + dy * dy <= (key.pick_radius ** 2):
            has_key = True
            key = None
            play_mode.has_master_key = True

    if ui_life.should_quit():
        game_framework.quit()
        return


def draw():
    clear_canvas()

    room_image.draw(1500 // 2, 1000 // 2, 1500, 1000)

    if key:
        key.draw()

    if player:
        player.draw()

    if room_mask:
        room_mask.draw()

    ui_life.draw_hearts()
    ui_life.draw_gameover()

    update_canvas()


def handle_events():
    global player
    events = get_events()
    for e in events:
        if e.type == SDL_QUIT:
            game_framework.quit()

        elif e.type == SDL_KEYDOWN:
            if e.key == SDLK_ESCAPE:
                game_framework.pop_mode()
            elif e.key == SDLK_RIGHT:
                player.dx += 1
            elif e.key == SDLK_LEFT:
                player.dx -= 1
            elif e.key == SDLK_UP:
                player.dy += 1
            elif e.key == SDLK_DOWN:
                player.dy -= 1

        elif e.type == SDL_KEYUP:
            if e.key == SDLK_RIGHT:
                player.dx -= 1
            elif e.key == SDLK_LEFT:
                player.dx += 1
            elif e.key == SDLK_UP:
                player.dy -= 1
            elif e.key == SDLK_DOWN:
                player.dy += 1


def pause():
    pass


def resume():
    pass
