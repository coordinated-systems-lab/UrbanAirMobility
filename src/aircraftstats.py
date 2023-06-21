import uuid


class AircraftStats:
    def __init__(
        self,
        ideal_distance,
        ac_encountered: dict,
        unique_id=uuid.uuid1(),
        distance_traveled=0,
        time_elapsed=0,
        num_nmac=0,
    ):  # check if uuid1() is a predefined Julia function or defined function in AAM project or not
        self.ideal_distance = ideal_distance
        self.distance_traveled = distance_traveled
        self.time_elapsed = time_elapsed
        self.num_nmac = num_nmac
        self.unique_id = unique_id
        self.ac_encountered = ac_encountered

    # factory function for creating aircraftstats for aircraft
    @classmethod
    def aircraftstats(cls, ideal_distance):
        return cls(ideal_distance, {}, uuid.uuid1(), 0, 0, 0)

    def getNormalizedRouteLength(self):
        return self.distance_traveled / self.ideal_distance

    def getAverageVelocity(self):
        return self.distance_traveled / self.time_elapsed

    def getNMACPerSecond(self):
        return self.num_nmac / self.time_elapsed
