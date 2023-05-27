import math
#import sys
#sys.path.append(r'/Users/aadit/Development/AAM_AMOD/')


class Cartesian2:
    def __init__(self, x,y):
        self.x = x
        self.y = y
    
    def __add__(self,a):
        new_x = self.x + a.x
        new_y = self.y + a.y
        return Cartesian2(new_x, new_y)
    def __sub__(self, a):
        new_x = self.x - a.x
        new_y = self.y - a.y
        return Cartesian2(new_x, new_y)
    def __mul__(self,a):
        new_x = self.x * a
        new_y = self.y * a
        return Cartesian2(new_x, new_y)
    def __eq__(self, a):
        if self.x == a.x and self.y == a.y:
            return True
    def __abs__(self):
        return (self.x**2 + self.y**2)**0.5
    def angle(self):
        return math.atan((self.y/self.x))
    def __str__(self) -> str:
        return f'x = {self.x}, y={self.y}'
    
    
    
    
            
