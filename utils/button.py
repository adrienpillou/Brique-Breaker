from .gameobject import GameObject
import pygame

class Button(GameObject):
    def __init__(self, name, position, size):
        super().__init__(name, position, size)
        self.border = 1
        self.state = "IDLE"
        self.label = ""
        self.solid = False
        self.colors = dict()
        self.colors['IDLE'] = (200, 200, 200)
        self.colors['SELECTED'] = (255, 255, 255)
        self.colors['PRESSED'] = (100, 100, 100)
        self.font_size = 16
        pygame.font.init()
        self.font = pygame.font.Font('freesansbold.ttf', 16)
        

    def set_label(self, label):
        self.label = label
    
    def set_state(self, state):
        self.state = state
        self.color = self.colors[state]
    
    def set_font_size(self, font_size):
        self.font_size = font_size
        self.font = pygame.font.Font('freesansbold.ttf', self.font_size)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.position.x, self.position.y, self.size.x, self.size.y))
        text = self.font.render(self.label, True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (self.position.x + self.size.x//2, self.position.y + self.size.y//2)
        surface.blit(text, text_rect)
