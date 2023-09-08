from gym_examples.envs.uam_env import UAM_Env
import gymnasium as gym 
from ray.rllib.algorithms.ppo import PPOConfig
from ray.tune.logger import pretty_print
from ray.tune.registry import register_env

# The following two lines show that UAM is a registered gym environment,
# Uncomment and check is env is registered properly 

#gym.spec("gym_examples/UAM-v0")
#gym.pprint_registry()

# 

register_env("single_agent_uam_env", lambda config: UAM_Env(config))


algo = (
    PPOConfig()
    .rollouts(num_rollout_workers=1)
    .environment(env="single_agent_uam_env", disable_env_checking=True)
    .build()
)

for i in range(5):
    result = algo.train()
    print(pretty_print(result))

    if i%2 == 0:
        checkpoint_dir = algo.save()
        print(f"Checkpoint saved in directory {checkpoint_dir}")
    