from typing import List, Tuple
import numpy as np
from matplotlib import pyplot as plt
import random
import abstractspawncontroller as absspwnctrl
import aircraft as ac
import shapemanager as shpmng
import cartesian2 as c2
import circle, rectangle
import helpers


class QueuedAndTimedSpawnController(absspwnctrl.AbstractSpawnController):
    def __init__(
        self,
        sources: shpmng.ShapeManger,
        source_priority_functions: List,
        destinations: shpmng.ShapeManger,
        destination_priority_functions: List,
        queues: np.ndarray,
        spawnrate_per_second: float,
        relative_destination: bool,
    ):
        self.sources = sources
        self.source_priority_functions = source_priority_functions
        self.destinations = destinations
        self.destination_priority_functions = destination_priority_functions
        self.queues = queues
        self.spawnrate_per_second = spawnrate_per_second
        self.relative_destination = relative_destination

    @classmethod
    def queuedandtimedspawncontroller(
        cls,
        sources: shpmng.ShapeManger,
        source_priority_functions: List,
        destinations: shpmng.ShapeManger,
        destination_priority_functions: List,
        spawns_per_km_squared_hours: float,
        relative_destination: bool,
    ):
        spawns_per_meter_squared_seconds = helpers.km_sq_hrs_to_m_sq_secs(
            spawns_per_km_squared_hours
        )
        spawns_per_seconds = (
            spawns_per_meter_squared_seconds * sources.getArea()
        )  # TODO rename to spawns_per_second
        queues = np.zeros(shape=len(sources.shapes))

        return cls(
            sources,
            source_priority_functions,
            destinations,
            destination_priority_functions,
            queues,
            spawns_per_seconds,
            relative_destination,
        )

    # must return a vector of Tuple of cartesian 2 points
    def getSourceAndDestinations(
        self, timestep, current_time, aircraft, ego_position, rng=random.Random(123)
    ) -> List[Tuple[c2.Cartesian2, c2.Cartesian2]]:
        ac_to_spawn = helpers.makeInt(self.spawnrate_per_second * timestep)
        ret = []

        src_weights = []
        dest_weights = []

        for f in self.source_priority_functions:
            src_weights.append(f(current_time))

        for f in self.destination_priority_functions:
            dest_weights.append(f(current_time))

        # randomly add to queues based on priorities given in shape manager
        for i in range(ac_to_spawn):
            index = random.choice(src_weights)
            self.queues[index] += 1

        # try to pull from queues based on if there is anyone around
        for i in range(len(self.queues)):
            # if no one in queue, skip
            if self.queues[i] == 0:
                continue
            # sample starting point from the shape at this index
            # this will be where the person in queue spawns

            start = self.sources.shapes[i].samplePoint(rng) + ego_position

            # verify there is no immediate NMAC
            if not (self.isAirspaceClear):
                # print('failed to spawn ', start, ' because there is an ac' )
                continue

            # if not, then find their destination
            dest_index = random.choice(dest_weights)
            destination = self.destinations.shapes[dest_index].samplePoint()

            if self.relative_destination:
                destination += start

            ret.append((start, destination))
            self.queues[i] -= 1
        return ret

    def setSpawnRate(self, spawns_per_km_squared_hours):
        spawns_per_meter_squared_seconds = helpers.km_sq_hrs_to_m_sq_secs(
            spawns_per_km_squared_hours
        )
        spawns_per_seconds = spawns_per_meter_squared_seconds * self.sources.getArea()
        self.spawnrate_per_second = spawns_per_seconds

    def isAirspaceClear(self, point: c2.Cartesian2, acft: List[ac.Aircraft]):
        for plane in acft:
            if c2.Cartesian2.__abs__(plane.dynamic.position - point) < 150:
                return False
        return True

    def render(self, ax):
        self.render(
            self.sources, ax, "g", ":"
        )  # TODO need to find where this render function comes from
        self.render(self.destinations, ax, "b", ":")

        for i in range(len(self.sources.shapes)):
            if type(self.sources.shapes[i]) == circle.Circle:
                x = self.sources.shapes[i].center_point.x  # type: ignore
                y = (
                    self.sources.shapes[i].center_point.y   # type: ignore
                    + self.sources.shapes[i].radius         # type: ignore 
                ) 
                s = str(self.queues[i])
                plt.text(x, y, s)
            elif type(self.sources.shapes[i]) == rectangle.Rectangle:
                x = self.sources.shapes[i].top_left.x - 10  # type: ignore
                y = self.sources.shapes[i].bottom_right.y + 10  # type:ignore
                s = str(self.queues[i])
                plt.text(x, y, s)
            else:
                print("Shapes not supported")

    def getSinusoidal(self, length_of_cycle, max_value, min_value, peak_time):
        assert length_of_cycle > 0
        assert max_value >= min_value
        assert 0 <= peak_time <= length_of_cycle

        magnitude = (max_value - min_value) / 2
        adjustment = min_value + magnitude
        frequency = (2 * np.pi) / length_of_cycle

        return lambda x: magnitude * np.cos(frequency * (x - peak_time) + adjustment)
