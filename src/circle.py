import abstractshape as abs_shp
import cartesian2 as c2
import random 
import math 
import numpy as np 

class Circle(abs_shp.AbstractShape):
    def __init__(self, center_ponint:c2.Cartesian2, radius:float, r_distribution, angle_distribution, clip:bool):
        # r_distribution/angle_distribution = random.uniform(a,b) 
        # r_distribution/angle_distribution = np.random.random_sample() or np.random.binomial() or ...... choose any from numpy 
        self.center_point = center_ponint
        self.radius = radius
        self.r_distribution = r_distribution
        self.angle_distribution = angle_distribution
        self.clip = clip

    @classmethod
    #factory function for standard circle 
    def circle(cls,center_point:c2.Cartesian2, radius:float):
        assert radius >= 0 
        #             using uniform dist choose a val between 0 and radius,  
        return cls(center_point, radius, radius * random.uniform(0,radius), random.uniform(0, 2*math.pi), False)
    
    def getNearestPointOnEdge(self, point:c2.Cartesian2):
        vector = self.center_point - point

        distance_to_center = c2.Cartesian2.__abs__(vector)
        distance_to_edge = distance_to_center - self.radius

        unit_vector = vector * (1/ c2.Cartesian2.__abs__(vector))
        edge_point =  point + unit_vector * distance_to_edge

        return edge_point, distance_to_edge
    
    def samplePoint(self, rng = random.Random(123)): #using a defaut seed of 123, should this be a variable in future while we work with testing the simulator
        r = self.r_distribution # := random.uniform(a,b) choose a random value for radius,r using uniform dist 
        angle = self.angle_distribution #:= random.uniform(a,b) choose a random value for angle using uniform dist

        if self.clip :
            r = np.clip(r, -1 * self.radius, self.radius)
        
        x = r * math.cos(angle)
        y = r * math.sin(angle) 

        return c2.Cartesian2(x+self.center_point.x, y+self.center_point.y) 
    
    #todo need to work with matplotlib, alternative - look for other plotting tools  
    def plotShape(self, ax, color, ls):
        pass

    def getArea (self):
        return math.pi * self.radius**2
    