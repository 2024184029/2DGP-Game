# collision_bb.py
from pico2d import draw_rectangle
import camera

OBSTACLES = [
    (140, 430, 250, 560),
    (90, 180, 170, 340),
    (400, 770, 710, 800),
    (480, 560, 585, 630),
    (232, 54, 370, 181),
    (110, 629, 182, 750),
    (606, 340, 773, 438),
    (455, 200, 528, 272),
    (760, 74, 880, 192),
    (959, 170, 1062, 230),
    (920, 428, 1136, 460),
    (837, 868, 988, 940),
    (908, 576, 1064, 712),
    (1290, 646, 1439, 736),
    (1277, 425, 1435, 501),
]

def can_move(nx, ny, radius=0):
    for left, bottom, right, top in OBSTACLES:
        if nx + radius > left and nx - radius < right and \
           ny + radius > bottom and ny - radius < top:
            return False
    return True

def draw_collision_boxes():
    for left, bottom, right, top in OBSTACLES:

        l, b = camera.world_to_screen(left, bottom)
        r, t = camera.world_to_screen(right, top)

        # draw_rectangle(l, b, r, t)