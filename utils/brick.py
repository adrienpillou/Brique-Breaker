import pygame
from .gameobject import GameObject
from .tweenease import *

class Brick(GameObject):
    def __init__(self, name, position, size, lives = 1):
        super().__init__(name, position, size)
        self.lives = lives
        self.color = (216, 140, 36)
        self.tween = Tween(1, EaseType.easeinquart)
        self.hitted = False

    def set_lives(self, lives):
        self.lives = lives
        if self.lives == 1:
            self.color = (66, 133, 244)
        elif self.lives == 2:
            self.color = (219, 68, 55)
        elif self.lives == 3:
            self.color = (244, 180, 0)
        elif self.lives == 4:
            self.color = (15, 157, 88)
        elif self.lives == 5:
            self.color = (101, 101, 101)
        else:
            self.color = (255, 255, 255)

    def update(self):
        pass