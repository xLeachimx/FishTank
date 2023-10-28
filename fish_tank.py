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
    def __init__(self, fish_count: int, dim: (int, int)):
        self.dim = dim
        self.fishes = [Fish(self.__rand_point(), self.dim) for i in range(fish_count)]
        self.surf = pg.Surface(self.dim)
        self.bg_color = (10, 150, 255)
        self.food_active = False
        self.food = None
        
    def drop_food(self, pos: np.ndarray):
        self.food_active = True
        self.food = pos
        for fish in self.fishes:
            fish.goal = self.food
            
    def pick_food(self):
        self.food_active = False

    def update(self, delta: float):
        # if self.food_active:
        #     for fish in self.fishes:
        #         if np.linalg.norm(fish.pos - self.food) < 10:
        #             self.food_active = False
        #             break
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
            pg.draw.circle(self.surf, (0, 0, 0), self.food, 10)
        for fish in self.fishes:
            fish.draw(self.surf)
        screen.blit(self.surf, (0, 0))
        
    def __rand_point(self):
        return np.array([randrange(0, self.dim[0]), randrange(0, self.dim[1])], dtype=float)