# camera.py
from pico2d import get_canvas_width, get_canvas_height

# 맵(배경) 전체 크기
MAP_W = 1500
MAP_H = 1000

# 카메라 민감도
CAMERA_SENS = 1.9

window_left = 0
window_bottom = 0

def clamp(minimum, x, maximum):
    return max(minimum, min(x, maximum))

def update_camera(target_x, target_y):
    global window_left, window_bottom

    cw, ch = get_canvas_width(), get_canvas_height()

    sx = target_x * CAMERA_SENS
    sy = target_y * CAMERA_SENS

    window_left   = clamp(0, int(sx) - cw // 2, MAP_W - cw)
    window_bottom = clamp(0, int(sy) - ch // 2, MAP_H - ch)

def world_to_screen(x, y):
    return x - window_left, y - window_bottom
