# Dependencies: Cartesian2, Polar2, ConvertCoordinateSystem, Dynamics, Aircraft
from abc import abstractmethod, ABC
from typing import List, Tuple
import cartesian2 as c2

class AbstractSpawnController(ABC):
    
    
    # must return a vector of Tuple of cartesian 2 points
    @abstractmethod
    def getSourceAndDestinations(self, timestep, current_time, aircraft, ego_position, rng,) -> List[Tuple[c2.Cartesian2, c2.Cartesian2]]:
        pass 

    @abstractmethod
    def setSpawnRate(self, spawns_per_km_squared_hours,):
        pass

    @abstractmethod
    def render(self, ax, *args):
        pass

    