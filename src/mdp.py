import numpy as np 
class CollisionAvoidanceEnv(AbstractEnv):
    def __init__(self,
                 is_MDP:bool = True,
                 boundary:Cartesian2 = (10000,10000),
                 spawn_controller:AbstractSpawnController = ConstantSpawnrateController(boundary,isMDP),
                 restricted_areas:ShapeManager = ShapeManager(),
                 waypoints:PathFinder = PathFinder(),
                 maximum_aircraft_acceleration:Polar2 = Polar2(3.0, 2*pi/10),
                 maximum_aircraft_speed:float = 50.0,
                 detection_radius:float = 1000.0,
                 pilot_function = None,
                 max_time:float = 3600.0,
                 timestep:float = 1.0,
                 arrival_distance:float = 100.0,
                 nmac_distance:float = 150.0,
                 rng = np.random.MersenneTwister(123) ## needs work
    ):
        self.is_MDP = is_MDP
        self.boundary = boundary
        self.spawn_controller = spawn_controller
        self.restricted_areas = restricted_areas
        self.waypoints = waypoints
        self.maximum_aircraft_acceleration = maximum_aircraft_acceleration
        self.maximum_aircraft_speed = maximum_aircraft_speed
        self.detection_radius = detection_radius
        self.pilot_function = pilot_function
        self.max_time = max_time
        self.timestep = timestep
        self.arrival_distance = arrival_distance
        self.nmac_distance = nmac_distance
        self.rng = rng
    

        airspace = Airspace(
                            boundary = boundary,
                            rng = rng,
                            create_ego_aircraft = create_ego_aircraft,
                            spawn_controller = spawn_controller,
                            restricted_airspace = restricted_airspace,
                            waypoints = waypoints,
                            maximum_aircraft_acceleration = maximum_aircraft_acceleration,
                            maximum_aircraft_speed = maximum_aircraft_speed,
                            detection_radius = detection_radius,
                            arrival_radius = arrival_radius
    )


        if self.pilot_function == None:
            self.pilot_function = default_pilot_function(maximum_aircraft_acceleration)
        