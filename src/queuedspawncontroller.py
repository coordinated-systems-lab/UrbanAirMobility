import numpy as np
from typing import List, Tuple

import abstractspawncontroller as abscntl
import shapemanager as shpmng
import cartesian2 as c2
import helpers
import aircraft as acft


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
        relativea_destination: bool,
    ):
        spawns_per_seconds = (
            helpers.km_sq_hrs_to_m_sq_secs(spawns_per_km_squared_hours)
            * sources.getArea()
        )
        queues = np.zeros(len(sources.shapes))

        return cls(
            sources, destinations, queues, spawns_per_seconds, relativea_destination
        )
