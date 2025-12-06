# door.py
from pico2d import load_image, draw_rectangle


class Door:
    image = None

    def __init__(self, x, y):
        if Door.image is None:
            Door.image = load_image('door.png')

        self.x = x
        self.y = y
        self.scale = 0.25

        # door.png - 가로 4프레임
        self.total_frames = 4
        self.w = Door.image.w // self.total_frames
        self.h = Door.image.h

        # 애니메이션 상태
        self.frame = 0           # 현재 프레임 (0이면 닫힌 상태)
        self.frame_hold = 0      # 프레임 유지 카운터
        self.frame_delay = 50     # 몇 tic마다 다음 프레임으로 넘어갈지

        self.is_opening = False  # 열리는 중인지
        self.is_open = False     # 완전히 열린 상태인지

    # 플레이어 공격이 맞았을 때 호출
    def start_open(self):
        if self.is_open:         # 이미 다 열린 문이면 무시
            return
        self.is_opening = True
        self.frame = 0
        self.frame_hold = 0

    def update(self):
        # 열리는 중일 때만 애니메이션 진행
        if self.is_opening and not self.is_open:
            self.frame_hold += 1
            if self.frame_hold >= self.frame_delay:
                self.frame_hold = 0
                self.frame += 1

                # 마지막 프레임까지 재생하면 열린 상태로 고정
                if self.frame >= self.total_frames:
                    self.frame = self.total_frames - 1
                    self.is_open = True
                    self.is_opening = False

    def draw(self):
        # 현재 프레임 한 칸만 잘라서 그리기
        sx = self.frame * self.w
        sy = 0
        Door.image.clip_draw(
            sx, sy,
            self.w, self.h,
            self.x, self.y,
            int(self.w * self.scale),
            int(self.h * self.scale)
        )

        # 디버그용 BB
        # draw_rectangle(*self.get_bb())

    # 공격 충돌용 BB
    def get_bb(self):
        half_w = int(self.w * self.scale) // 2
        half_h = int(self.h * self.scale) // 2
        return (self.x - half_w, self.y - half_h,
                self.x + half_w, self.y + half_h)
