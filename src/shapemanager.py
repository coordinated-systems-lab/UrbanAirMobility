from cartesian2 import Cartesian2 as C2
from abstractshape import AbstractShape as AbsShp 
from circle import Circle as Circ
from rectangle import Rectangle as Rect
from typing import List, Tuple
import math
import random
import numpy as np
class ShapeManger:
    def __init__(self, shapes:List[AbsShp], weights:List[float], total_area:float):
        self.shapes = shapes
        self.weights = weights 
        self.total_area = total_area


    
    @classmethod
    def shapemanager(cls):
        return cls([],[],0)
    
    def addShape(self, s:AbsShp, weight:float = 1):
        self.shapes.append(s)
        self.weights.append(weight)
        self.total_area += s.getArea()
    
    def getNearestPointOnEdge(self, point:C2) -> Tuple[C2, float] :
        nearest_point:C2 = C2(0, 0)  
        best_distance:float = math.inf

        if self != object:
            for shape in self.shapes:
                some_point, some_distance = shape.getNearestPointOnEdge(point) 
                if C2.__abs__(some_distance) < abs(best_distance) :
                    nearest_point = some_point
                    best_distance = some_distance
        return nearest_point, best_distance
    
    def samplePoint(self, rng):
        if len(self.shapes) == 0:
            raise RuntimeError ('NO shapes to sample from')
                    
        some_shape:AbsShp = random.choices(self.shapes, self.weights) #type: ignore 

        # * should we provide a default seed value to reduce variablity in the code during code tests/ unit test
        return some_shape.samplePoint(rng=np.random.uniform()) 
    
    def sampleShapeIndex(self, rng = np.random.default_rng()):
        if len(self.shapes) == 0:
            raise RuntimeError ('NO shapes to sample from')
        
        index = random.choices(self.weights)
        return index
    
    def isEmpty(self,):
        return len(self.shapes) == 0
    
    def getArea(self,):
        return self.total_area
    
    # this function should use pyplot to plot the shape
# ax = the graph, look at other examples its complicated
# color = string such as "r", "g", see pyplot examples
# ls = line shape, such as "-", "--", ":", etc. see pyplot

    def render(self, ax, color,ls):
        for shape in self.shapes:
            shape.plotShape(ax,color,ls)

    


    





    