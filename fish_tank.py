# File: fish_tank.py
# Author: Michael Huelsman
# Created On: 27 Oct 2023
# Lisence: GNU GPLv3
# Purpose:
#   A simple fish tank for rendering a screen full of fish.

from fish import Fish
from random import randrange
import numpy as np
import pygame as pg


class FishTank:
    __FOOD_LIMIT = 10
    __FOOD_COLOR = (10, 250, 130)
    def __init__(self, fish_count: int, dim: (int, int)):
        self.dim = dim
        self.fishes = [Fish(self.__rand_point(), self.dim) for i in range(fish_count)]
        self.surf = pg.Surface(self.dim)
        self.bg_color = (10, 150, 255)
        self.food_active = False
        self.food = None
        self.food_timer = 10
        
    def drop_food(self, pos: np.ndarray):
        self.food_active = True
        self.food = pos
        for fish in self.fishes:
            fish.goal = self.food
        self.food_timer = FishTank.__FOOD_LIMIT
            
    def pick_food(self):
        self.food_active = False

    def update(self, delta: float):
        if self.food_active:
            self.food_timer -= delta
            if self.food_timer <= 0:
                self.food_active = False
        if not self.food_active and self.food is not None:
            self.food = None
            for fish in self.fishes:
                fish.random_walk()
        for fish in self.fishes:
            fish.process(self.fishes)
        for fish in self.fishes:
            fish.update(delta)
    
    def draw(self, screen: pg.Surface):
        self.surf.fill(self.bg_color)
        if self.food_active:
            pg.draw.circle(self.surf, FishTank.__FOOD_COLOR, self.food, 10)
        for fish in self.fishes:
            fish.draw(self.surf)
        screen.blit(self.surf, (0, 0))
        
    def __rand_point(self):
        x_min = self.dim[0]//4
        x_max = x_min * 3
        y_min = self.dim[1]//4
        y_max = y_min * 3
        return np.array([randrange(x_min, x_max), randrange(y_min, y_max)], dtype=float)