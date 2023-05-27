from cartesian2 import Cartesian2 as C2
from abstractshape import AbstractShape as AbsShp 
from circle import Circle as Circ
from rectangle import Rectangle as Rect
from typing import List, Generator
import math
import random
class ShapeManger:
    def __init__(self, shapes:List[*AbsShp], weights:List[float], total_area:float):
        self.shapes = shapes
        self.weights = weights 
        self.total_area = total_area
    
    @classmethod
    def shapemanager(cls):
        return cls([],[],0)
    
    def addShape(self, s:AbsShp, weight:float = 1):
        self.shapes.append(s)
        self.weights.append(weight)
        self.total_area += getArea(s)
    
    # TODO Need to change the name of this method, it causes ambiguity within code and does not explain what this method does
    def getNearestPointOnEdge(self, shapes:List[*AbsShp], point:C2):
        nearest_point = object()  
        best_distance: C2 | float = math.inf

        if self != object:
            for shape in shapes:
                some_point, some_distance = shape.getNearestPointOnEdge(point) # ? need to confirm if this will work -> needs unit test, also need to see the implication of changing the abstract class method definition
                if C2.__abs__(some_distance) < abs(best_distance) :
                    nearest_point = some_point
                    best_distance = some_distance
        return nearest_point, best_distance
    
    def samplePoint(self, rng:Generator):
        if len(self.shapes) == 0:
            raise RuntimeError ('NO shapes to sample from')
        
        some_shape = random.choice(self.shapes)



    