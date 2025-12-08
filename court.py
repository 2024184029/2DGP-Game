from pico2d import *
import camera

class Court:
    def __init__(self, image_path='village.png'):
        self.image = load_image(image_path)

        self.bgm = load_music('village.ogg')
        self.bgm.set_volume(32)
        self.bgm.repeat_play()

        self.w = self.image.w
        self.h = self.image.h

        self.cw = get_canvas_width()
        self.ch = get_canvas_height()

        camera.MAP_W = self.w
        camera.MAP_H = self.h

    def update(self):
        import play_mode
        boy = play_mode.boy
        camera.update_camera(boy.x, boy.y)

    def draw(self):
        self.image.clip_draw_to_origin(
            camera.window_left,
            camera.window_bottom,
            self.cw, self.ch,
            0, 0
        )
