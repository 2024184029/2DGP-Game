from pico2d import load_image
import game_world
from state_machine import StateMachine
import random
from random import randint

class Zombie:
    FRAME_COLS = 4
    FRAME_ROWS = 4
    SPEED = 0.03

    def __init__(self):
        self.image = load_image('zombie.png')
        self.frame = 0
        self.x, self.y = randint(500, 500), randint(100, 500)

    def enter(self):
        pass

    def update(self):
        self.x += self.SPEED
        self.frame = (self.frame + 1) % (Zombie.FRAME_COLS * Zombie.FRAME_ROWS)

    def draw(self):
        col = self.frame % Zombie.FRAME_COLS
        row = self.frame // Zombie.FRAME_COLS
        self.image.clip_draw(col * 100, row * 200, 100, 200, self.x, self.y)

