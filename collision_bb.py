# collision_bb.py
from pico2d import draw_rectangle

# 1) 충돌 박스 목록 (left, bottom, right, top)
OBSTACLES = [
    (200, 400, 400, 650),
    (650, 250, 950, 600),
    (1100, 450, 1350, 750),
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
