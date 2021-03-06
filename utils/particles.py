import time
import pygame
import random
import math
from .gameobject import GameObject

class Emitter(GameObject):
    def __init__(self, name, position, lifetime, amount, bursts, rate):
        super().__init__(name, position, (0,0))
        self.position = position
        self.lifetime = lifetime
        self.amount = amount
        self.bursts = bursts
        self.created_bursts = 0
        self.rate = rate
        self.particles = []
        self.can_emit = True
        self.last_emit = 0
        self.dt = 1/60
        self.gravity = (0, 1)
        self.base_velocity = (0, 0)
        self.base_color = (255, 255, 255)
        self.base_size = 16
        self.base_lifetime = 5

    def emit(self):
        if self.created_bursts >= self.bursts:
            self.can_emit = False
        if self.can_emit:
            self.can_emit = False
            for i in range(self.amount):
                self.particles.append(Particle(
                    self.position,
                    self.base_color,
                    (8*math.cos(random.uniform(0, 2*math.pi)), 8*math.sin(random.uniform(0, 2*math.pi))),
                    self.base_lifetime + random.uniform(-self.base_lifetime, self.base_lifetime),
                    self.gravity,
                    self.base_size + random.uniform(0, self.base_size/4)
                ))
            self.created_bursts += 1
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

    def set_gravity_modifier(self, gravity:tuple):
        self.gravity = gravity

    def is_emitting(self):
        if self.lifetime == -1 or self.lifetime>0:
            return True
        return False
        
class Particle():
    def __init__(self, position, color, velocity, base_lifetime, gravity_modifier, size):
        self.position = position
        self.color = color
        self.velocity = velocity
        self.base_lifetime = base_lifetime
        self.lifetime = base_lifetime
        self.size = size
        self.gravity_modifier = gravity_modifier
        self.alpha = 10

    def update(self, dt):
        if self.lifetime >= 0:
            self.lifetime -= dt
            lifetime_factor = self.lifetime/self.base_lifetime
            if(lifetime_factor>=0):self.size *= lifetime_factor
        else : self.lifetime = 0
        
        if(self.size < 1 ):
            self.lifetime = 0
        self.gravity_modifier = (self.gravity_modifier[0]*(1+dt), self.gravity_modifier[1]*(1+dt))
        self.position = (self.position[0] + self.velocity[0]*lifetime_factor + self.gravity_modifier[0] , self.position[1] + self.velocity[1]*lifetime_factor + self.gravity_modifier[1])

    def draw(self, surface):
        pygame.draw.rect(surface, (30, 30, 30), (self.position[0]+6, self.position[1]+6, self.size, self.size))
        pygame.draw.rect(surface, self.color, (self.position[0], self.position[1], self.size, self.size))
        