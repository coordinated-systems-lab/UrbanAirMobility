import math

class Polar2:
    def __init__(self, r , theta):
        self.r = r
        self.theta = theta
    
    def __add__(self,a):
        new_r = self.r + a.r
        new_theta = self.theta + a.theta
        return Polar2(new_r, new_theta)
    def __sub__(self, a):
        new_r = self.r - a.r
        new_theta = self.theta - a.theta
        return Polar2(new_r, new_theta)
    def __mul__(self,a):
        new_r = self.r * a
        new_theta = self.theta * a
        return Polar2(new_r, new_theta)
    
    def getX(self):
        return self.r * math.cos(self.theta)
    def getY(self):
        return self.r * math.sin(self.theta)
    
    def __str__(self) -> str:
        return 'r = {self.r}, theta={self.theta}'