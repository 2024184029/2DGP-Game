from pico2d import load_image

CANVAS_WIDTH  = 1536
CANVAS_HEIGHT = 1024

class Background:
    def __init__(self):
        # self.image = load_image('background.png')
        self.image = load_image('village.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(CANVAS_WIDTH // 2,
                        CANVAS_HEIGHT // 2,
                        CANVAS_WIDTH,
                        CANVAS_HEIGHT)
