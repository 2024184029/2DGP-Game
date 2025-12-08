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
import mask
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
# room에서 키를 먹었는지 여부
has_master_key = False

# EXIT 문 / 게임클리어 관련
EXIT_X, EXIT_Y = 1050, 430  # 마을에서 exit 문 위치 (월드 좌표)

exit_image = None
exit_active = False          # 키 가져오고 마을로 돌아오면 True
exit_cols = 8                # exit.png 가로 프레임 수 (800 / 8 = 100)
exit_frame = 0
exit_frame_hold = 0
exit_frame_delay = 20         # 숫자 클수록 느리게

exit_playing = False         # 플레이어가 문 앞에 서서 애니메이션 재생 중인지
boy_removed = False          # 애니메이션 끝나고 플레이어 삭제했는지

DOOR_SCALE = 0.6             # 문 크기 줄이기

gameclear_image = None
game_cleared = False
gameclear_start_time = 0.0



def pause():
    pass

def resume():
    # room_mode에서 돌아왔을 때, 키를 먹었으면 exit 문 활성화
    global exit_active
    if has_master_key:
        exit_active = True

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

    import mask as mask_module
    global mask
    mask = Mask(boy)
    game_world.add_object(mask, 3)
    # 시야 레벨 초기화 (마을 시작할 때 항상 1단계부터)
    mask_module.reset_mask_level()   # 시야 레벨 초기화

    global doors, key_door_index
    doors = []
    DOOR_POSITIONS = [
        (135, 250),  # 왼쪽 아래 집
        (495, 180),  # 왼쪽 우측 아래 집
        (140, 670),  # 왼쪽 위 3층 집
        (720, 340),  # 가운데 중간 집
        (1005, 580),  # 오른쪽 위 큰 집들 중 하나
        (900, 860),  # 오른쪽 위 젤 큰 집
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

    # ★ exit / gameclear 이미지 로딩 및 상태 초기화
    global exit_image, exit_active, exit_frame, exit_frame_hold
    global exit_playing, boy_removed
    global gameclear_image, game_cleared, gameclear_start_time

    exit_image = load_image('exit.png')          # 800x150짜리 스프라이트 시트
    gameclear_image = load_image('gameclear.png')

    exit_active = False
    exit_frame = 0
    exit_frame_hold = 0
    exit_playing = False
    boy_removed = False

    game_cleared = False
    gameclear_start_time = 0.0

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

    # 문이 완전히 열린 문이 하나라도 있으면 RoomMode로 전환
    for d in doors:
        if d.is_open and not d.entered_room:
            d.entered_room = True

            import room_mode
            room_mode.set_room_has_key(getattr(d, 'has_key_room', False))
            game_framework.push_mode(room_mode)
            return

    # exit / gameclear 상태 갱신
    update_exit_and_clear()

    # 게임 오버면 더 이상 진행 안 함
    if game_over:
        return


def update_exit_and_clear():

    global exit_frame, exit_frame_hold
    global exit_playing, boy_removed
    global game_cleared, gameclear_start_time

    if not exit_active:
        return

    # 이미 클리어 상태라면, 일정 시간 뒤 게임 종료
    if game_cleared:
        if time.time() - gameclear_start_time > 3.0:
            game_framework.quit()
        return

    # 아직 클리어 전인데, 애니메이션 재생 중이면 프레임만 갱신
    if exit_playing:
        # 프레임 천천히 넘기기
        exit_frame_hold += 1
        if exit_frame_hold >= exit_frame_delay:
            exit_frame_hold = 0
            exit_frame += 1

            # 마지막 프레임(7)까지 재생했으면 클리어 처리
            if exit_frame >= exit_cols:
                exit_frame = exit_cols - 1  # 마지막 프레임 유지
                exit_playing = False

                # 플레이어 제거 (문 안으로 들어간 느낌)
                if not boy_removed:
                    game_world.remove_object(boy)
                    boy_removed = True

                # 게임 클리어 상태로 전환
                game_cleared = True
                gameclear_start_time = time.time()

        return

    # 여기까지 왔다는 건 아직 애니메이션 재생 안 한 상태(exit_playing == False, game_cleared == False)

    # boy가 exit 문 근처에 오면 애니메이션 재생 시작
    dx = boy.x - EXIT_X
    dy = boy.y - EXIT_Y
    if dx * dx + dy * dy <= (80 ** 2):   # 반경 80픽셀 안
        exit_playing = True
        exit_frame = 0
        exit_frame_hold = 0

def draw_exit_and_clear():

    # exit 문
    if exit_active and exit_image:
        fw = exit_image.w // exit_cols   # 100
        fh = exit_image.h                # 150

        # 재생 중이 아니면 항상 0번 프레임 보여줌
        frame_index = exit_frame if exit_playing or game_cleared else 0

        col = frame_index % exit_cols
        sx = col * fw
        sy = 0

        # 월드 좌표 → 화면 좌표
        sx_screen, sy_screen = camera.world_to_screen(EXIT_X, EXIT_Y)

        draw_w = fw * DOOR_SCALE
        draw_h = fh * DOOR_SCALE

        exit_image.clip_draw(
            sx, sy, fw, fh,
            sx_screen, sy_screen,
            draw_w, draw_h
        )

    # gameclear 오버레이
    if game_cleared and gameclear_image:
        w = get_canvas_width()
        h = get_canvas_height()
        gameclear_image.draw(w // 2, h // 2)



def handle_attack_collision():
    if not boy.is_attacking:
        return

    attack_bb = boy.get_attack_bb()
    # 공격 당하면 제거됨 (나중에 체력 깎는 걸로 수정하기)
    import mask as mask_module
    for e in enemies[:]:
        if collide(attack_bb, e.get_bb()):
            game_world.remove_object(e)
            enemies.remove(e)
            # 적 하나 죽일 때마다 시야를 한 단계 넓힘
            mask_module.increase_mask_level()

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
    draw_exit_and_clear()

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

