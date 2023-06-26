import numpy as np
import random
from typing import List, Tuple
from matplotlib import pyplot as plt
import abstractspawncontroller as abscntl
import shapemanager as shpmng
import cartesian2 as c2
import helpers
import aircraft as acft
import circle, rectangle


class QueuedSpawnController(abscntl.AbstractSpawnController):
    def __init__(
        self,
        sources: shpmng.ShapeManger,
        destinations: shpmng.ShapeManger,
        queues: List[int] | np.ndarray,
        spawnrate_per_second,
        relative_destination: bool,
    ):
        self.sources = sources
        self.destinations = destinations
        self.queues = queues
        self.spawnrate_per_second = spawnrate_per_second
        self.relative_destination = relative_destination

    @classmethod
    def queuedspawncontroller(
        cls,
        sources: shpmng.ShapeManger,
        destinations: shpmng.ShapeManger,
        spawns_per_km_squared_hours,
        relative_destination: bool,
    ):
        spawns_per_seconds = (
            helpers.km_sq_hrs_to_m_sq_secs(spawns_per_km_squared_hours)
            * sources.getArea()
        )
        queues = np.zeros(len(sources.shapes))

        return cls(
            sources, destinations, queues, spawns_per_seconds, relative_destination
        )

    def getSourceAndDestinations(
        self, timestep, current_time, aircraft, ego_position, rng=random.Random(123)
    ) -> List[Tuple[c2.Cartesian2, c2.Cartesian2]]:  # type: ignore
        # find how many to spawn this timestep
        ac_to_spawn = helpers.makeInt(self.spawnrate_per_second * timestep)
        #! debugging statement - comment later
        # print('number of aircrafts to spawn: ', ac_to_spawn)
        ret = []

        # randomly add to queues based on priorities given in shape manager
        for i in range(ac_to_spawn):
            index = self.sources.sampleShapeIndex()
            #! debugging statement - comment later
            # print('value of index: ', index)
            self.queues[index] += 1

        # try to pull from queues based on if there is anyone around
        for i in range(len(self.queues)):
            if self.queues[i] == 0:
                continue

            # sample starting point from the shape at this index
            # this will be where the person in queue spawns
            start = self.sources.samplePoint(rng.random()) + ego_position

            # verify there is no immediate NMAC
            if not (self.isAirspaceClear(start, aircraft)):
                # print('Failed to spawn', start,' because there is an ac')   #! this line is commented in julia code
                continue

            destination = self.destinations.samplePoint(rng.random())
            if self.relative_destination:
                destination += start

            # add to list, decrement queue
            ret.append((start, destination))
            self.queues[i] -= 1

        return ret

    def setSpawnRate(self, spawns_per_km_squared_hours):
        spawn_rate_per_second = (
            helpers.km_sq_hrs_to_m_sq_secs(spawns_per_km_squared_hours)
            * self.sources.getArea()
        )

    def isAirspaceClear(self, point: c2.Cartesian2, ac: List[acft.Aircraft]):
        for plane in ac:
            if c2.Cartesian2.__abs__(plane.dynamic.position - point) < 150:
                return False
        return True

    def render(self, ax):
        # render the source and destination
        # TODO - need to find how these renders are working
        self.render(self.sources, ax, "g", ":")  # type:ignore
        self.render(self.destinations, ax, "b", ":")  # type:ignore

        # render queue counts
        for i in range(len(self.sources.shapes)):
            if type(self.sources.shapes[i]) == circle.Circle:
                x = self.sources.shapes[i].center_point.x  # type: ignore
                y = self.sources.shapes[i].center_point.y + self.sources.shapes[i].radius  # type: ignore
                s = str(self.queues[i])
                plt.text(x, y, s)
            elif self.sources.shapes[i] == rectangle.Rectangle:
                x = self.sources.shapes[i].top_left.x - 10  # type:ignore
                y = self.sources.shapes[i].bottom_right.y + 10  # type:ignore
                s = str(self.queues[i])
                plt.text(x, y, s)

            else:
                # TODO any other shape
                print("Shape not supported for queue rendering")
