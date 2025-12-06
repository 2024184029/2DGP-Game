from pico2d import *
import game_world
from state_machine import StateMachine
import random
from random import randint, choice
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector

# 전역 변수
ROW_DOWN  = 0   # 정면 - 아래
ROW_LEFT  = 1   # 왼쪽
ROW_RIGHT = 2   # 오른쪽
ROW_UP    = 3   # 등 - 위

FRAME_COUNT = 4
SPEED = 0.15

class Zombie:
    global ROW_DOWN, ROW_LEFT, ROW_RIGHT, ROW_UP
    global FRAME_COUNT, SPEED

    def __init__(self, boy):
        self.image = load_image('zombie.png')
        self.frame = 0
        self.scale = 1.0

        # 시작 위치 랜덤
        self.x, self.y = randint(100, 1000), randint(100, 1000)
        dx, dy = choice([(1, 0), (-1, 0), (0, 1), (0, -1)]) # 시작 4방향 중 하나 (오, 왼, 위, 아래)
        self.next_turn = get_time() + 1.5 #1.5초마다 자동 방향 전환
        self.row = ROW_DOWN # 시작은 정면 방향
        self.vx, self.vy = dx * SPEED, dy * SPEED
        self.cols, self.rows = 4, 4
        self.frame_hold = 0

        # 배회 중일 때 방향을 다시 바꿀 시간
        self.next_turn = get_time() + 2.0

        # 추적 대상 (플레이어)
        self.boy = boy

        # Behavior Tree 구성
        self.build_behavior_tree()


    def enter(self):
        pass

    def update(self):
        self.bt.run()

        # 현재 속도대로 이동
        self.x += self.vx
        self.y += self.vy

        # 화면 경계에서 전환
        if self.x < 50 or self.x > 1000:   # 왼/오른쪽 벽
            self.vx = -self.vx            # 방향 반전
        if self.y < 50 or self.y > 1000:   # 위/아래 벽
            self.vy = -self.vy            # 방향 반전

        # t = get_time()
        # if t >= self.next_turn:
        #     dx, dy = choice([(1,0), (-1,0), (0,1), (0,-1)])
        #     self.vx, self.vy = dx * SPEED, dy * SPEED
        #     self.next_turn = t + 1.5
        #
        # # 방향으로 애니메이션 행 선택
        # if abs(self.vx) >= abs(self.vy):
        #     self.row = ROW_LEFT if self.vx > 0 else ROW_RIGHT
        # else:
        #     self.row = ROW_DOWN if self.vy > 0 else ROW_UP

        self.frame_hold += 1
        if self.frame_hold >= 70:  # 프레임 전환 속도 조절
            self.frame_hold = 0
            self.frame = (self.frame + 1) % FRAME_COUNT

    def draw(self):
        sx = (self.frame % FRAME_COUNT) * 100
        sy = self.row * 200
        self.image.clip_draw(sx, sy, 100, 200, self.x, self.y)

        # bb 보이게 함
        draw_rectangle(*self.get_bb())

    # 충돌 처리
    def get_bb(self):
        half = 100 * self.scale
        return self.x - half + 70, self.y - half, self.x + half - 70, self.y + half - 40

    # ----- Behavior Tree -----

    # Boy와의 거리가 r 이하인지
    def is_boy_near(self, r):
        dx = self.boy.x - self.x
        dy = self.boy.y - self.y
        distance2 = dx * dx + dy * dy
        return BehaviorTree.SUCCESS if distance2 <= r * r else BehaviorTree.FAIL

    # 현재 속도에 따라 애니메이션 행 선택
    def update_row_from_velocity(self):
        # 수평 이동이 더 큰 경우 (좌/우)
        if abs(self.vx) >= abs(self.vy):
            if self.vx > 0:  # 오른쪽으로 이동 중
                self.row = ROW_LEFT  # 기존 RIGHT 대신 LEFT
            else:  # 왼쪽으로 이동 중
                self.row = ROW_RIGHT  # 기존 LEFT 대신 RIGHT

        else:
            if self.vy > 0:  # 위로 이동 중 (등)
                self.row = ROW_DOWN  # 기존 UP 대신 DOWN
            else:  # 아래로 이동 중 (플레이어 쪽/정면)
                self.row = ROW_UP  # 기존 DOWN 대신 UP

    # 배회 - 일정 시간마다 랜덤 방향으로만 바꿔줌
    def wander(self):
        now = get_time()
        if now > self.next_turn:
            self.next_turn = now + 1.5
            dx, dy = choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
            self.vx, self.vy = dx * SPEED, dy * SPEED
            self.update_row_from_velocity()
        return BehaviorTree.RUNNING

    # 추적 - Boy를 향해 빠른 속도로 이동
    def chase_boy(self):
        dx = self.boy.x - self.x
        dy = self.boy.y - self.y
        dist = math.sqrt(dx * dx + dy * dy) + 1e-6

        # Boy 방향으로
        self.vx = (dx / dist) * SPEED * 1.2  # 추적할 때 더 빠르게
        self.vy = (dy / dist) * SPEED * 1.2
        self.update_row_from_velocity()
        return BehaviorTree.RUNNING

    def build_behavior_tree(self):
        # Boy가 가까이 있는지 (7m 정도)
        c_boy_near = Condition('플레이어가 가까운가?', self.is_boy_near, 200)

        # 가까우면 chase_boy
        a_chase = Action('플레이어 추적', self.chase_boy)
        chase = Sequence('가까우면 추적', c_boy_near, a_chase)
        # 멀면 wander
        a_wander = Action('배회', self.wander)

        root = Selector('추적 또는 배회', chase, a_wander)

        self.bt = BehaviorTree(root)