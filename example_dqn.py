import gymnasium as gym

from stable_baselines3 import DQN
from snake_env import CustomEnv

# env = gym.make("CartPole-v1", render_mode="human")
env = CustomEnv(fps=400,window_x=720,window_y=480)
model = DQN("MultiInputPolicy", env, verbose=1)
model.learn(total_timesteps=1000, log_interval=4)
# model.save("dqn_cartpole")
#
# del model # remove to demonstrate saving and loading
#
# model = DQN.load("dqn_cartpole")

obs, info = env.reset()
while True:
    action, _ = model.predict(obs, deterministic=True)
    obs, reward, terminated, truncated, _ = env.step(action)
    if terminated or truncated:
        obs, info = env.reset()