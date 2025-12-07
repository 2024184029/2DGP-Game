import background
import game_framework
import title_mode
from pico2d import *
from boy import Boy
from background import Background
import game_world
from zombie import Zombie
from enemies import Corn, Snail, Bug
import time
from mask import Mask
from door import Door
from collision_bb import draw_collision_boxes
import camera
import court
import random
import ui_life

running = True
image = None

start_time = 0
elapsed_time = 0
game_over = False
font = None # 시간 출력 폰트

doors = []
key_door_index = -1

def pause():
    pass

def resume():
    pass

def handle_events():
    global boy
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT or (event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE):
            game_framework.quit()
        if event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            x = event.x
            y = get_canvas_height() - 1 - event.y
            print(f"좌표: ({x}, {y})")

        boy.handle_event(event)

        if event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            attack_bb = boy.get_attack_bb()   # 이 시점에서 이미 방향/공격 상태 반영됨

            for d in doors:
                if not d.is_open and collide(attack_bb, d.get_bb()):
                    d.hit()

def init():
    # background = Background()
    background = court.Court('village.png')  # 추가된 부분
    game_world.add_object(background, 0)

    global boy
    boy = Boy()
    game_world.add_object(boy, 1)

    global zombie
    zombie = Zombie(boy)
    game_world.add_object(zombie, 1)

    global enemies
    enemies = [ Corn(300, 830), Snail(100, 350), Bug(750, 230) ]
    for e in enemies:
        game_world.add_object(e, 1)

    global mask
    mask = Mask(boy)
    game_world.add_object(mask, 3)

    global doors, key_door_index
    doors = []
    DOOR_POSITIONS = [
        (130, 240),  # 왼쪽 아래 집
        (488, 180),  # 왼쪽 우측 아래 집
        (135, 645),  # 왼쪽 위 3층 집
        (700, 330),  # 가운데 중간 집
        (980, 560),  # 오른쪽 위 큰 집들 중 하나
        (880, 840),  # 오른쪽 위 젤 큰 집
    ]

    # 6개 문 중에서 랜덤으로 1개를 "키 있는 방"으로 지정
    key_door_index = random.randint(0, len(DOOR_POSITIONS) - 1)

    for i, (x, y) in enumerate(DOOR_POSITIONS):
        d = Door(x, y)
        d.entered_room = False

        # 이 문을 통해 들어가는 room에 key가 있을지 여부
        d.has_key_room = (i == key_door_index)

        doors.append(d)

    game_world.add_objects(doors, 1)

    global start_time, font, game_over
    start_time = time.time()
    font = load_font('D2Coding.ttc', 40)
    game_over = False

    ui_life.init()


def update():
    game_world.update()
    # background.update(boy)
    # camera.update_camera(boy.x, boy.y) # 보이 위치 기준 카메라 갱신

    global start_time, elapsed_time, game_over

    handle_attack_collision()

    # 보이와 좀비 거리 계산해서 caution 아이콘 on/off
    dx = boy.x - zombie.x
    dy = boy.y - zombie.y
    distance = (dx ** 2 + dy ** 2) ** 0.5

    CAUTION_DISTANCE = 300
    boy.caution_icon = (distance <= CAUTION_DISTANCE)

    # 공격이 끝났다면 문들의 hit 상태 초기화
    if not boy.is_attacking:
        for d in doors:
            d.already_hit = False

    # 타이머 갱신
    elapsed_time = time.time() - start_time

    # 하트가 0이 된 뒤 2초 지나면 게임 종료
    if ui_life.should_quit():
        game_framework.quit()
        return

    # 2분 경과 시 게임 오버
    if elapsed_time >= 120:
        game_over = True

    # 문이 완전히 열린 문이 하나라도 있으면 RoomMode로 전환
    for d in doors:
        if d.is_open and not d.entered_room:
            d.entered_room = True

            import room_mode

            # 이 문이 키 방인지 여부를 room_mode에 알려준다
            room_mode.set_room_has_key(getattr(d, 'has_key_room', False))

            game_framework.push_mode(room_mode)
            return

    # 게임 오버면 더 이상 진행 안 함
    if game_over:
        return



def handle_attack_collision():
    if not boy.is_attacking:
        return

    attack_bb = boy.get_attack_bb()
    # 공격 당하면 제거됨 (나중에 체력 깎는 걸로 수정하기)
    for e in enemies[:]:
        if collide(attack_bb, e.get_bb()):
            game_world.remove_object(e)
            enemies.remove(e)

    # for d in doors:
    #     if not d.is_open and collide(attack_bb, d.get_bb()):
    #         if not d.already_hit:
    #             # d.start_open()
    #             print("Hit door at:", d.x, d.y)  # 디버그
    #             d.hit()

def draw_timer():
    global elapsed_time, font

    total_seconds = int(elapsed_time)
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    time_text = f"{minutes:02}:{seconds:02}"

    font.draw(730, 900, time_text, (255, 255, 255))


def draw():
    clear_canvas()
    game_world.render()
    draw_timer()
    draw_collision_boxes()
    ui_life.draw_hearts()
    ui_life.draw_gameover()

    update_canvas()

def collide(a, b):
    left_a, bottom_a, right_a, top_a = a
    left_b, bottom_b, right_b, top_b = b

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True


def finish():
    game_world.clear()

