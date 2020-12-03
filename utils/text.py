from .gameobject import GameObject
from .vector import Vector2
import pygame

# Text Gameobject class made for GUI

class Text(GameObject):
    def __init__(self, name, position, text, font_size = 12):
        super().__init__(name, position, (8,8))
        self.text = text
        self.font = None
        self.antialias = True

    def set_text(self, text):
        self.text = text

    def set_color(self, color):
        self.color = color

    def set_font_size(self, font_size):
        self.font.font_size = font_size

    def set_font(self, font):
        self.font = font

    def draw(self, surface):
        text_image = self.font.get_font().render(self.text, self.antialias, self.color)
        text_rect = text_image.get_rect()
        if(isinstance(self.position, tuple)):
            text_rect.center = (self.position[0], self.position[1])
        elif (isinstance(self.position, Vector2)):
            text_rect.center = (self.position.x, self.position.y)
        surface.blit(text_image, text_rect)