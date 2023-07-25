#Dependencies Cartesian2, Polar2
from modules import cartesian2 as c2 
from modules import polar2 as p2 


def toPolar(a:c2.Cartesian2):
    r  = c2.Cartesian2.__abs__(a) # abs definition should have been update in global scope due to dunder methods naming convention, need to investigate further
    theta = c2.Cartesian2.angle(a)
    return p2.Polar2(r, theta)

def toCartesian(a:p2.Polar2):
    x = p2.Polar2.getX(a)
    y = p2.Polar2.getY(a)
    return c2.Cartesian2(x,y)