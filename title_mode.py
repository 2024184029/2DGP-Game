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
    image = load_image('background.png')

def finish():
    global image
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
