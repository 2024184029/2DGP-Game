from pico2d import load_image, draw_rectangle,  load_wav
import camera

class Door:
    image = None
    open_sound = None

    def __init__(self, x, y):
        if Door.image is None:
            Door.image = load_image('door.png')

        if Door.open_sound is None:
            Door.open_sound = load_wav('door_open.ogg')
            Door.open_sound.set_volume(32)

        self.x = x
        self.y = y
        self.scale = 0.28

        self.total_frames = 4
        self.w = Door.image.w // self.total_frames
        self.h = Door.image.h

        self.frame = 0
        self.frame_hold = 0
        self.frame_delay = 50

        self.is_opening = False
        self.is_open = False
        self.already_hit = False

    def start_open(self):
        if self.is_open:
            return
        self.is_opening = True
        self.frame = 0
        self.frame_hold = 0

    def update(self):
        pass

    def hit(self):
        if self.is_open:
            return

        if Door.open_sound:
            Door.open_sound.play()

        self.frame += 1
        print("Door hit. frame =", self.frame)

        if self.frame >= self.total_frames:
            self.frame = self.total_frames - 1
            self.is_open = True

    def draw(self):
        sx = self.frame * self.w
        sy = 0

        draw_x, draw_y = camera.world_to_screen(self.x, self.y)

        Door.image.clip_draw(
            sx, sy, self.w, self.h,
            draw_x, draw_y,
            int(self.w * self.scale),
            int(self.h * self.scale)
        )

        # draw_rectangle(*self.get_bb())

    def get_bb(self):
        half_w = int(self.w * self.scale) // 2
        half_h = int(self.h * self.scale) // 2
        return (self.x - half_w, self.y - half_h,
                self.x + half_w, self.y + half_h)
