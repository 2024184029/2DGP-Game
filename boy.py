from pico2d import load_image, draw_rectangle
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_UP, SDLK_DOWN

import game_world
import camera
from state_machine import StateMachine
from attack import Attack
from collision_bb import can_move

FRAME_COLS = 5
FRAME_ROWS = 3
IDLE_ROW = 0
RUN_ROW  = 1
SPEED = 0.3

IDLE_FRAMES = [(0,0), (0,1), (0,2), (0,3)]

RUN_FRAMES = [
    (1,0), (1,1), (1,2), (1,3), (1,4),
    (2,0), (2,1), (2,2)
]

MISSION_FRAME_COLS = 4
MISSION_FRAME_ROWS = 2

MISSION_FRAMES = [
    (0, 0), (0, 1), (0, 2), (0, 3),
    (1, 0), (1, 1), (1, 2)
]

instance = None
caution_image = None

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

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
        self.frame_hold = 0

    def enter(self, e):
        self.boy.dx = 0
        self.boy.dy = 0
        self.boy.frame = 0
        self.frame_hold = 0

    def exit(self, e):
        pass

    def do(self):
        self.frame_hold += 1

        if self.frame_hold >= 20:
            self.frame_hold = 0
            self.boy.frame = (self.boy.frame + 1) % len(IDLE_FRAMES)

    def draw(self):
        row, col = IDLE_FRAMES[self.boy.frame]

        sx =  col * self.boy.fw
        sy = (FRAME_ROWS - 1 - row) * self.boy.fh

        draw_x, draw_y = camera.world_to_screen(self.boy.x, self.boy.y)

        if self.boy.current_dir >= 0:
            self.boy.image.clip_draw(
                sx, sy, self.boy.fw, self.boy.fh,
                draw_x, draw_y
            )
        else:
            self.boy.image.clip_composite_draw(
                sx, sy, self.boy.fw, self.boy.fh,
                0, 'h',
                draw_x, draw_y,
                self.boy.fw, self.boy.fh
            )


class Run:
    def __init__(self, boy):
        self.boy = boy
        self.frame_hold = 0

    def enter(self, e):
        if right_down(e):       self.boy.dx += 1; self.boy.current_dir = 1
        elif right_up(e):       self.boy.dx -= 1
        elif left_down(e):      self.boy.dx -= 1; self.boy.current_dir = -1
        elif left_up(e):        self.boy.dx += 1
        elif up_down(e):        self.boy.dy += 1
        elif up_up(e):          self.boy.dy -= 1
        elif down_down(e):      self.boy.dy -= 1
        elif down_up(e):        self.boy.dy += 1

        self.frame_hold = 0

    def exit(self, e):
        pass

    def do(self):
        # 애니메이션
        self.frame_hold += 1
        if self.frame_hold >= 18:
            self.frame_hold = 0
            self.boy.frame = (self.boy.frame + 1) % len(RUN_FRAMES)

        x, y = self.boy.x, self.boy.y

        SPEED = 0.3
        if self.boy.dx != 0 and self.boy.dy != 0:
            dx = (self.boy.dx * SPEED) / 1.5
            dy = (self.boy.dy * SPEED) / 1.5
        else:
            dx = self.boy.dx * SPEED
            dy = self.boy.dy * SPEED

        nx = x + dx
        ny = y + dy

        W, H = 1500, 1000
        half_w, half_h = self.boy.fw // 2, self.boy.fh // 2
        nx = max(half_w, min(nx, W - half_w))
        ny = max(half_h, min(ny, H - half_h))

        if can_move(nx, ny, radius=20):
            self.boy.x, self.boy.y = nx, ny

        if self.boy.dx == 0 and self.boy.dy == 0:
            self.boy.state_machine.handle_state_event(('STOP', None))

    def draw(self):

        row, col = RUN_FRAMES[self.boy.frame]

        sx = col * self.boy.fw
        sy = (FRAME_ROWS - 1 - row) * self.boy.fh

        draw_x, draw_y = camera.world_to_screen(self.boy.x, self.boy.y)

        if self.boy.current_dir >= 0:
            self.boy.image.clip_draw(
                sx, sy, self.boy.fw, self.boy.fh,
                draw_x, draw_y
            )
        else:
            self.boy.image.clip_composite_draw(
                sx, sy, self.boy.fw, self.boy.fh,
                0, 'h',
                draw_x, draw_y,
                self.boy.fw, self.boy.fh
            )

