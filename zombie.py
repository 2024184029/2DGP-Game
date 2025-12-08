from pico2d import *
import game_world
from state_machine import StateMachine
import random
from random import randint, choice
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
import math
from collision_bb import can_move
import camera
import ui_life

# 전역 변수

ROW_DOWN  = 6
ROW_SIDE  = 5
ROW_UP    = 2


ROW_ATTACK = 1

ATTACK_RANGE = 50
ATTACK_HIT_RANGE = 100

FRAME_COUNT = 5
FRAME_W = 200
FRAME_H = 200
SPEED = 0.15

class Zombie:
    hit_sound = None

    def __init__(self, boy):
        self.image = load_image('zombie_b.png')
        self.frame = 0
        self.scale = 1.0
        self.scale = 0.6
        self.frame_hold = 0

        if Zombie.hit_sound is None:
            Zombie.hit_sound = load_wav('zombie_hit.wav')
            Zombie.hit_sound.set_volume(32)

        self.cols, self.rows = 5, 7
        self.w = self.image.w // self.cols
        self.h = self.image.h // self.rows

        spawn_radius = 25
        tries = 0

        while True:
            tries += 1

            self.x, self.y = randint(100, 1000), randint(100, 1000)

            if not can_move(self.x, self.y, radius=spawn_radius):
                continue

            free_dirs = 0
            for dx, dy in [(30, 0), (-30, 0), (0, 30), (0, -30)]:
                if can_move(self.x + dx, self.y + dy, radius=spawn_radius):
                    free_dirs += 1

            if free_dirs > 0:
                break

            if tries > 50:
                break

        dx, dy = choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        self.vx, self.vy = dx * SPEED, dy * SPEED

        
        self.row = ROW_DOWN
        self.dir = 1

        self.face_dir = 'down'

        self.is_attacking = False


        self.boy = boy

        self.attack_cooltime = 1.0
        self.last_attack_time = 0.0

        self.build_behavior_tree()


    def enter(self):
        pass

    def update(self):
        self.bt.run()

        self.frame_hold += 1
        if self.frame_hold >= 70:
            self.frame_hold = 0
            self.frame = (self.frame + 1) % FRAME_COUNT

        x, y = self.x, self.y
        nx = x + self.vx
        ny = y + self.vy

        # 화면 경계
        if nx < 50 or nx > 1450:
            self.vx = -self.vx
            nx = x + self.vx
        if ny < 50 or ny > 950:
            self.vy = -self.vy
            ny = y + self.vy

        if can_move(nx, ny, radius=25):
            self.x, self.y = nx, ny
        else:
            self.vx = -self.vx
            self.vy = -self.vy

    def draw(self):
        sx = (self.frame % FRAME_COUNT) * self.w
        use_row = ROW_ATTACK if self.is_attacking else self.row
        sy = use_row * self.h

        draw_x, draw_y = camera.world_to_screen(self.x, self.y)

        if self.row == ROW_SIDE and self.dir == -1:
            self.image.clip_composite_draw(
                sx, sy, self.w, self.h,
                0, 'h',
                draw_x, draw_y,
                int(self.w * self.scale),
                int(self.h * self.scale)
            )
        else:
            self.image.clip_draw(
                sx, sy,
                self.w, self.h,
                draw_x, draw_y,
                int(self.w * self.scale),
                int(self.h * self.scale)
            )

        left, bottom, right, top = self.get_bb()
        l, b = camera.world_to_screen(left, bottom)
        r, t = camera.world_to_screen(right, top)
        # draw_rectangle(l, b, r, t)

    # 충돌 처리
    def get_bb(self):
            half_w = self.w * 0.3 * self.scale
            half_h = self.h * 0.4 * self.scale

            left   = self.x - half_w
            right  = self.x + half_w
            bottom = self.y - half_h
            top    = self.y + half_h

            if not self.is_attacking:
                return left, bottom, right, top

            extra = half_w

            if self.face_dir == 'right':
                right += extra
            elif self.face_dir == 'left':
                left -= extra
            elif self.face_dir == 'up':
                top += extra
            elif self.face_dir == 'down':
                bottom -= extra

            return left, bottom, right, top

    def get_attack_bb(self):
        left, bottom, right, top = self.get_bb()

        pad_x = (right - left) * 0.2
        pad_y = (top - bottom) * 0.2

        return left + pad_x, bottom + pad_y, right - pad_x, top - pad_y


    # ----- Behavior Tree -----

    def is_boy_near(self, r):
        dx = self.boy.x - self.x
        dy = self.boy.y - self.y
        distance2 = dx * dx + dy * dy
        return BehaviorTree.SUCCESS if distance2 <= r * r else BehaviorTree.FAIL

    def update_row_from_velocity(self):
        # 수평 이동이 더 큰 경우 (좌/우)
        if abs(self.vx) >= abs(self.vy):
            self.row = ROW_SIDE
            if self.vx >= 0:
                self.dir = 1   # 오른쪽
                self.face_dir = 'right'
            else:
                self.dir = -1  # 왼쪽
                self.face_dir = 'left'

        else:
            self.dir = 1
            if self.vy > 0:
                self.row = ROW_UP      # 위로 (등)
                self.face_dir = 'up'
            else:
                self.row = ROW_DOWN    # 아래로 (정면)
                self.face_dir = 'down'

    def wander(self):
        self.is_attacking = False
        now = get_time()
        if now > self.next_turn:
            self.next_turn = now + 1.5
            dx, dy = choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
            self.vx, self.vy = dx * SPEED, dy * SPEED
            self.update_row_from_velocity()
        return BehaviorTree.RUNNING

    def chase_boy(self):
        self.is_attacking = False
        dx = self.boy.x - self.x
        dy = self.boy.y - self.y
        dist = math.sqrt(dx * dx + dy * dy) + 1e-6

        self.vx = (dx / dist) * SPEED * 1.4
        self.vy = (dy / dist) * SPEED * 1.4
        self.update_row_from_velocity()
        return BehaviorTree.RUNNING

    def attack_boy(self):
        self.is_attacking = True

        self.vx = 0
        self.vy = 0

        dx = self.boy.x - self.x
        dy = self.boy.y - self.y

        if abs(dx) >= abs(dy):
            if dx >= 0:
                self.face_dir = 'right'
                self.dir = 1
            else:
                self.face_dir = 'left'
                self.dir = -1
        else:
            if dy >= 0:
                self.face_dir = 'up'
            else:
                self.face_dir = 'down'


        dist2 = dx * dx + dy * dy
        effective_range = ATTACK_HIT_RANGE

        if dist2 <= (effective_range ** 2):
            now = get_time()
            if now - self.last_attack_time >= self.attack_cooltime:

                if Zombie.hit_sound:
                    Zombie.hit_sound.play()

                ui_life.take_damage(1)
                self.last_attack_time = now

        return BehaviorTree.RUNNING


    def build_behavior_tree(self):

        c_boy_attack = Condition('플레이어가 매우 가까운가?', self.is_boy_near, ATTACK_RANGE)
        a_attack = Action('공격', self.attack_boy)
        attack = Sequence('근접하면 공격', c_boy_attack, a_attack)

        c_boy_near = Condition('플레이어가 가까운가?', self.is_boy_near, 270)
        a_chase = Action('플레이어 추적', self.chase_boy)
        chase = Sequence('가까우면 추적', c_boy_near, a_chase)

        a_wander = Action('배회', self.wander)

        root = Selector('공격 또는 추적 또는 배회', attack, chase, a_wander)

        self.bt = BehaviorTree(root)