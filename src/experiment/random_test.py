import gym_examples 
from gym_examples.envs.uam_env import UAM_Env
import gymnasium

from stable_baselines3.common.env_checker import check_env
from stable_baselines3 import A2C
#the following import is for making vectorized envs and testing trained agent in multiple vectorized env 
from stable_baselines3.common.env_util import make_vec_env

#!
#* INSTANTIATE THE ENV 
env = gymnasium.make('gym_examples/UAM-v0')
#* INSTANTIATE THE VECTORIZED ENV 
vec_env = make_vec_env(UAM_Env, n_envs=1)
# check_env(env)

# print("Observation space: ", env.observation_space)
# print("Shape of observation space: ", env.observation_space.shape)
# print("Action space: ", env.action_space)

# obs, info = env.reset()

# action = env.action_space.sample()
# print("Sampled action: ", action)

# obs, reward, terminated,truncated, info = env.step(action)

# print(obs.shape, reward, terminated, truncated, info)
#!

# TRAINING AGENT 
model = A2C("MlpPolicy", env, verbose=1).learn(100)

# TESTING THE TRAINED AGENT 
obs = vec_env.reset()
n_step = 20

for step in range(n_step):
    action, _ = model.predict(obs, deterministic=True)
    print(f"Step {step +1}")
    print("Action: ", action)
    obs, reward, done, info = vec_env.step(action)
    print("obs= ", obs, "reward= ", reward, "done= ", done)
    
    if done:
        print("Goal reached!", "reward= ", reward)
        break


