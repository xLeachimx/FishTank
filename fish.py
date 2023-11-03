# File: fish.py
# Author: Michael Huelsman
# Created On: 26 Oct 2023
# Lisence: GNU GPLv3
# Purpose:
#   A simple fish object

from mob import Mobile
from food import Food
from random import randrange, choice
import numpy as np
import pygame as pg
from math import radians
from utilities import ang_to_vec, unit_vec, aspect_ratio


class Fish(Mobile):
    __NORM_FAC = 7
    __SPRITE_SWIM = pg.image.load("fish_sprite_swim.png")
    __SPRITE_HUNGRY = pg.image.load("fish_sprite_hungry.png")
    __SPD_MAX = 100.0
    __DEFAULT_DIST = 10**-5
    __ATTR_CONST = 1
    __REP_CONST = 30
    __DEFAULT_FORCING = 10
    __HUNGER_TIMER = 20

    def __init__(self, pos: np.ndarray, screen_dim: (int, int)):
        super(Fish, self).__init__(pos, np.array([0.0, 0.0]), Fish.__SPRITE_SWIM, screen_dim)
        self.goal = self.__random_goal()
        self.norm_dim = Fish.__NORM_FAC * np.array(aspect_ratio(screen_dim), dtype=float)
        self.state = "SWIM"
        self.hunger = randrange(5, Fish.__HUNGER_TIMER)
    
    def __random_goal(self):
        x_min = self.dim[0]//7
        x_max = x_min * 6
        y_min = self.dim[1]//7
        y_max = y_min * 6
        return np.array([randrange(x_min, x_max), randrange(y_min, y_max)], dtype=float)
    
    def update(self, delta: float):
        super(Fish, self).update(delta)
        self.hunger -= delta
        if self.hunger <= 0:
            self.state = "HUNGRY"
            self.sprite = Fish.__SPRITE_HUNGRY
        if np.linalg.norm(self.pos - self.goal) <= 10:
            self.goal = self.__random_goal()

    def feed(self):
        self.state = "SWIM"
        self.sprite = Fish.__SPRITE_SWIM
        self.hunger = randrange(5, Fish.__HUNGER_TIMER)

    def draw(self, surface: pg.Surface):
        super(Fish, self).draw(surface)
        
    def process_quick(self, fish: np.ndarray, food: np.ndarray):
        attractor = None
        if len(food) == 0 or self.state == "SWIM":
            attractor = np.array([self.goal])
        elif self.state == "HUNGRY":
            dist = np.linalg.norm(food - self.pos, axis=1)
            min_idx = np.argmin(dist)
            attractor = np.array([food[min_idx]])
        repulsor = np.apply_along_axis(self.__norm_position, 1, fish)
        attractor = np.apply_along_axis(self.__norm_position, 1, attractor)
        pos = self.__norm_position(self.pos)
        # Compute repulsing forces
        rep_diff = repulsor - pos
        rep_dist = np.power(np.linalg.norm(rep_diff, axis=1), 2)
        rep_dist[rep_dist == 0] = Fish.__DEFAULT_DIST
        rep = np.sum(rep_diff/np.transpose(np.array([rep_dist])), axis=0) * -1
        # Compute attracting forces
        attr_diff = attractor - pos
        attr_dist = np.power(np.linalg.norm(attr_diff, axis=1), 1)
        attr_dist[attr_dist == 0] = Fish.__DEFAULT_DIST
        attr = np.sum(attr_diff/np.transpose(np.array([attr_dist])), axis=0)
        # Combine
        balance = aspect_ratio((len(repulsor), len(attractor)))
        overall_vec = (balance[0] * Fish.__ATTR_CONST * attr) + (balance[1] * Fish.__REP_CONST * rep)
        overall_vec = Fish.__DEFAULT_FORCING * overall_vec
        speed = min(max(-Fish.__SPD_MAX, np.linalg.norm(overall_vec)), Fish.__SPD_MAX)
        self.velocity = speed * unit_vec(overall_vec)

    def __norm_position(self, vec):
        n = vec.copy()
        n[0] = self.norm_dim[0] * (n[0]/self.dim[0])
        n[1] = self.norm_dim[1] * (n[1]/self.dim[1])
        return n