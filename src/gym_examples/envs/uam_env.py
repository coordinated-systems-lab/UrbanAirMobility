import math
import random
import numpy as np
import gymnasium as gym
from gymnasium import spaces
from stable_baselines3 import A2C, PPO
from stable_baselines3.common.env_util import make_vec_env
from typing import Tuple, Callable, Generator, Any, Dict
from gymnasium.spaces import Discrete


from modules import pilotfunction as pfunc, airspace as aspc, cartesian2 as c2, constantspawnratecontroller as cnstspwnctrl, pathfinder as pf, polar2 as p2, shapemanager as shpmng


# discrete state space
# discrete action space
class UAM_Env(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}

    def __init__(
        self,
        pilot_function : None | Callable = None,
        spawn_controller: cnstspwnctrl.ConstantSpawnRateController = cnstspwnctrl.ConstantSpawnRateController.constantspawnratecontroller(c2.Cartesian2(10000,10000), True),  
        restricted_areas: shpmng.ShapeManger = shpmng.ShapeManger.shapemanager(),
        waypoints: pf.PathFinder = pf.PathFinder.pathfinder_empty(),
        current_time: float = 0,
        is_MDP: bool = True,
        boundary: c2.Cartesian2 = c2.Cartesian2(100000, 10000),
        maximum_aircraft_acceleration: p2.Polar2 = p2.Polar2(3, 2 * math.pi / 10),
        maximum_aircraft_speed: float = 50,
        detection_radius: float = 1000,
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
            #self.pilot_function is a callable - pilot_fucntion is some_pilot_function from pilotfunction module
            self.pilot_function = pfunc.default_pilot_function(maximum_aircraft_acceleration)
        
        self.airspace = airspace
        self.is_MDP = is_MDP
        self.rng = rng
        self.current_time = current_time
        self.max_time = max_time
        self.time_step = time_step
        self.nmac_distance = nmac_distance
        
        # needs attention - fix observation space 
        
        
        self.observation_space = gym.spaces.Box(
            low = np.array([-np.pi, 0, 0, 0, -np.pi, -np.pi, 0]),                                                                               #! why should isIntruder be a value between 0 and 1 NEED TO CHECK 
                            # deviation, own_vel, isIntruder, distance_to_intruder, angle_of_intruder, relative_heading_intruder, relative_vel_intruder
            high = np.array([np.pi, self.airspace.maximum_aircraft_speed, 1, self.airspace.detection_radius, np.pi, np.pi, 2*self.airspace.maximum_aircraft_speed]), 
                                                                                                                                                #! add the explanantion in readme for the choice of obs space parameters 
            shape=(7,),
            dtype=np.float64
        )  
        
        # * make a wrapper that converts to discrete
        
        self.action_space = gym.spaces.Box(
            low=np.array(
                [
                    -self.airspace.maximum_aircraft_acceleration.r / abs(self.airspace.maximum_aircraft_acceleration.r),
                    -self.airspace.maximum_aircraft_acceleration.theta/ abs(self.airspace.maximum_aircraft_acceleration.theta),
                ]
            ),
            high=np.array(
                [
                    self.airspace.maximum_aircraft_acceleration.r/ abs(self.airspace.maximum_aircraft_acceleration.r),
                    self.airspace.maximum_aircraft_acceleration.theta/ abs(self.airspace.maximum_aircraft_acceleration.theta),
                ]
            ),
            shape=(2,),
            dtype=np.float32
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
    
    
    #* The constructor has been commented - Does gym envs not work with constructor for entry points ???
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

    def _get_obs(self) :
        ego_agent_state = self.airspace.getEgoState()
        # deviation, 
        ego_deviation = ego_agent_state[0]
        # own_vel, 
        ego_velocity = ego_agent_state[1]
        # isIntruder,
        ego_intruder = ego_agent_state[2]
        # distance_to_intruder, 
        ego_dist_intruder = ego_agent_state[3]
        # angle_of_intruder, 
        ego_angle_intruder = ego_agent_state[4]
        # relative_heading_intruder, 
        rel_heading_intruder = ego_agent_state[5]
        # relative_vel_intruder
        rel_vel_intruder = ego_agent_state[6]
        # ego agent state
        

        #dest location
        #dests = self.airspace.all_aircraft[0].destinations
        #look at aircraft, pull information from there 
        return np.array([ego_deviation, ego_velocity, ego_intruder, ego_dist_intruder, ego_angle_intruder, rel_heading_intruder, rel_vel_intruder])
    
    def _get_info(self) -> Dict:
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
    
    
    def step(
        self,action_1, action_2=None
    ) -> Tuple[Any, float, bool, bool, dict,]:
        
        
        #ego action 
        assert self.is_MDP == True
        action_1 = p2.Polar2(action_1[0], action_1[1])
        self.airspace.setEgoAcceleration(action_1)
        
        #action_2 comes from second algo 
        if action_2 is not None:
            action_2 = p2.Polar2(action_2[0], action_2[1])
       
        
        
        #non-ego action
        all_state = self.airspace.getAllStates()
        all_action = []
        #* when the step method is called by an algorithm from the stable baselines library
        #* the step method will use actions from the action space defined in the init 

        
        for state in all_state:
            if (action_2 is not None) and (state == all_state[0]): 
                #next_to_ego action 
                all_action.append(action_2)
                continue 
         
            #                     pilot_function is some_pilot_function 
            action_non_ego = self.pilot_function(state, self.rng)
            action_non_ego = p2.Polar2(action_non_ego[0], action_non_ego[1])
            all_action.append(action_non_ego)
        
        self.airspace.setAllAccelerations(all_action)

        self.airspace.step(self.time_step, self.current_time, self.nmac_distance)
        self.current_time += self.time_step     

        
        observations = self._get_obs()

        reward = self._get_reward()

        terminated = self.airspace.all_aircraft[0].hasArrived(self.airspace.arrival_radius)[1]

        truncated = (self.current_time >= self.max_time)

        info = self._get_info()




        return observations, reward, terminated, truncated, info
    
        
     
    def reset(self, seed=None, options=None):
        self.airspace.reset()
        self.current_time = 0

        observation = self._get_obs()
        info = self._get_info()

        return observation, info

    def render(self):
        pass

    def close(self):
        pass


# Training and Testing in module script 
env = UAM_Env()
vec_env = make_vec_env(UAM_Env, n_envs=1)

model_a2c = A2C("MlpPolicy", env, verbose=1).learn(5)
print("A2C training complete")
model_ppo = PPO("MlpPolicy", env, verbose=1, n_steps=32, n_epochs=2).learn(5)
print("PPO training complete")

obs = vec_env.reset()


n_step = 5

for step in range(n_step):
    action_1, _ = model_a2c.predict(obs, deterministic=True)
    action_2, _ = model_ppo.predict(obs,deterministic=True)
    print(f"Step {step +1}")
    print("Action ego: ", action_1)
    print("Action next to ego: ", action_2)
    
    if action_1.shape == (1,2):
        action_1 = action_1[0]
    else:
        action_1 = action_1
    print(action_1.shape)
    
    if action_2.shape == (1,2):
        action_2 = action_2[0]
    else:
        action_2 = action_2
    print(action_2.shape)
    obs, reward, terminated, truncated, info = env.step(action_1, action_2)
    # vec_env is UAM_Env obj          step is from UAM_Env class 
    
    print("obs= ", obs, "reward= ", reward, "terminated= ", terminated, "truncated= ", truncated)
    
    if terminated:
        print("Goal reached!", "reward= ", reward)
        break
    elif truncated:
        print("Truncated for test step completion")
        break
