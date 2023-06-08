import math
import src.cartesian2 as c2 
import src.polar2 as p2 
import src.convertcoordinatesystem as ccs

class Dynamics:
    def __init__(self,
                 position:c2.Cartesian2,
                 velocity:p2.Polar2,
                 acceleration:p2.Polar2):
        self.position:c2.Cartesian2 = position
        self.velocity:p2.Polar2 = velocity
        self.acceleration:p2.Polar2 = acceleration

    def setacceleration(self, a:p2.Polar2):
        self.acceleration = a
    
    def step(self, timestep, max_speed = float('inf')):
        self.velocity.r += self.acceleration.r * timestep

        if self.velocity.r > max_speed:
            self.velocity.r = max_speed
        
        if self.velocity.r < 0.0:
            self.velocity.r = -self.velocity.r
            self.velocity.theta = self.velocity.theta - math.pi

        self.position += ccs.toCartesian(self.velocity) * timestep

    def __str__(self):
        return f'Pos {self.position}, Vel {self.velocity}, Acceleration {self.acceleration}'
    
        