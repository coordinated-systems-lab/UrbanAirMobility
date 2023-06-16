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
        edges.append((current, next_edge))
        if bidirectional:
            edges.append((next_edge, current))

    return points, edges

# a convenience function that returns a circle of points that are connected. 
# optionally connected in both directions, defaults to false

def gitCircleOfPoints(center_point:c2.Cartesian2, radius:float, number_points:int, connected_clockwise:bool, connected_counter_clockwise:bool, start_index:int = 0):
    assert number_points > 0
    assert (connected_clockwise or connected_counter_clockwise)

    #generate all the points, evenly distributed
    thetas = np.linspace(0, 2*np.pi,number_points+1)
    thetas = thetas[:-1]

    points = []
    edges = []

    for i in range(len(thetas)):
        x = radius * np.cos(thetas[i])
        y = radius * np.sin(thetas[i])
        points.append(c2.Cartesian2(x,y)+center_point)

    #create edges 
    number_points = len(points)
    for i in range(number_points):
        current_edge = i + start_index
        next_edge = 1 if (i+1) > number_points else i+1
        next_edge += start_index

        if connected_counter_clockwise:
            edges.append((current_edge, next_edge))
        if connected_clockwise:
            edges.append((next_edge, current_edge))
    
    return points, edges

#a convenience function that returns a rectangle of points that are connected.
#note the number of rows and cols is inside the rectangle, ie if they are 0, this will generate the outside edge
#every row/col is 1-directional, alternates which direction

def getRectangleOfPoints(top_left:c2.Cartesian2, bottom_right:c2.Cartesian2, number_rows:int, number_cols:int, start_index: int= 0):
    assert (number_rows >= 0 and number_cols >= 0)
    assert (number_rows % 2 == 0 and number_cols % 2 == 0)

    #generate all the points, evenly distributed 
    points = []
    edges = []

    xs = np.linspace(top_left.x, bottom_right.x, number_cols+2)
    ys = np.linspace(bottom_right.y, top_left.y, number_rows+2)

    #create points 
    for y in ys:
        for x in xs:
            points.append(c2.Cartesian2(x,y))
    
    #create edge
    for row in range(number_rows+2):
        for col in range(number_cols+2):

            #find index of current point. This function may not be only points in list,
            #so add start index also.
            this_index = start_index + col + (row-1)*(number_cols + 2)

            #add direction based on row index
            if (row % 2 == 0) and (col != 1):
                edges.append((this_index, this_index-1))
            elif (row % 2 == 1) and (col != number_cols + 2):
                edges.append((this_index, this_index+1))

            #add direction based on col index

            if (col % 2 == 0) and (row != number_rows + 2):
                edges.append((this_index, this_index + number_cols + 2))
            elif (col%2 == 1) and (row!=1):
                edges.append((this_index, this_index - number_cols + 2))
    
    return points, edges
