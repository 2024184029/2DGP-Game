from pico2d import *
import game_framework
import play_mode   # 튜토리얼 끝나면 여기로 넘어감

image = None
font = None
intro_bgm = None

def pause():
    pass

def resume():
    pass

def init():
    global image, font, intro_bgm
    image = load_image('tutorial.png')
    font = load_font('D2Coding.ttc', 15)

    intro_bgm = load_music('intro.ogg')
    intro_bgm.set_volume(40)
    intro_bgm.repeat_play()

def finish():
    global image, intro_bgm
    if image is not None:
        del image

    if intro_bgm:
        intro_bgm.stop()
        intro_bgm = None

def update():
    pass

def draw():
    clear_canvas()
    image.draw(750, 500)  # 튜토리얼 이미지 중앙
    font.draw(620, 100, "PRESS SPACE OR CLICK TO START GAME", (255, 255, 255))
    update_canvas()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()

        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            game_framework.change_mode(play_mode)

        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            game_framework.change_mode(play_mode)
