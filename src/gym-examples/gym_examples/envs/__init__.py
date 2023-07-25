#__init__.py

from gymnasium.envs.registration import register

register(
     id="gym-examples/UAM-v0",
     entry_point="gym-examples.envs:UAM_Env",
     max_episode_steps=300,
)