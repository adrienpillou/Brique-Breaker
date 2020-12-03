import pygame

# Font class used by GUI GameObjects

class Font():
    def __init__(self, resource, size):
        self.resource = resource # .ttf font file
        self.size = size # font size
        self.font = None # Pygame font object
        self.load()

    # Load a font file using it's path
    def load(self, resource=""):
        if resource != "":
            self.resource = resource
        self.font = pygame.font.Font(self.resource, self.size)
    
    # Resize the font object 
    def resize(self, size):
        self.size = size
        self.load()
    
    # Return '.ttf' file path
    def get_ressource(self):
        return self.resource
    
    # Return Pygame font object
    def get_font(self):
        return self.font
