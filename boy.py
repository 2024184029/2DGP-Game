from pico2d import load_image, draw_rectangle
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_UP, SDLK_DOWN

import game_world
from state_machine import StateMachine

# 캐릭터 스프라이트 정보
FRAME_COLS = 4
FRAME_ROWS = 3
IDLE_ROW = 0           # Idle 프레임이 있는 행
RUN_ROW  = 1           # Run 프레임이 있는 행
SPEED = 0.3

# 미션 해결을 위한 이벤트 (나중에 구현)
# def space_down(e): # e is space down ?
#     return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE
#
# time_out = lambda e: e[0] == 'TIMEOUT'

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT

def up_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_UP


def up_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_UP


def down_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_DOWN


def down_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_DOWN


class Idle:

    def __init__(self, boy):
        self.boy = boy
        self.boy.dy = 0
        self.boy.frame = 0

    def enter(self, e):
        self.boy.dx = 0
        self.boy.dy = 0
        self.boy.frame = 0

    def exit(self, e):
        pass

    def do(self):
        self.boy.frame = (self.boy.frame + 1) % FRAME_COLS

    def draw(self):
        offset_x = [-15, -10, -5, 0]  # 프레임별 중심 보정
        sx = (self.boy.frame % 4) * 100
        sy = 0 # 첫번째 행

        self.boy.image.clip_draw(sx, sy, 100, 100, self.boy.x + offset_x[self.boy.frame], self.boy.y)



class Run:
    def __init__(self, boy):
        self.boy = boy

    def enter(self, e):
        if right_down(e):       self.boy.dx += 1; self.boy.current_dir = 1
        elif right_up(e):       self.boy.dx -= 1
        elif left_down(e):      self.boy.dx -= 1; self.boy.current_dir = -1
        elif left_up(e):        self.boy.dx += 1
        elif up_down(e):        self.boy.dy += 1
        elif up_up(e):          self.boy.dy -= 1
        elif down_down(e):      self.boy.dy -= 1
        elif down_up(e):        self.boy.dy += 1

    def exit(self, e):
        pass

    def do(self):
        self.boy.frame = (self.boy.frame + 1) % FRAME_COLS

        self.boy.x += self.boy.dx * SPEED
        self.boy.y += self.boy.dy * SPEED

        W, H = 1024, 1024
        half_w, half_h = self.boy.fw // 2, self.boy.fh // 2
        self.boy.x = max(half_w, min(self.boy.x, W - half_w))
        self.boy.y = max(half_h, min(self.boy.y, H - half_h))

        if self.boy.dx != 0 and self.boy.dy != 0:
            self.boy.x += (self.boy.dx * SPEED) / 1.5
            self.boy.y += (self.boy.dy * SPEED) / 1.5
        else:
            self.boy.x += self.boy.dx * SPEED
            self.boy.y += self.boy.dy * SPEED

        # 정지하면 IDLE 상태로 전환
        if self.boy.dx == 0 and self.boy.dy == 0:
            self.boy.state_machine.handle_state_event(('STOP', None))

    def draw(self):
        offset_x = [-14, -10, -5, 0, 5]
        sx = (self.boy.frame % 5) * 100
        sy = 100 # 두번째 행

        if self.boy.current_dir < 0:
            self.boy.image.clip_draw(sx+100, sy, 100, 100, self.boy.x + offset_x[self.boy.frame], self.boy.y)
        else: # face_dir == -1: # left
            self.boy.image.clip_draw(sx, sy, 100, 100, self.boy.x + offset_x[self.boy.frame], self.boy.y)


class Boy:
    def __init__(self):
        self.x, self.y = 360, 150
        self.frame = 0
        self.scale = 1.0

        self.dx = 0 # 이동상태
        self.dy = 0
        self.current_dir = 1
        self.image = load_image('boy.png')

        self.fw = self.image.w // FRAME_COLS
        self.fh = self.image.h // FRAME_ROWS

        self.IDLE = Idle(self)
        self.RUN = Run(self)

        def is_stop(ev): return ev[0] == 'STOP'
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE : {right_down: self.RUN, left_down: self.RUN, up_down: self.RUN, down_down: self.RUN},
                self.RUN : {right_down: self.RUN, left_down: self.RUN, up_down: self.RUN, down_down: self.RUN,
                            right_up: self.RUN,   left_up: self.RUN,   up_up: self.RUN,   down_up: self.RUN,
                            is_stop: self.IDLE}
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()

        draw_rectangle(*self.get_bb())

    # 충돌 처리
    def get_bb(self):
        half = 100 * self.scale
        return self.x - half + 85, self.y - half + 60, self.x + half - 80, self.y + half - 70
