import gym_examples 
from gym_examples.envs.uam_env import UAM_Env
import gymnasium

from stable_baselines3.common.env_checker import check_env
from stable_baselines3 import A2C, PPO
#the following import is for making vectorized envs and testing trained agent in multiple vectorized env 
from stable_baselines3.common.env_util import make_vec_env

#!
#* INSTANTIATE THE ENV 
env = UAM_Env()
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

