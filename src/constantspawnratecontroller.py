import shapemanager as sm, cartesian2 as c2, circle as cir, rectangle as rect, abstractspawncontroller as abs_spwn_ctrlr, aircraft as acft, helpers
from typing import List, Generator, Tuple
import random
import numpy as np

class ConstantSpawnRateController():
    def __init__(self, sources:sm.ShapeManger, 
                 destinations:sm.ShapeManger,
                 spawnrate_per_second:float,
                 relative_destination:bool):
        self.sources = sources
        self.destinations = destinations
        self.spawnrate_per_second = spawnrate_per_second
        self.relative_destination = relative_destination

    @classmethod 
    def constantspawnratecontroller(cls,
                                    boundary: c2.Cartesian2,
                                    is_mdp: bool,
                                    spawns_per_km_sq_hrs: float = 50.0):
        sources = sm.ShapeManger.shapemanager()
        destinations = sm.ShapeManger.shapemanager()

        if is_mdp:
            sources.addShape(cir.Circle.circle(c2.Cartesian2(0,0),1000,r_dist=random.uniform(150,1000)))
            destinations.addShape(cir.Circle.circle(c2.Cartesian2(0,0),2000,r_dist=random.uniform(150,1000))) 
        else:
            sources.addShape(rect.Rectangle.rectangle(c2.Cartesian2(0,boundary.y),c2.Cartesian2(boundary.x, 0)))
            destinations.addShape(rect.Rectangle.rectangle(c2.Cartesian2(0, boundary.y),c2.Cartesian2(boundary.x, 0)))
        return cls(sources, destinations, spawns_per_km_sq_hrs, relative_destination = is_mdp)
    
    @classmethod
    def constantspawnratecontroller_1(cls, sources:sm.ShapeManger, destinations:sm.ShapeManger, spawns_per_km_squared_hours:float, relative_destination:bool):
        spawns_per_meter_squared_seconds = helpers.km_sq_hrs_to_m_sq_secs(spawns_per_km_squared_hours)
        spawns_per_seconds = spawns_per_meter_squared_seconds * sources.getArea()
        return cls(sources, destinations, spawns_per_seconds, relative_destination)
    
        
    def getSourceandDestinations(self, 
                                    timestep,
                                    current_time,
                                    aircraft:List[acft.Aircraft],
                                    ego_position:c2.Cartesian2,
                                    rng = np.random.default_rng()):
        ac_to_spawn = int(self.spawnrate_per_second * timestep)  

        ret :List[Tuple[c2.Cartesian2, c2.Cartesian2]] = []

        for i in range(ac_to_spawn):
            start = self.sources.samplePoint(rng) + ego_position
            destination = self.destinations.samplePoint(rng)

            if self.relative_destination:
                destination += start 
            ret.append((start, destination))
        return ret
    
    def setSpawnRate(self, spawns_per_km_squared_hours):
        spawns_per_meter_squared_seconds = helpers.km_sq_hrs_to_m_sq_secs(spawns_per_km_squared_hours) 
        spawns_per_second = spawns_per_meter_squared_seconds * self.sources.getArea()
        self.spawnrate_per_second = spawns_per_second

    def render(self, ax):
        self.sources.render(ax,'g',':')
        self.destinations.render(ax,'b',':')
    