# depends on cartesian 2

# the following struct serves as a placeholder for what a shape should look like
# it must have the below methods defined
# Additionally, it must define the following:
#   Relevant geometry - position, size, etc
#   Sampling distributions - potentially 2 such as x,y or radius, angle
#   Clip = a bool of whether a sampled point is clipped to gurantee it is within the shape or not
#       For example, a standard normal distribution may be the internal sampling distribution, which can technically output a point from -inf to inf.
#       Therefore, we may want to clip the points to always be within the shape
from abc import abstractmethod, ABC
from typing import Tuple
import cartesian2 as c2 
class AbstractShape(ABC):

    



    # This function finds the nearest point to "point" along the edge of the shape s. 
    # it also returns the distance from that point to the nearest point. If the point is outside the shape, the distance is positive
    # if the point is inside the shape, the distance is negative

    @abstractmethod
    def getNearestPointOnEdge(self,point,) -> Tuple: # ? what are the implications of expecting a tuple output 
        pass


    # This function samples a point from the shape randomly. The internal distribution should be specified in the constructor of a given shape
    # this should return a Cartesian2 point
    # any randomness must use the RNG
    # clip if Clip == true
    @abstractmethod
    def samplePoint(self, rng,) -> c2.Cartesian2:
        pass


    # this function should use pyplot to plot the shape
    # ax = the graph, look at other examples its complicated
    # color = string such as "r", "g", see pyplot examples
    # ls = line shape, such as "-", "--", ":", etc. see pyplot
    @abstractmethod
    def plotShape(self, ax, color, ls,):
        pass

    # this function returns the area of the shape.
    # if the shape does not have a fixed border (IE for a gaussian distribution which can in theory return a point anywhere between -inf and inf)
    # Then decide on a relevant size. Such as the area of which 95% of spawns will be or something like this

    @abstractmethod
    def getArea(self):
        pass