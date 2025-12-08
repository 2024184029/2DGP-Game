# collision_bb.py
from pico2d import draw_rectangle
import camera

# 1) 충돌 박스 목록 (left, bottom, right, top)
OBSTACLES = [
    (140, 430, 250, 550),
    (232, 54, 390, 181),
    (110, 629, 182, 750),
    (606, 340, 773, 438),
    (455, 200, 528, 272),
    (760, 74, 880, 192),
    (959, 170, 1062, 230),
    (920, 428, 1136, 460), # 이건 y줄일 필요 없음
    (837, 868, 988, 940),
    (908, 576, 1064, 712),
    (1290, 646, 1439, 736),
    (1277, 425, 1435, 501),
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

        l, b = camera.world_to_screen(left, bottom)
        r, t = camera.world_to_screen(right, top)

        draw_rectangle(l, b, r, t)