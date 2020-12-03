import pygame
from .vector import Vector2

# GameObject base class

class GameObject():
    def __init__(self, name, position, size):
        self.name = name
        self.position = Vector2(position[0], position[1])
        self.sprites = []
        self.frame_index = 0
        self.size = Vector2(size[0], size[1])
        self.tag = ""
        self.color = (255, 255, 255)
        self.solid = True
        self.z_order = 0

    def __repr__(self):
        return f"GameObject {self.name}"

    def get_rect(self):
        return pygame.Rect(self.position.x, self.position.y, self.size.x, self.size.y)

    def set_tag(self, tag:str):
        self.tag = tag

    def set_size(self, size):
        self.size = size

    def set_position(self, position):
        self.position = position

    def add_sprite(self, sprite):
        self.sprites.append(sprite)

    def set_frame_index(self, index):
        self.frame_index = index

    def is_solid(self):
        return self.solid
    
    def update(self):
        pass

    def set_z_order(self, z_order):
        self.z_order = z_order
        pass

    def draw(self, surface):
        pygame.draw.rect(surface, (15, 15, 15), (self.position.x+6, self.position.y+6, self.size.x, self.size.y)) # Drop shadow
        pygame.draw.rect(surface, self.color ,self.get_rect())
        pass

    def tint(self, color):
        mask = pygame.surface.Surface(self.sprites[self.frame_index].get_size())
        mask.fill(color)
        self.sprites[self.frame_index].blit(mask, (0, 0), special_flags = pygame.BLEND_RGBA_MULT)

