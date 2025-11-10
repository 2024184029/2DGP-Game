from pico2d import *
import game_world
from state_machine import StateMachine
import random
from random import randint, choice

# 전역 변수
ROW_DOWN  = 0   # 정면 - 아래
ROW_LEFT  = 1   # 왼쪽
ROW_RIGHT = 2   # 오른쪽
ROW_UP    = 3   # 등 - 위

FRAME_COUNT = 4
SPEED = 0.2

class Zombie:
    global ROW_DOWN, ROW_LEFT, ROW_RIGHT, ROW_UP
    global FRAME_COUNT, SPEED

    def __init__(self):
        self.image = load_image('zombie.png')
        self.frame = 0
        self.scale = 1.0
        self.x, self.y = randint(100, 1000), randint(100, 1000)
        dx, dy = choice([(1, 0), (-1, 0), (0, 1), (0, -1)]) # 시작 4방향 중 하나 (오, 왼, 위, 아래)
        self.next_turn = get_time() + 1.5 #1.5초마다 자동 방향 전환
        self.row = ROW_DOWN # 시작은 정면 방향
        self.vx, self.vy = dx * SPEED, dy * SPEED
        self.cols, self.rows = 4, 4


    def enter(self):
        pass

    def update(self):
        # 위치 갱신
        self.x += self.vx
        self.y += self.vy

        if self.x < 50 or self.x > 1000:   # 왼/오른쪽 벽
            self.vx = -self.vx            # 방향 반전
        if self.y < 50 or self.y > 1000:   # 위/아래 벽
            self.vy = -self.vy            # 방향 반전

        t = get_time()
        if t >= self.next_turn:
            dx, dy = choice([(1,0), (-1,0), (0,1), (0,-1)])
            self.vx, self.vy = dx * SPEED, dy * SPEED
            self.next_turn = t + 1.5

        # 방향으로 애니메이션 행 선택
        if abs(self.vx) >= abs(self.vy):
            self.row = ROW_LEFT if self.vx > 0 else ROW_RIGHT
        else:
            self.row = ROW_DOWN if self.vy > 0 else ROW_UP

        self.frame = (self.frame + 1) % FRAME_COUNT

    def draw(self):
        sx = (self.frame % FRAME_COUNT) * 100
        # sy = (self.frame // FRAME_COUNT) * 200
        sy = self.row * 200
        self.image.clip_draw(sx, sy, 100, 200, self.x, self.y)

        # bb 보이게 함
        draw_rectangle(*self.get_bb())

    # 충돌 처리
    def get_bb(self):
        half = 100 * self.scale
        return self.x - half + 70, self.y - half, self.x + half - 70, self.y + half - 40

