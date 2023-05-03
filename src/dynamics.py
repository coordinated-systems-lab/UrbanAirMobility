import math

class Dynamics:
    def __init__(self, position, velocity, acceleration):
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration

    def setacceleration(self,a):
        self.acceleration = a
    
    def step(self, timestep, max_speed = float('inf')):
        self.velocity += self.acceleration * timestep

        if self.velocity > max_speed:
            self.velocity = max_speed
        
        if self.velocity.r < 0.0:
            self.velocity.r = -self.velocity.r
            self.velocity.theta = self.velocity.theta - math.pi

        self.position += toCartesian(self.velocity) * timestep

    def __str__(self):
        return f'Pos {self.position}, Vel {self.velocity}, Acceleration {self.acceleration}'
    
        