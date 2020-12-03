import random
import time
import math

# Screen shake class used to juice up the game

class ScreenShake:
    def __init__(self, magnitude=0, duration=1, damping=0.1):
        self.magnitude = magnitude
        self.duration = duration
        self.damping = damping
        self.offset = (0, 0)
        self.lifetime = 0

    def shake(self, dt):
        if self.magnitude == 0:
            return (0, 0)
        x_offset = math.cos(random.uniform(0, 2*math.pi)) * self.magnitude
        y_offset = math.sin(random.uniform(0, 2*math.pi)) * self.magnitude
        self.offset = (int(x_offset), int(y_offset))
        self.magnitude *= self.damping
        self.lifetime += dt
        if self.lifetime>=self.duration or self.magnitude == 0:
            self.offset = (0, 0)
        return self.offset
    
    def set_properties(self, magnitude, duration, damping):
        self.magnitude = magnitude
        self.duration = duration
        self.damping = damping
        self.offset = (0, 0)
        self.lifetime = 0
