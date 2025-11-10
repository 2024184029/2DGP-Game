from pico2d import load_image

class Background:
    def __init__(self):
        self.image = load_image('background.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(512, 512)  # 1024x1024 기준 중심
