from pico2d import *
import game_framework
import play_mode as play_state

def main():
    open_canvas(1024, 1024)  # HD 해상도 권장
    game_framework.run(play_state)
    close_canvas()

if __name__ == "__main__":
    main()
