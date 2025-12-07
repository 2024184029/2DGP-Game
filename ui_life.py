from pico2d import load_image, get_time

HEART_MAX = 3  # 최대 하트 개수

heart_image = None
gameover_image = None

hearts = HEART_MAX
game_over = False
_game_over_time = 0.0


def init():
    """
    게임 시작 시 한 번 호출해서 이미지 로딩 + 상태 초기화
    """
    global heart_image, gameover_image, hearts, game_over, _game_over_time

    if heart_image is None:
        heart_image = load_image('heart.png')      # 네 하트 이미지 이름
    if gameover_image is None:
        gameover_image = load_image('gameover.png')  # 게임오버 이미지 이름

    hearts = HEART_MAX
    game_over = False
    _game_over_time = 0.0


def draw_hearts():
    """
    화면 좌측 상단에 남은 하트 개수만큼 그리기
    """
    if heart_image is None:
        return

    # 화면 크기 1500x1000 기준
    for i in range(hearts):
        x = 80 + i * 80   # 하트 간격
        y = 900           # 위쪽에 고정
        heart_image.draw(x, y, 60, 60)  # 실제 크기(100x100)보다 살짝 줄여서 표시


def draw_gameover():
    """
    게임오버 상태일 때 중앙에 gameover.png 그리기
    """
    if not game_over or gameover_image is None:
        return

    gameover_image.draw(1500 // 2, 1000 // 2)


def take_damage(amount=1):
    """
    좀비 공격 등으로 데미지 입을 때 호출
    """
    global hearts, game_over, _game_over_time

    if game_over:
        return

    hearts -= amount
    if hearts <= 0:
        hearts = 0
        game_over = True
        _game_over_time = get_time()  # 이 시점부터 2초 후 종료


def is_game_over():
    return game_over


def should_quit():
    """
    게임오버된 후 2초 정도 보여주고 나갈지 여부
    """
    if not game_over:
        return False

    return (get_time() - _game_over_time) > 2.0
