#Dependencies Cartesian2, Polar2
from CoordinateSystem import Cartesian2
from CoordinateSystem import Polar2 


def toPolar(a:Cartesian2):
    r  = Cartesian2.abs(a)
    theta = Cartesian2.angle(a)
    return Polar2(r, theta)

def toCartesian(a:Polar2):
    x = Polar2.getX(a)
    y = Polar2.getY(a)
    return Cartesian2(x,y)
