import time
import pygame
import random
from .gameobject import GameObject

class Emitter(GameObject):
    def __init__(self, name, position, lifetime, amount, rate):
        super().__init__(name, position, (0,0))
        self.position = position
        self.lifetime = lifetime
        self.amount = amount
        self.created_particles = 0
        self.rate = rate
        self.particles = []
        self.can_emit = True
        self.last_emit = 0
        self.dt = 1/60
        self.gravity = (0, 0)
    
    def emit(self):
        if self.created_particles >= self.amount:
            self.can_emit = False
        if self.can_emit:
            self.can_emit = False
            for i in range(self.amount):
                self.particles.append(Particle(self.position, (255,255,255), (random.uniform(-1, 1), random.uniform(-1,1)), 5, self.gravity,random.randint(2, 12)))
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
    
    def set_gravity_modifier(self, gravity:tuple):
        self.gravity = gravity

    def is_emitting(self):
        if self.lifetime == -1 or self.lifetime>0:
            return True
        return False
        
class Particle():
    def __init__(self, position, color, velocity, lifetime, gravity_modifier, size):
        self.position = position
        self.color = color
        self.velocity = velocity
        self.lifetime = lifetime
        self.size = size
        self.gravity_modifier = gravity_modifier
        self.alpha = 10

    def update(self, dt):
        if self.lifetime >= 0:
            self.lifetime -= dt
        else : self.lifetime = 0
        self.position = (self.position[0] + self.velocity[0] + self.gravity_modifier[0] , self.position[1] + self.velocity[1] + self.gravity_modifier[1])
        
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.position[0], self.position[1], self.size, self.size))
        