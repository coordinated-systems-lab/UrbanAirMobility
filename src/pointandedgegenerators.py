import cartesian2 as c2
import numpy as np 
from typing import List

def getLineOfPoints(start:c2.Cartesian2, dest:c2.Cartesian2, number_points, bidirectional:bool, start_index = 0):
    assert number_points >= 0 

    #generate all the points
    xs = list(np.linspace(start.x, dest.x, number_points+2))
    ys = list(np.linspace(start.y, dest.y, number_points+2))

    points:List[c2.Cartesian2] = []
    
    # * edges is a list of Edge, Edge is a datastructure that holds an edge between two vertices. 
    edges = []

    #create points 
    for i in range(len(xs)):
        points.append(c2.Cartesian2(xs[i],ys[i]))

    #create edges
    for i in range(len(xs) - 1):
        current = i + start_index
        next_edge = i + 1 + start_index
        edges.append()