class Mission:
    def __init__(self, boy):
        self.boy = boy
        self.frame_hold = 0

    def enter(self, e):
        self.boy.dx = 0
        self.boy.dy = 0
        self.boy.mission_frame = 0
        self.frame_hold = 0
        self.boy.is_attacking = True

        attack = Attack(self.boy.x, self.boy.y, self.boy.current_dir)
        game_world.add_object(attack, 2)

    def exit(self, e):
        self.boy.is_attacking = False

    def do(self):
        self.frame_hold += 1

        if self.frame_hold >= 25:
            self.frame_hold = 0
            self.boy.mission_frame += 1

        if self.boy.mission_frame >= len(MISSION_FRAMES):
            self.boy.state_machine.handle_state_event(('MISSION_END', None))
            self.boy.mission_frame = len(MISSION_FRAMES) - 1

    def draw(self):
        row, col = MISSION_FRAMES[self.boy.mission_frame]

        sx = col * self.boy.mfw
        sy = (MISSION_FRAME_ROWS - 1 - row) * self.boy.mfh


        draw_x, draw_y = camera.world_to_screen(self.boy.x, self.boy.y)

        if self.boy.current_dir >= 0:
            self.boy.mission_image.clip_draw(
                sx, sy, self.boy.mfw, self.boy.mfh,
                draw_x, draw_y
            )
        else:
            self.boy.mission_image.clip_composite_draw(
                sx, sy, self.boy.mfw, self.boy.mfh,
                0, 'h',
                draw_x, draw_y,
                self.boy.mfw, self.boy.mfh
            )


class Boy:
    def __init__(self):
        self.x, self.y = 475, 76
        self.frame = 0
        self.scale = 1.0

        self.dx = 0
        self.dy = 0
        self.current_dir = 1
        self.image = load_image('boy.png')

        self.fw = self.image.w // FRAME_COLS
        self.fh = self.image.h // FRAME_ROWS

        self.mission_image = load_image('boy_mission.png')
        self.mfw = self.mission_image.w // MISSION_FRAME_COLS
        self.mfh = self.mission_image.h // MISSION_FRAME_ROWS
        self.mission_frame = 0
        self.is_attacking = False
        self.IDLE = Idle(self)
        self.RUN = Run(self)
        self.MISSION = Mission(self)

        self.caution_icon = False
        global caution_image
        if caution_image is None:
            caution_image = load_image('caution.png')
        global instance
        instance = self

        def is_stop(ev): return ev[0] == 'STOP'
        def is_mission_end(ev): return ev[0] == 'MISSION_END'

        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE : {right_down: self.RUN,
                             left_down: self.RUN,
                             up_down: self.RUN,
                             down_down: self.RUN,
                             space_down: self.MISSION},

                self.RUN : {right_down: self.RUN,
                            left_down: self.RUN,
                            up_down: self.RUN,
                            down_down: self.RUN,
                            right_up: self.RUN,
                            left_up: self.RUN,
                            up_up: self.RUN,
                            down_up: self.RUN,
                            space_down: self.MISSION,
                            is_stop: self.IDLE},

                self.MISSION: {
                    is_mission_end: self.IDLE
                }
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()

        draw_x, draw_y = camera.world_to_screen(self.x, self.y)

        if self.caution_icon:
            caution_image.draw(draw_x, draw_y + 50, 80, 80)

        left, bottom, right, top = self.get_bb()
        bb_left, bb_bottom = camera.world_to_screen(left, bottom)
        bb_right, bb_top = camera.world_to_screen(right, top)
        # draw_rectangle(bb_left, bb_bottom, bb_right, bb_top)

        if self.is_attacking:
            a_left, a_bottom, a_right, a_top = self.get_attack_bb()
            a_left, a_bottom = camera.world_to_screen(a_left, a_bottom)
            a_right, a_top = camera.world_to_screen(a_right, a_top)
            # draw_rectangle(a_left, a_bottom, a_right, a_top)

    @staticmethod
    def get_instance():
        return instance

    # 충돌 처리
    def get_bb(self):
        half = 100 * self.scale
        return self.x - half + 85, self.y - half + 50, self.x + half - 80, self.y + half - 80

    def get_attack_bb(self):
        left, bottom, right, top = self.get_bb()

        if self.current_dir >= 0:
            attack_left  = right
            attack_right = right + 90
        else:
            attack_left  = left - 90
            attack_right = left

        attack_bottom = bottom + 10
        attack_top    = top - 10

        return attack_left, attack_bottom, attack_right, attack_top
