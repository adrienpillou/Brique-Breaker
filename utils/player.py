from .gameobject import GameObject
import pygame

class Player(GameObject):
    def __init__(self, name, position, size):
        super().__init__(name, position, size)
        self.can_move = True
        self.speed = 16
