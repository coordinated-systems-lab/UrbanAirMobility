# Dependencies: Cartesian2, Polar2, ConvertCoordinateSystem, Dynamics, Aircraft
from abc import abstractmethod, ABC
from typing import List

class AbstractSpawnController(ABC):
    
    
    # must return a vector of Tuple of cartesian 2 points
    @abstractmethod
    def getSourceAndDestinations(self, timestep, current_time, aircreaft, ego_position, rng,) -> List[object]:
        pass 

    @abstractmethod
    def setSpawnRate(self, spawns_per_km_squared_hours,):
        pass

    @abstractmethod
    def render(self, ax,):
        pass

    