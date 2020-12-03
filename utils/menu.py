import pygame
from .gameobject import GameObject
from .button import Button
from .vector import Vector2

class Menu(GameObject):
    def __init__(self, name, position, size):
        super().__init__(name, position, size)
        self.padding = 4
        self.selection_index = 0
        self.buttons = []
        self.active = True

    def add_button(self, button:Button):
        self.buttons.append(button)

    def update(self):
        pass

    # Receive events from the gameloop            
    def receive_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selection_index-=1
                if self.selection_index < 0:
                    self.selection_index = len(self.buttons)-1
                    
            elif event.key == pygame.K_DOWN:
                self.selection_index+=1
                if self.selection_index >= len(self.buttons):
                    self.selection_index = 0

    def set_layout(self):
        for i, button in enumerate(self.buttons):
            button.set_position(Vector2(self.position.x - button.get_rect().w//2, self.position.y + (i-len(self.buttons)//2) * (button.size.y + self.padding))) 
        pass
    
    # Return selected button name and index
    def get_selection(self):
        return (self.selection_index, self.buttons[self.selection_index].name)

    def draw(self, surface):
        if self.active:
            for i, button in enumerate(self.buttons):
                if i == self.selection_index:
                    button.set_state("SELECTED")
                else :
                    button.set_state("IDLE")
                button.draw(surface)
            pass