# collision_bb.py
from pico2d import draw_rectangle

# 1) 충돌 박스 목록 (left, bottom, right, top)
OBSTACLES = [
    (120, 430, 250, 550),
    (212, 54, 390, 181),
    (90, 629, 182, 750),
    (586, 308, 773, 438),
    (435, 152, 528, 272),
    (740, 74, 880, 192),
    (939, 89, 1062, 235),
    (890, 378, 1136, 460), # 이건 y줄일 필요 없음
    (817, 818, 988, 940),
    (1020, 792, 1216, 943), # 이건 y줄일 필요 없음
    (888, 536, 1064, 712),
    (1270, 606, 1439, 736),
    (1257, 385, 1435, 501),
]

def can_move(nx, ny, radius=0):
    # (nx, ny)를 중심으로, radius를 가진 원
    for left, bottom, right, top in OBSTACLES:
        if nx + radius > left and nx - radius < right and \
           ny + radius > bottom and ny - radius < top:
            return False
    return True

def draw_collision_boxes():
    for left, bottom, right, top in OBSTACLES:
        draw_rectangle(left, bottom, right, top)
