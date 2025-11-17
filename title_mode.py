from pico2d import *
import game_framework
import play_mode

image = None

def pause():
    pass

def resume():
    pass

def init():
    global image
    image = load_image('title.png')

def finish():
    global image
    if image is not None:
        del image # 메모리 소멸

def update():
    pass

def draw():
    clear_canvas()
    image.draw(512, 512)
    update_canvas()

def handle_events():
    # flush events
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            game_framework.change_mode(play_mode)
        # 마우스 왼쪽 클릭해도 전환
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            game_framework.change_mode(play_mode)
