import gymnasium as gym
import numpy as np
from gymnasium import spaces
import pygame
import time
import random
import enum
import math

from poetry.utils.helpers import directory



class CustomEnv(gym.Env):
    """Custom Environment that follows gym interface."""

    metadata = {"render_modes": ["human"], "render_fps": 30}

    def __init__(self, fps, window_x,window_y ):
        super().__init__()
        self.snake_speed = fps
        self.fps = pygame.time.Clock()
        self.window_x = window_x
        self.window_y = window_y
        self.black = pygame.Color(0, 0, 0)
        self.white = pygame.Color(255, 255, 255)
        self.red = pygame.Color(255, 0, 0)
        self.green = pygame.Color(0, 255, 0)
        self.blue = pygame.Color(0, 0, 255)
        self.snake_position = [100, 50]
        pygame.init()
        pygame.display.set_caption('Snake')
        self.game_window = pygame.display.set_mode((self.window_x, self.window_y))
        self.fps = pygame.time.Clock()
        self.snake_body = [[100, 50],
                      [90, 50],
                      [80, 50],
                      [70, 50]
                      ]
        self.fruit_position = [random.randrange(1, (self.window_x // 10)) * 10,
                          random.randrange(1, (self.window_y // 10)) * 10]
        self.fruit_spawn = True
        self.direction = 'RIGHT'
        self.change_to = self.direction
        self.score = 0
        self.observation_space = spaces.Dict(
            {
                "fruit_position": spaces.Box(low=np.array([0,0]),shape=(2,), high=np.array([self.window_x,self.window_y]), dtype=np.int64),
                "snake_position": spaces.Box(low=np.array([0,0]),shape=(2,), high=np.array([self.window_x,self.window_y]), dtype=np.int64),
                "direction": spaces.Box(0, 4,shape=(1,), dtype=np.int64),
            }
        )
        # Define action and observation space
        # They must be gym.spaces objects
        # Example when using discrete actions:
        self.action_space = spaces.Discrete(4)

    def step(self, action):
        reward = 0
        self.set_direction(action)
        if self.direction ==  'UP':
            self.snake_position[1] -= 10
        if self.direction == 'DOWN':
            self.snake_position[1] += 10
        if self.direction == 'LEFT':
            self.snake_position[0] -= 10
        if self.direction == 'RIGHT':
            self.snake_position[0] += 10
        self.snake_body.insert(0, list(self.snake_position))
        if self.snake_position[0] == self.fruit_position[0] and self.snake_position[1] == self.fruit_position[1]:
            self.score += 10
            reward += 100
            self.fruit_spawn = False
        else:
            self.snake_body.pop()

        if not self.fruit_spawn:
            self.fruit_position = [random.randrange(1, (self.window_x // 10)) * 10,
                              random.randrange(1, (self.window_y // 10)) * 10]
        self.fruit_spawn = True
        terminated = False
        if self.snake_position[0] < 0 or self.snake_position[0] > self.window_x - 10:
            reward -= 100
            terminated = True
        if self.snake_position[1] < 0 or self.snake_position[1] > self.window_y - 10:
            reward -= 100
            terminated = True

        # Touching the snake body
        for block in self.snake_body[1:]:
            if self.snake_position[0] == block[0] and self.snake_position[1] == block[1]:
                reward -= 100
                terminated = True

        if not terminated:
            reward += 5
        fruit_distance = math.sqrt(abs(self.fruit_position[0] - self.snake_body[0][0])**2 + abs(self.fruit_position[1] - self.snake_body[0][1])**2)
        last_fruit_distance = math.sqrt(abs(self.fruit_position[0] - self.snake_body[1][0])**2 + abs(self.fruit_position[1] - self.snake_body[1][1])**2)
        reward += last_fruit_distance-fruit_distance*2
        info={}
        self.render()
        observation = {"fruit_position": np.array(self.fruit_position) , "snake_position":np.array(self.snake_position), "direction":np.array([self.get_direction()])}
        return observation, reward, terminated, False, info

    def reset(self, seed=None, options=None):
        pygame.event.get()
        self.score = 0
        self.snake_position = [100, 50]
        self.snake_body = [[100, 50],
                           [90, 50],
                           [80, 50],
                           [70, 50]
                           ]
        self.fruit_position = [random.randrange(1, (self.window_x // 10)) * 10,
                               random.randrange(1, (self.window_y // 10)) * 10]
        self.fruit_spawn = True
        self.direction = 'RIGHT'
        self.change_to = self.direction
        observation = {"fruit_position": np.array(self.fruit_position), "snake_position": np.array(self.snake_position),
                       "direction": np.array([self.get_direction()])}

        return observation, {}

    def render(self):
        self.game_window.fill(self.black)
        for pos in self.snake_body:
            pygame.draw.rect(self.game_window, self.green,
                             pygame.Rect(pos[0], pos[1], 10, 10))
        pygame.draw.rect(self.game_window, self.white, pygame.Rect(
            self.fruit_position[0], self.fruit_position[1], 10, 10))
        pygame.display.update()
        self.fps.tick(self.snake_speed)

    def show_score(self,choice, color, font, size):
        score_font = pygame.font.SysFont(font, size)
        score_surface = score_font.render('Score : ' + str(self.score), True, color)
        score_rect = score_surface.get_rect()
        self.game_window.blit(score_surface, score_rect)

    def close(self):
        pygame.quit()

    def set_direction(self, action):
        if action == 1:
            self.change_to = 'UP'
        if action == 2:
            self.change_to = 'DOWN'
        if action ==3:
            self.change_to = 'LEFT'
        if action == 4:
            self.change_to = 'RIGHT'

        if self.change_to == 'UP' and self.direction != 'DOWN':
            self.direction = 'UP'
        if self.change_to == 'DOWN' and self.direction != 'UP':
            self.direction = 'DOWN'
        if self.change_to == 'LEFT' and self.direction != 'RIGHT':
            self.direction = 'LEFT'
        if self.change_to == 'RIGHT' and self.direction != 'LEFT':
            self.direction = 'RIGHT'
    def get_direction(self):

        if self.direction == 'UP':
            return 1
        if self.direction == 'DOWN':
            return 2
        if self.direction == 'LEFT':
            return 3
        if self.direction == 'RIGHT':
            return 4
        return 1
