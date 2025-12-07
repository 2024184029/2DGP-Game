from pico2d import *
import game_framework
from mask import Mask

# 전역 변수
room_image = None
player = None
room_mask = None

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
            if self.frame_hold >= 8:
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

def init():
    global room_image, player, room_mask

    room_image = load_image('room.png')
    player = RoomPlayer()
    room_mask = Mask(player)


def finish():
    global room_image, player, room_mask

    room_image = None
    player = None
    room_mask = None


def update():

    if player:
        player.update()


def draw():
    clear_canvas()

    room_image.draw(1500 // 2, 1000 // 2, 1500, 1000)

    if player:
        player.draw()

    if room_mask:
        room_mask.draw()

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
