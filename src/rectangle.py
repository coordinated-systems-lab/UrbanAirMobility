from abstractshape import AbstractShape as Absshp
import cartesian2 as c2
import numpy as np 
import math 
import random 
from typing import Generator

class Rectangle(Absshp):
    def __init__(self, top_left: c2.Cartesian2, bottom_right: c2.Cartesian2, x_distribution:float, y_distribution:float, clip:bool):
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.x_distribution = x_distribution #use np.random.uniform()
        self.y_distribution = y_distribution #use np.random.uniform()
        self.clip = clip

    @classmethod
    def rectangle(cls,top_left:c2.Cartesian2, bottom_right:c2.Cartesian2,
                    clip = False):
        x_distribution = np.random.uniform(top_left.x, bottom_right.x)
        y_distribution = np.random.uniform(bottom_right.y, top_left.y)

        assert top_left.x <= bottom_right.x
        assert top_left.y >=bottom_right.y
        
        return cls(top_left, bottom_right,x_distribution,y_distribution,clip)
    
    def getNearestPointOnEdge(self, point:c2.Cartesian2):
        x, y = None, None
        top = self.top_left.y
        bottom = self.bottom_right.y
        left = self.top_left.x 
        right = self.bottom_right.x
        outside = False # whether or not our point is outside the rectangle. Defaults to false. If any dim is outside, then it becomes true.

        # ? refactor with nearest point algorithm, maybe ??
        #find the nearest y value
        if point.x < left:
            x = left
            outside = True
        elif point.x > right:
            x = right
            outside = True
        else:
            x = point.x
        
        #find nearest y value 
        if point.y < bottom:
            y = bottom
            outside = True
        elif point.y > top:
            y = top
            outside = True
        else:
            y = point.y
        
        # special case. If we are inside rectangle in both x and y, then the above didnt work
        if not outside:
            # adjust x,y for inside point. This is kinda complex because we have to calculate triangles from the inside of the rectangle
            vector_back_slash = self.bottom_right - self.top_left # vector that looks like a backslash 
            vector_forward_slash = c2.Cartesian2(right - left, top-bottom)

            #make them unit length
            vector_back_slash = vector_back_slash * (1/c2.Cartesian2.__abs__(vector_back_slash))
            vector_forward_slash = vector_forward_slash * (1/c2.Cartesian2.__abs__(vector_forward_slash))

            #calculate which triangle we are in, refer to diagram at the bottom 
            
            change_x = point.x - left
            y_value_of_slash_by_point = (vector_forward_slash * (point.x / vector_forward_slash.x)).y + bottom
            above_forward_slash = point.y > y_value_of_slash_by_point

            # ? why are we calculating change_x again ????
            change_x = point.x - left
            y_value_of_slash_by_point = (vector_back_slash * (point.x / vector_back_slash.x)).y + top
            above_backward_slash = point.y > y_value_of_slash_by_point

            #now that we know which triangle we are in, can just calculate x,y 
            
            if above_forward_slash and above_backward_slash: #top triangle 
                x = point.x
                y = top
            elif above_forward_slash and (not above_backward_slash):
                x = left
                y = point.y
            elif (not above_forward_slash) and above_backward_slash:
                x = right 
                y = point.y
            else:
                x = point.x
                y = bottom
            
        edge_point = c2.Cartesian2(x,y)
        distance_to_edge = c2.Cartesian2.__abs__(point - edge_point)
        distance_to_edge = distance_to_edge if outside else -distance_to_edge

        return edge_point, distance_to_edge
        
    
    
    def samplePoint(self): 
        #random x and y according to provided distributions, 
        #x_distribution and y_distribution should be something like np.random.uniform()
        x = self.x_distribution
        y = self.y_distribution

        if self.clip:
            x = np.clip(x, self.top_left.x, self.bottom_right.x)
            y = np.clip(y, self.bottom_right.y, self.top_left.y)
        
        return c2.Cartesian2(x, y)
    
    # TODO need to complete writing the method using matplotlib 
    def plotShape(self, ax, color, ls):
        pass

    def getArea(self):
        area = (self.bottom_right.x - self.top_left.x) * (self.top_left.y - self.bottom_right.y)
        return area
    

    #= Diagram for nearest point. Consider the following
    # solid lines are the borders of the rectangle. Dotted lines denote regions of interest where the behavior of nearest point is consistent
    # note the forward and backwards slashes (in dots) inside the rectangle

#         .                     .
#         .                     .
#         .                     .
# ....... ______________________ ...............
#         |  .               .  |
#         |     .         .     |        
#         |         . .         |
#         |         . .         |
#         |      .       .      |
#         |   .             .   |
# ........|_____________________|................
#         .                     .
#         .                     .        
#         .                     .
