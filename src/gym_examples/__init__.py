#__init__.py

from gymnasium.envs.registration import register

register(
     id="gym_examples/UAM-v0",
     entry_point="gym_examples.envs:UAM_Env", #? can there be multiple entry points 
     max_episode_steps=300,
)