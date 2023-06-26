import shapemanager as sman
import circle
import rectangle
import cartesian2 as c2


sm = sman.ShapeManger.shapemanager()

c = circle.Circle.circle(c2.Cartesian2(0,0), 1)
r = rectangle.Rectangle.rectangle(c2.Cartesian2(5,1),c2.Cartesian2(6,0))

sm.addShape(c, 10)
sm.addShape(r, 1)

point, distance = sm.getNearestPointOnEdge(c2.Cartesian2(-5,0))
assert point == c2.Cartesian2(-1,0)
assert distance == 4

point, distance = sm.getNearestPointOnEdge(c2.Cartesian2(10,0))
assert point == c2.Cartesian2(6,0)
assert distance == 4

for _ in range(4):
    print('sampling a point using shape manager method - samplePoint; output -> ', sm.samplePoint())

#* since circle is given higher weight it is choosen as the shape to be sampled from relatively more

print('Passed shapemanager test')