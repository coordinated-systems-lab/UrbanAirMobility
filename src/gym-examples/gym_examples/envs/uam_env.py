import math
import random
import numpy as np
import gymnasium as gym
from gymnasium import spaces
from typing import Tuple, Callable, Generator, Any
from gymnasium.spaces import Discrete

from modules import pilotfunction as pfunc, airspace as aspc, cartesian2 as c2, constantspawnratecontroller as cnstspwnctrl, pathfinder as pf, polar2 as p2, shapemanager as shpmng


# discrete state space
# discrete action space
class UAM_Env(gym.Env):
    metadata = {"render_mode": ["human", "rgb_array"], "render_fps": 4}

    def __init__(
        self,
        spawn_controller: cnstspwnctrl.ConstantSpawnRateController,  #! this class will take is_MDP, and boundary as input in the factory definition
        restricted_areas: shpmng.ShapeManger,
        waypoints: pf.PathFinder,
        current_time: float = 0,
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
            self.pilot_function = pfunc.default_pilot_function(maximum_aircraft_acceleration)
        
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
            #! add the explanantion in readme for the choice of obs space parameters 
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
        # comments below are from gymnasium 
        """
        If human-rendering is used, `self.window` will be a reference
        to the window that we draw to. `self.clock` will be a clock that is used
        to ensure that the environment is rendered at the correct framerate in
        human-mode. They will remain `None` until human-mode is used for the
        first time.
        """
        self.window = None
        self.clock = None
    
    
    #* The constructor has been commented - gym does not work with constructor for entry points
    # @classmethod
    # def uam_env(
    #     cls,
    #     spawn_controller: cnstspwnctrl.ConstantSpawnRateController,  #! this class will take is_MDP, and boundary as input in the factory definition
    #     restricted_areas: shpmng.ShapeManger,
    #     waypoints: pf.PathFinder,
    #     is_MDP: bool = True,
    #     boundary: c2.Cartesian2 = c2.Cartesian2(100000, 10000),
    #     maximum_aircraft_acceleration: p2.Polar2 = p2.Polar2(3, 2 * math.pi / 10),
    #     maximum_aircraft_speed: float = 50,
    #     detection_radius: float = 1000,
    #     pilot_function: None | Callable = None,
    #     max_time: float = 3600,  # * this is sim time/ experiment time ??
    #     time_step: float = 1,  # * assuming this to be a timestep of 1 second ??
    #     arrival_distance: float = 100,
    #     nmac_distance: float = 150,
    #     rng: random.Random = random.Random(123),
    # ):
    #     airspace = aspc.Airspace.airspace(
    #         boundary=boundary,
    #         spawn_controller=spawn_controller,
    #         restricted_areas=restricted_areas,
    #         waypoints=waypoints,
    #         maximum_aircraft_acceleration=maximum_aircraft_acceleration,
    #         rng=rng,
    #         create_ego_aircraft=is_MDP,
    #         maximum_aircraft_speed=maximum_aircraft_speed,
    #         detection_radius=detection_radius,
    #         arrival_radius=arrival_distance,
    #     )
    #     if pilot_function == None:
    #         pilot_function = pfunc.default_pilot_function(maximum_aircraft_acceleration)

    #     return cls(
    #         airspace, is_MDP, pilot_function, rng, 0, max_time, time_step, nmac_distance
    #     )

    def _get_obs(self):
        # ego agent state
        ego_agent_state = self.airspace.getEgoState()
        
        # current deviation
        ego_deviation = ego_agent_state[0]
        # current velocity
        ego_velocity = ego_agent_state[1]
        # has intruder 
        ego_intruder = ego_agent_state[2]

        #dest location
        dests = self.airspace.all_aircraft[0].destinations
        
        #look at aircraft, pull information from there 
        return ego_deviation, ego_velocity, ego_intruder, dests
    
    def _get_info(self):
        #distance to target 
        dist_dest = self.airspace.all_aircraft[0].aircraft_stat()
        return dist_dest
    
    def _get_reward(self):
        #getEgoState returns getState
        #getState returns a list with 7 items 
        state = self.airspace.getEgoState()

        punishment_existing = -0.1

        if state[2] == 0:
            punishment_closeness = 0
        else:
            normed_nmac_distance = self.nmac_distance / self.airspace.detection_radius
            punishment_closeness = math.e ** ((normed_nmac_distance - state[3]) * 10)
        
        reward_to_destination = state[1] * math.cos(state[0])

        punishment_devation = -2 * (state[0] / math.pi)**2

        reward_sum = punishment_existing + punishment_closeness + reward_to_destination + punishment_devation

        reward_sum *= self.time_step
        
        return reward_sum

    #! Do we need a 'done' in return if we do add that to return signature of step 
    def step(
        self, action
    ) -> Tuple[Any, float, bool, bool, dict,]:
        
        observations = self._get_obs()

        reward = self._get_reward()

        terminated = self.airspace.all_aircraft[0].hasArrived(self.airspace.arrival_radius)[1]

        truncated = (self.current_time >= self.max_time)

        info = self._get_info()




        return observations, reward, terminated, truncated, info

    def reset(self, seed=None, options=None):
        self.airspace.reset()
        self.current_time = 0

    def render(self):
        pass

    def close(self):
        pass
