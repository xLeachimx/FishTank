# File: fish_tank.py
# Author: Michael Huelsman
# Created On: 27 Oct 2023
# Lisence: GNU GPLv3
# Purpose:
#   A simple fish tank for rendering a screen full of fish.

from fish import Fish
from food import Food
from random import randrange
import numpy as np
import pygame as pg


class FishTank:
    __FOOD_LIMIT = 10
    __WATER_COLOR = (0, 35, 163)
    def __init__(self, fish_count: int, dim: (int, int)):
        self.dim = dim
        self.fishes = [Fish(self.__rand_point(), self.dim) for i in range(fish_count)]
        self.surf = pg.Surface(self.dim)
        self.bg_color = FishTank.__WATER_COLOR
        self.food_pellets = []
        
    def drop_food(self, pos: np.ndarray):
        self.food_pellets.append(Food(pos))

    def sprinkle_food(self):
        num_to_add = min(FishTank.__FOOD_LIMIT, len(self.fishes) - len(self.food_pellets))
        for _ in range(num_to_add):
            self.drop_food(self.__rand_point())

    def update(self, delta: float):
        fishes = np.array(list(map(lambda fish: fish.pos, self.fishes)))
        food = np.array(list(map(lambda pellet: pellet.pos, self.food_pellets)))
        for fish in self.fishes:
            fish.process_quick(fishes, food)
        for fish in self.fishes:
            fish.update(delta)
        self.check_food()

    def check_food(self):
        res_pellets = []
        for food in self.food_pellets:
            eaten = False
            for fish in self.fishes:
                if np.linalg.norm(food.pos - fish.pos) <= 5:
                    fish.feed()
                    eaten = True
                    break
            if not eaten:
                res_pellets.append(food)
        self.food_pellets = res_pellets
    
    def draw(self, screen: pg.Surface):
        self.surf.fill(self.bg_color)
        for food in self.food_pellets:
            food.draw(self.surf)
        for fish in self.fishes:
            fish.draw(self.surf)
        screen.blit(self.surf, (0, 0))
        
    def __rand_point(self):
        x_min = self.dim[0]//7
        x_max = x_min * 6
        y_min = self.dim[1]//7
        y_max = y_min * 6
        return np.array([randrange(x_min, x_max), randrange(y_min, y_max)], dtype=float)