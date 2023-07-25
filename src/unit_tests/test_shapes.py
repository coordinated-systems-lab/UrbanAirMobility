import math
import circle
import rectangle
import cartesian2 as c2

c = circle.Circle.circle(c2.Cartesian2(0,0), 1)

some_point = c2.Cartesian2(-5,0)
nearest, distance = c.getNearestPointOnEdge(some_point)
assert nearest == c2.Cartesian2(-1,0)
assert distance == 4

some_point = c2.Cartesian2(5,0)
nearest, distance = c.getNearestPointOnEdge(some_point)
assert nearest == c2.Cartesian2(1,0)
assert distance == 4 

some_point = c2.Cartesian2(0,-5)
nearest, distance = c.getNearestPointOnEdge(some_point)
assert nearest == c2.Cartesian2(0,-1)
assert distance == 4

some_point = c2.Cartesian2(0,5)
nearest, distance = c.getNearestPointOnEdge(some_point)
assert nearest == c2.Cartesian2(0,1)
assert distance == 4 

some_point = c2.Cartesian2(5,5)
nearest, distance = c.getNearestPointOnEdge(some_point)
assert nearest.x - math.sqrt(2)/2 < 0.000001
assert nearest.y - math.sqrt(2)/2 < 0.000001
assert distance == math.sqrt(5**2 + 5**2) -1

print('sample point using samplePoint method -> ', c.samplePoint())

#test 2 - rectangle 
r = rectangle.Rectangle.rectangle(c2.Cartesian2(0,1), c2.Cartesian2(1,0))

some_point = c2.Cartesian2(-5,0)
nearest, distance = r.getNearestPointOnEdge(some_point)
assert nearest == c2.Cartesian2(0,0)
assert distance == 5

some_point = c2.Cartesian2(5,0)
nearest, distance = r.getNearestPointOnEdge(some_point)
assert nearest == c2.Cartesian2(1,0)
assert distance == 4

some_point = c2.Cartesian2(5,5)
nearest, distance = r.getNearestPointOnEdge(some_point)
assert nearest == c2.Cartesian2(1,1)
assert distance == math.sqrt(4**2 + 4**2)

some_point = c2.Cartesian2(0.5, 5)
nearest, distance = r.getNearestPointOnEdge(some_point)
assert nearest == c2.Cartesian2(0.5, 1)
assert distance == 4

some_point = c2.Cartesian2(0.25,0.5)
nearest, distance = r.getNearestPointOnEdge(some_point)
assert nearest == c2.Cartesian2(0,0.5)
assert distance == -0.25

some_point = c2.Cartesian2(0.75, 0.5)
nearest, distance = r.getNearestPointOnEdge(some_point)
assert nearest == c2.Cartesian2(1,0.5)
assert distance == -0.25

some_point = c2.Cartesian2(0.5, 0.75) # in left triangle of the rectangle
nearest, distance =  r.getNearestPointOnEdge(some_point) 
assert nearest == c2.Cartesian2(0.5, 1.0)
assert distance ==  -0.25

some_point = c2.Cartesian2(0.25, 0.5) # in left triangle of the rectangle
nearest, distance =  r.getNearestPointOnEdge(some_point) 
assert nearest == c2.Cartesian2(0, 0.5)
assert distance ==  -0.25

print('sample point using samplePoint method -> ', r.samplePoint())