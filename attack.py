from pico2d import *
import game_world
import camera

attack_image = None

ATTACK_FRAMES = [
    (4,   0, 104, 200),
    (117, 0, 204, 200),
    (329, 0, 192, 200),
    (529, 0, 105, 200),
    (641, 0,  55, 200),
]

class Attack:
    def __init__(self, x, y, dir):

        global attack_image
        if attack_image is None:
            attack_image = load_image('attack.png')

        self.image = attack_image
        self.x, self.y = x, y
        self.dir = dir

        self.frame = 0
        self.frame_hold = 0
        self.frame_delay = 30
        self.scale = 0.3

    def update(self):
        self.frame_hold += 1
        if self.frame_hold >= self.frame_delay:
            self.frame_hold = 0
            self.frame += 1

            if self.frame >= len(ATTACK_FRAMES):
                game_world.remove_object(self)
                return

    def draw(self):
        sx, sy, sw, sh = ATTACK_FRAMES[self.frame]

        scale = self.scale
        dw = sw * scale
        dh = sh * scale

        screen_x, screen_y = camera.world_to_screen(self.x, self.y)

        if self.dir >= 0:
            draw_x = screen_x + dw * 1.3
            self.image.clip_draw(
                sx, sy, sw, sh,
                draw_x, screen_y, dw, dh
            )
        else:
            draw_x = screen_x - dw * 1.3
            self.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, 'h',
                draw_x, screen_y, dw, dh
            )


    def get_bb(self):
        sx, sy, sw, sh = ATTACK_FRAMES[self.frame]
        scale = self.scale
        w = sw * scale
        h = sh * scale
        if self.dir >= 0:
            cx = self.x + w * 0.6
        else:
            cx = self.x - w * 0.6

        cy = self.y
        half_w = w * 0.5
        half_h = h * 0.5
        return cx - half_w, cy - half_h, cx + half_w, cy + half_h
