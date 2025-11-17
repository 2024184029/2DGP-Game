from pico2d import *
import game_framework
import title_mode

def main():
    open_canvas(1024, 1024)
    game_framework.run(title_mode)
    close_canvas()

if __name__ == "__main__":
    main()
