import gym
from ray import tune
from ray.tune.registry import register_env

from .task_wrappers import CartPoleTaskWrapper

if __name__ == "__main__":

    def env_creator(config):
        env = gym.make("CartPole-v1")
        # Wrap the environment to change tasks on reset()
        env = CartPoleTaskWrapper(env)

        return env

    register_env("task_cartpole", env_creator)

    config = {
        "env": "task_cartpole",
        "num_gpus": 1,
        "num_workers": 8,
        "framework": "torch",
    }

    tuner = tune.Tuner("APEX", param_space=config)
    results = tuner.fit()
