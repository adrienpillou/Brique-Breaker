import time
import pygame
import random
import math
from .gameobject import GameObject

class CircleEmitter(GameObject):
    def __init__(self, name, position, lifetime, amount, bursts, rate):
        super().__init__(name, position, (0,0))
        self.position = position
        self.lifetime = lifetime
        self.amount = amount
        self.bursts = bursts
        self.created_particles = 0
        self.rate = rate
        self.particles = []
        self.can_emit = True
        self.last_emit = 0
        self.dt = 1/60
        self.base_color = (255, 255, 255)
        self.base_size = 6
        self.base_lifetime = 10

    def emit(self):
        if self.created_particles >= self.bursts and self.bursts!=-1:
            self.can_emit = False
        if self.can_emit:
            self.can_emit = False
            for i in range(self.amount):
                self.particles.append(Particle(
                    self.position,
                    self.base_color,
                    self.base_lifetime,
                    self.base_size + random.uniform(-1, 1)
                ))
            self.created_particles += 1
            self.last_emit = time.time()

    def draw(self, surface):
        if self.lifetime >= 0 and self.lifetime != -1:
            self.lifetime -= self.dt
        self.emit()
        if not self.can_emit and (time.time() > self.last_emit + self.rate):
            self.can_emit = True
        for particle in self.particles:
            particle.update(self.dt)
            particle.draw(surface)
            if particle.lifetime <= 0:
                self.particles.remove(particle)

    def is_emitting(self):
        if self.lifetime == -1 or self.lifetime>0:
            return True
        return False
        
class Particle():
    def __init__(self, position, color, base_lifetime, size):
        self.position = position
        self.color = color
        self.base_lifetime = base_lifetime
        self.lifetime = base_lifetime
        self.size = size

    def update(self, dt):
        if self.lifetime >= 0:
            self.lifetime -= dt
            lifetime_factor = self.lifetime/self.base_lifetime
            if(lifetime_factor>=0):
                self.size *= 1+lifetime_factor*.25
        else : self.lifetime = 0
        
        if(self.size > 256 ):
            self.lifetime = 0

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.position, int(self.size), 1)