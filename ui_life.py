from pico2d import load_image, get_time

HEART_MAX = 3  # 최대 하트 개수

heart_image = None
gameover_image = None

hearts = HEART_MAX
game_over = False
_game_over_time = 0.0


def init():
    global heart_image, gameover_image, hearts, game_over, _game_over_time

    if heart_image is None:
        heart_image = load_image('heart.png')      # 네 하트 이미지 이름
    if gameover_image is None:
        gameover_image = load_image('gameover.png')  # 게임오버 이미지 이름

    hearts = HEART_MAX
    game_over = False
    _game_over_time = 0.0


def draw_hearts():
    if heart_image is None:
        return

    for i in range(hearts):
        x = 80 + i * 80   # 하트 간격
        y = 900           # 위쪽에 고정
        heart_image.draw(x, y, 60, 60)


def draw_gameover():
    if not game_over or gameover_image is None:
        return

    gameover_image.draw(1500 // 2, 1000 // 2)


def take_damage(amount=1):
    global hearts, game_over, _game_over_time

    if game_over:
        return

    hearts -= amount
    if hearts <= 0:
        hearts = 0
        game_over = True
        _game_over_time = get_time()


def is_game_over():
    return game_over


def should_quit():
    if not game_over:
        return False
    # 5초 후 종료
    return (get_time() - _game_over_time) > 5.0
