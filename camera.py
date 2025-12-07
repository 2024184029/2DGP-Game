# camera.py
from pico2d import get_canvas_width, get_canvas_height

# 맵(배경) 전체 크기 – village 이미지 크기랑 맞춰줘
MAP_W = 1500
MAP_H = 1000

window_left = 0
window_bottom = 0

def clamp(minimum, x, maximum):
    return max(minimum, min(x, maximum))

def update_camera(target_x, target_y):
    global window_left, window_bottom

    cw, ch = get_canvas_width(), get_canvas_height()

    # 슬라이드 18–20쪽 방식: 플레이어를 화면 중앙에 두고 윈도우 계산
    window_left   = clamp(0, int(target_x) - cw // 2, MAP_W - cw)
    window_bottom = clamp(0, int(target_y) - ch // 2, MAP_H - ch)

def world_to_screen(x, y):
    return x - window_left, y - window_bottom
