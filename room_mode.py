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
key = None            # 키 객체
has_key = False       # 키 먹었는지 여부
room_has_key = False  # 이 방에 키가 있는지 여부


def set_room_has_key(flag: bool):
    # village 쪽에서 이 room에 key를 만들지 말지 알려주는 함수
    global room_has_key
    room_has_key = flag

class RoomPlayer:
    def __init__(self):
        self.image = load_image('boy.png')
        # 스프라이트 시트
        self.FRAME_COLS = 5
        self.FRAME_ROWS = 3

        self.fw = self.image.w // self.FRAME_COLS
        self.fh = self.image.h // self.FRAME_ROWS

        self.scale = 1.2

        # 방 안 시작 위치
        self.x = 750
        self.y = 150

        # 이동 방향 (키 입력으로 -1, 0, 1)
        self.dx = 0
        self.dy = 0

        # 현재 바라보는 방향 (1: 오른쪽, -1: 왼쪽)
        self.face_dir = 1

        # 간단한 애니메이션용 프레임
        self.frame = 0
        self.frame_hold = 0

        # 속도 (프레임당 픽셀)
        self.SPEED = 0.3


    def update(self):
        # 이동
        nx = self.x + self.dx * self.SPEED
        ny = self.y + self.dy * self.SPEED

        # 방 크기(마을이랑 똑같이 1500x1000 기준)
        W, H = 1500, 1000
        half_w = int(self.fw * self.scale) // 2
        half_h = int(self.fh * self.scale) // 2

        # 화면 벽에서 안 나가게 클램프
        nx = max(half_w, min(nx, W - half_w))
        ny = max(half_h, min(ny, H - half_h))

        self.x, self.y = nx, ny

        # 바라보는 방향 갱신
        if self.dx > 0:
            self.face_dir = 1
        elif self.dx < 0:
            self.face_dir = -1

        # 아주 간단한 프레임 애니메이션 (걸을 때만)
        if self.dx != 0 or self.dy != 0:
            self.frame_hold += 1
            if self.frame_hold >= 30:
                self.frame_hold = 0
                # 대충 RUN 행에 있는 프레임 범위 안에서만 돈다고 가정
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


import random  # 파일 맨 위 import 쪽에 이미 안 돼 있으면 추가

class Key:
    def __init__(self):
        # key.png는 1200x400, 가로 12프레임
        self.image = load_image('key.png')

        self.cols = 12
        self.fw = self.image.w // self.cols   # 1200 // 12 = 100
        self.fh = self.image.h                # 400

        # 키 생성 범위 제한
        min_x = 300
        max_x = 800
        min_y = 300
        max_y = 500

        self.x = random.randint(min_x, max_x)
        self.y = random.randint(min_y, max_y)

        # 화면에서는 조금 줄여서
        self.scale = 0.3   # 나중에 0.25~0.4 사이에서 마음에 드는 값 찾으면 됨

        # ★ 애니메이션용
        self.frame = 0
        self.frame_hold = 0   # 몇 프레임마다 넘길지 조절용
        self.frame_delay = 30


        # 방 안 랜덤 위치 (벽에서 조금 띄워줌)
        margin_x = 150
        margin_y = 150
        self.x = random.randint(margin_x, 1500 - margin_x)
        self.y = random.randint(margin_y, 1000 - margin_y)

        # 플레이어가 이 거리 안으로 오면 먹었다고 처리
        self.pick_radius = 70

    def update(self):
        self.frame_hold += 1
        if self.frame_hold >= self.frame_delay:
            self.frame_hold = 0
            self.frame = (self.frame + 1) % self.cols  # 0~11 반복

    def draw(self):
        # 현재 프레임 잘라서 그리기
        sx = self.frame * self.fw
        sy = 0  # 한 줄짜리 시트라서 0

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

    # 이 room에 key를 만들지 여부는 room_has_key를 보고 결정
    if room_has_key:
        key = Key()      # 키 있는 방이면 생성
    else:
        key = None       # 키 없는 방이면 생성 안 함

    has_key = False      # 이 room에서 아직 키 안 먹은 상태


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

    # 키가 존재하고 아직 안 먹었다면
    if key and not has_key:
        key.update()   # 프레임 애니메이션

        # 플레이어와의 거리 계산해서 먹었는지 체크
        dx = player.x - key.x
        dy = player.y - key.y
        if dx * dx + dy * dy <= (key.pick_radius ** 2):
            has_key = True
            key = None      # 화면에서 삭제
            play_mode.has_master_key = True

    if ui_life.should_quit():
        game_framework.quit()
        return


def draw():
    clear_canvas()

    room_image.draw(1500 // 2, 1000 // 2, 1500, 1000)

    # 키가 있으면 먼저 그림
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
