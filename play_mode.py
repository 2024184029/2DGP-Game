import game_framework
import title_mode
from pico2d import *
from boy import Boy
from background import Background
import game_world
from zombie import Zombie
from enemies import Corn, Snail, Bug
import time

running = True
image = None

start_time = 0
elapsed_time = 0
game_over = False
font = None # 시간 출력 폰트

def pause():
    pass

def resume():
    pass

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)

        else:
            boy.handle_event(event)


def init():
    background = Background()
    game_world.add_object(background, 0)

    global boy
    boy = Boy()
    game_world.add_object(boy, 1)

    global zombie
    zombie = Zombie()
    game_world.add_object(zombie, 1)

    global enemies
    enemies = [ Corn(300, 830), Snail(100, 350), Bug(750, 230) ]
    for e in enemies:
        game_world.add_object(e, 1)

    global start_time, font, game_over
    start_time = time.time()
    font = load_font('D2Coding.ttc', 30)
    game_over = False


def update():
    game_world.update()

    global start_time, elapsed_time, game_over

    if game_over:
        return

    elapsed_time = time.time() - start_time

    # 2분 경과 시 게임 오버
    if elapsed_time >= 120:
        game_over = True


def draw_timer():
    global elapsed_time, font

    total_seconds = int(elapsed_time)
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    time_text = f"{minutes:02}:{seconds:02}"

    font.draw(512, 900, time_text, (255, 255, 255))


def draw():
    clear_canvas()
    game_world.render()
    draw_timer()
    update_canvas()

def finish():
    game_world.clear()



