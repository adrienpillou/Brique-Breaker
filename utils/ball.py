from .gameobject import GameObject
from .vector import Vector2
import pygame

class Ball(GameObject):
    def __init__(self, name, position, size):
        super().__init__(name, position, size)
        self.velocity = Vector2(0, 0)
        self.speed = 8

    def draw(self, surface):
        pygame.draw.rect(surface, (15, 15, 15), (self.position.x+6, self.position.y+6, self.size.x, self.size.y))
        pygame.draw.rect(surface, self.color, (self.position.x, self.position.y, self.size.x, self.size.y))
        

    def update(self):
        self.position += self.velocity*self.speed
        self.position = Vector2(int(self.position.x), int(self.position.y))