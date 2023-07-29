import gym_examples 
import gymnasium
from stable_baselines3.common.env_checker import check_env

env = gymnasium.make('gym_examples/UAM-v0')
check_env(env)







