from pico2d import *
import game_world
from state_machine import StateMachine
import random
from random import randint, choice
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
import math
from collision_bb import can_move

# 전역 변수

ROW_DOWN  = 6   # 정면(위에서 0번째 줄)
ROW_SIDE  = 5   # 옆 이동(위에서 1번째 줄)
ROW_UP    = 2   # 등(위에서 4번째 줄)

# 공격 애니메이션이 있는 줄 (위에서 5번째 줄)
ROW_ATTACK = 1

ATTACK_RANGE = 80    # 공격 유효 범위

FRAME_COUNT = 5
FRAME_W = 200
FRAME_H = 200
SPEED = 0.15

class Zombie:
    def __init__(self, boy):
        self.image = load_image('zombie_b.png')
        self.frame = 0
        self.scale = 1.0
        self.scale = 0.6
        self.frame_hold = 0

        # 새 스프라이트 시트 정보 (5x7)
        self.cols, self.rows = 5, 7
        self.w = self.image.w // self.cols
        self.h = self.image.h // self.rows

        # 시작 위치 랜덤
        self.x, self.y = randint(100, 1000), randint(100, 1000)
        dx, dy = choice([(1, 0), (-1, 0), (0, 1), (0, -1)]) # 시작 4방향 중 하나 (오, 왼, 위, 아래)
        self.vx, self.vy = dx * SPEED, dy * SPEED
        
        self.row = ROW_DOWN # 시작은 정면 방향
        self.dir = 1

        # 어디를 보고 있는지(공격 범위 방향용)
        self.face_dir = 'down'   # 'left', 'right', 'up', 'down'

        # 지금 공격 중인지 T/F
        self.is_attacking = False

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

        # 애니메이션
        self.frame_hold += 1
        if self.frame_hold >= 70:
            self.frame_hold = 0
            self.frame = (self.frame + 1) % FRAME_COUNT

        x, y = self.x, self.y
        # 기본 이동 후보
        nx = x + self.vx
        ny = y + self.vy

        # 화면 경계
        if nx < 50 or nx > 1450:
            self.vx = -self.vx
            nx = x + self.vx
        if ny < 50 or ny > 950:
            self.vy = -self.vy
            ny = y + self.vy

        # 좀비 크기에 맞는 반지름(25 정도)으로 충돌 검사
        if can_move(nx, ny, radius=25):
            self.x, self.y = nx, ny
        else:
            # 벽이면 튕겨나가게
            self.vx = -self.vx
            self.vy = -self.vy

    def draw(self):
        sx = (self.frame % FRAME_COUNT) * self.w

        # 이동일 때는 self.row, 공격 중이면 공격 줄 사용
        use_row = ROW_ATTACK if self.is_attacking else self.row
        sy = use_row * self.h
        # sy = (self.row) * self.h

        if self.row == ROW_SIDE and self.dir == -1:
            self.image.clip_composite_draw(
                sx, sy, self.w, self.h,
                0, 'h',
                self.x, self.y,
                int(self.w * self.scale),
                int(self.h * self.scale)
            )
        else:
            # 정면 / 등 / 오른쪽 이동
            self.image.clip_draw(
                sx, sy,
                self.w, self.h,
                self.x, self.y,
                int(self.w * self.scale),
                int(self.h * self.scale)
            )
        # bb 보이게 함
        draw_rectangle(*self.get_bb())

    # 충돌 처리
    def get_bb(self):
            half_w = self.w * 0.3 * self.scale
            half_h = self.h * 0.4 * self.scale
            # return self.x - half_w, self.y - half_h, self.x + half_w, self.y + half_h

            left   = self.x - half_w
            right  = self.x + half_w
            bottom = self.y - half_h
            top    = self.y + half_h

            # 공격 중 아니면 그냥 몸통만
            if not self.is_attacking:
                return left, bottom, right, top

            # 공격 중이면 보는 방향 쪽으로 범위를 늘려줌
            extra = half_w  # 얼마나 더 뻗어나갈지

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
        # 몸통 기준 박스를 가져온 뒤, “진짜 공격 범위”만 따로 추출하고 싶으면
        # 지금은 get_bb()에서 이미 확장했으니,
        # 여기서는 살짝 더 안쪽으로 줄여서 '공격 핵심 판정' 정도로 써도 됨.

        left, bottom, right, top = self.get_bb()

        # 몸통 + 확장된 전체 박스 기준에서 살짝 안쪽만 사용
        pad_x = (right - left) * 0.2
        pad_y = (top - bottom) * 0.2

        return left + pad_x, bottom + pad_y, right - pad_x, top - pad_y


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


    # 배회 - 일정 시간마다 랜덤 방향으로만 바꿔줌
    def wander(self):
        self.is_attacking = False
        now = get_time()
        if now > self.next_turn:
            self.next_turn = now + 1.5
            dx, dy = choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
            self.vx, self.vy = dx * SPEED, dy * SPEED
            self.update_row_from_velocity()
        return BehaviorTree.RUNNING

    # 추적 - Boy를 향해 빠른 속도로 이동
    def chase_boy(self):
        self.is_attacking = False
        dx = self.boy.x - self.x
        dy = self.boy.y - self.y
        dist = math.sqrt(dx * dx + dy * dy) + 1e-6

        # Boy 방향으로
        self.vx = (dx / dist) * SPEED * 1.2  # 추적할 때 더 빠르게
        self.vy = (dy / dist) * SPEED * 1.2
        self.update_row_from_velocity()
        return BehaviorTree.RUNNING


    # 공격 - 매우 가까울 때 제자리에서 공격 모션
    def attack_boy(self):
        # 공격 중임 표시
        self.is_attacking = True

        # 이동은 멈추고
        self.vx = 0
        self.vy = 0

        # 플레이어 위치를 보고 방향만 맞춰줌 (공격 범위 방향 계산용)
        dx = self.boy.x - self.x
        dy = self.boy.y - self.y

        if abs(dx) >= abs(dy):
            # 좌우 방향
            if dx >= 0:
                self.face_dir = 'right'
                self.dir = 1
            else:
                self.face_dir = 'left'
                self.dir = -1
        else:
            # 상하 방향
            if dy >= 0:
                self.face_dir = 'up'
            else:
                self.face_dir = 'down'

        # 공격은 계속해서 유지되는 행동이라 RUNNING 반환
        return BehaviorTree.RUNNING


    def build_behavior_tree(self):

        c_boy_attack = Condition('플레이어가 매우 가까운가?', self.is_boy_near, ATTACK_RANGE)
        a_attack = Action('공격', self.attack_boy)
        attack = Sequence('근접하면 공격', c_boy_attack, a_attack)

        # Boy가 가까이 있는지 (7m 정도)
        c_boy_near = Condition('플레이어가 가까운가?', self.is_boy_near, 200)

        # 가까우면 chase_boy
        a_chase = Action('플레이어 추적', self.chase_boy)
        chase = Sequence('가까우면 추적', c_boy_near, a_chase)
        # 멀면 wander
        a_wander = Action('배회', self.wander)

        root = Selector('공격 또는 추적 또는 배회', attack, chase, a_wander)

        self.bt = BehaviorTree(root)