import abstractshape as abs_shp
import cartesian2 as c2
import numpy as np

class Circle(abs_shp.AbstractShape):
    def __init__(self, center_ponint:c2.Cartesian2, radius:float, r_distribution, angle_distribution, clip:bool):
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
        return cls(center_point, radius, radius * np.random.random_sample(), 2*np.pi * np.random.random_sample(), False)
    
    def getNearestPointOnEdge(self, point:c2.Cartesian2):
        vector = self.center_point - point

        distance_to_center = c2.Cartesian2.__abs__(vector)
        distance_to_edge = distance_to_center - self.radius

        unit_vector = vector * (1/ c2.Cartesian2.__abs__(vector))
        edge_point =  point + unit_vector * distance_to_edge

        return edge_point, distance_to_edge
    
    def samplePoint(self, rng):
        r = self.r_distribution
        angle = self.angle_distribution

        if self.clip :
            
    