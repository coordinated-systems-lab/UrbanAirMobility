import math
import random
import numpy as np
import gymnasium as gym
from gymnasium import spaces
from typing import Tuple, Callable, Generator
from gymnasium.spaces import Discrete

import pilotfunction as pfunc
import airspace as aspc
import cartesian2 as c2
import constantspawnratecontroller as cnstspwnctrl
import pathfinder as pf
import polar2 as p2
import shapemanager as shpmng


# discrete state space
# discrete action space
class UAM_Env(gym.Env):
    metadata = {"render_mode": ["human", "rgb_array"], "render_fps": 4}

    def __init__(
        self,
        airspace: aspc.Airspace,
        is_MDP: bool,
        pilot_function: Callable,
        rng: random.Random,
        current_time: float,
        max_time: float,
        time_step: float,
        nmac_distance: float,
    ):
        self.airspace = airspace
        self.is_MDP = is_MDP
        self.pilot_function = pilot_function
        self.rng = rng
        self.current_time = current_time
        self.max_time = max_time
        self.time_step = time_step
        self.nmac_distance = nmac_distance
        
        # needs attention - fix observation space 
        self.observation_space = gym.spaces.Box(
            low = np.array([-np.pi, 0, 0, 0, -np.pi, -np.pi, 0]), #! why should isIntruder be a value between 0 and 1 NEED TO CHECK 
                            # deviation, own_vel, isIntruder, distance_to_intruder, angle_of_intruder, relative_heading_intruder, relative_vel_intruder
            high = np.array([np.pi, self.airspace.maximum_aircraft_speed, 1, self.airspace.detection_radius, np.pi, np.pi, 2*self.airspace.maximum_aircraft_speed]), 
            
            shape=(7,)
        )  
        
        # * make a wrapper that converts to discrete
        self.action_space = gym.spaces.Box(
            low=np.array(
                [
                    -self.airspace.maximum_aircraft_acceleration.r,
                    -self.airspace.maximum_aircraft_acceleration.theta,
                ]
            ),
            high=np.array(
                [
                    self.airspace.maximum_aircraft_acceleration.r,
                    self.airspace.maximum_aircraft_acceleration.theta,
                ]
            ),
            shape=(2,),
        )
        

    @classmethod
    def uam_env(
        cls,
        spawn_controller: cnstspwnctrl.ConstantSpawnRateController,  #! this class will take is_MDP, and boundary as input in the factory definition
        restricted_areas: shpmng.ShapeManger,
        waypoints: pf.PathFinder,
        is_MDP: bool = True,
        boundary: c2.Cartesian2 = c2.Cartesian2(100000, 10000),
        maximum_aircraft_acceleration: p2.Polar2 = p2.Polar2(3, 2 * math.pi / 10),
        maximum_aircraft_speed: float = 50,
        detection_radius: float = 1000,
        pilot_function: None | Callable = None,
        max_time: float = 3600,  # * this is sim time/ experiment time ??
        time_step: float = 1,  # * assuming this to be a timestep of 1 second ??
        arrival_distance: float = 100,
        nmac_distance: float = 150,
        rng: random.Random = random.Random(123),
    ):
        airspace = aspc.Airspace.airspace(
            boundary=boundary,
            spawn_controller=spawn_controller,
            restricted_areas=restricted_areas,
            waypoints=waypoints,
            maximum_aircraft_acceleration=maximum_aircraft_acceleration,
            rng=rng,
            create_ego_aircraft=is_MDP,
            maximum_aircraft_speed=maximum_aircraft_speed,
            detection_radius=detection_radius,
            arrival_radius=arrival_distance,
        )
        if pilot_function == None:
            pilot_function = pfunc.default_pilot_function(maximum_aircraft_acceleration)

        return cls(
            airspace, is_MDP, pilot_function, rng, 0, max_time, time_step, nmac_distance
        )


    #! Do we need a 'done' in return if we do add that to return signature of step 
    def step(
        self, action
    ) -> Tuple[ObsType, float, bool, bool, dict,]:
        
        observations = 

        reward = 

        terminated = 

        truncated = 

        info = 




        return observations, reward, terminated, truncated, info

    def reset(self, seed=None, options=None):
        pass

    def render(self):
        pass

    def close(self):
        pass
