# room_mode.py
from pico2d import *
import game_framework
import game_world
import play_mode  # ESC로 다시 마을로 나갈 거면 필요

name = "RoomMode"

image = None


def init():
    """룸 화면 초기화: room.png 로드"""
    global image
    # 캔버스가 이미 open_canvas() 된 상태라고 가정
    image = load_image('room.png')


def finish():
    """룸 모드 끝날 때 호출 (지금은 비워둬도 상관 없음)"""
    # 룸 안에서 game_world에 뭘 올릴 거면 여기서 정리하면 됨
    pass


def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for e in events:
        if e.type == SDL_QUIT:
            game_framework.quit()

        elif e.type == SDL_KEYDOWN:
            # ESC 누르면 다시 마을(play_mode)로 나가기
            if e.key == SDLK_ESCAPE:
                game_framework.change_mode(play_mode)
            # TODO: 나중에 여기서 룸 안 미션 관련 키 입력 처리하면 됨


def update():
    # 나중에 룸 안에서 좀비/퍼즐/타이머 넣으면 여기에서 업데이트
    pass


def draw():
    clear_canvas()
    w, h = get_canvas_width(), get_canvas_height()
    # 화면 정중앙에 room.png 그리기
    image.draw(w // 2, h // 2)
    update_canvas()
# room_mode.py
from pico2d import *
import game_framework
import game_world
import play_mode  # ESC로 다시 마을로 나갈 거면 필요

name = "RoomMode"

image = None


def init():
    """룸 화면 초기화: room.png 로드"""
    global image
    # 캔버스가 이미 open_canvas() 된 상태라고 가정
    image = load_image('room.png')


def finish():
    """룸 모드 끝날 때 호출 (지금은 비워둬도 상관 없음)"""
    # 룸 안에서 game_world에 뭘 올릴 거면 여기서 정리하면 됨
    pass


def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for e in events:
        if e.type == SDL_QUIT:
            game_framework.quit()

        elif e.type == SDL_KEYDOWN:
            # ESC 누르면 다시 마을(play_mode)로 나가기
            if e.key == SDLK_ESCAPE:
                game_framework.change_mode(play_mode)
            # TODO: 나중에 여기서 룸 안 미션 관련 키 입력 처리하면 됨


def update():
    # 나중에 룸 안에서 좀비/퍼즐/타이머 넣으면 여기에서 업데이트
    pass


def draw():
    clear_canvas()
    w, h = get_canvas_width(), get_canvas_height()
    # 화면 정중앙에 room.png 그리기
    image.draw(w // 2, h // 2)
    update_canvas()
