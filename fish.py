# File: fish.py
# Author: Michael Huelsman
# Created On: 26 Oct 2023
# Lisence: GNU GPLv3
# Purpose:
#   A simple fish object

from mob import Mobile
from random import randrange
import numpy as np
import pygame as pg
from math import radians
from utilities import ang_to_vec, unit_vec, aspect_ratio


class Fish(Mobile):
    __NORM_FAC = 10
    __FISH_SPRITE = pg.image.load("fish_sprite_swim.png")
    __SPD_MAX = 100.0
    __DEFAULT_DIST = 10**-5
    __ATTR_CONST = 1
    __REP_CONST = 50
    __DEFAULT_FORCING = 10

    def __init__(self, pos: np.ndarray, screen_dim: (int, int)):
        super(Fish, self).__init__(pos, np.array([0.0, 0.0]), Fish.__FISH_SPRITE, screen_dim)
        self.goal = self.__random_goal()
        self.norm_dim = Fish.__NORM_FAC * np.array(aspect_ratio(screen_dim), dtype=float)
    
    def __random_goal(self):
        x_min = self.dim[0]//10
        x_max = x_min * 9
        y_min = self.dim[1]//10
        y_max = y_min * 9
        return np.array([randrange(x_min, x_max), randrange(y_min, y_max)], dtype=float)
    
    def random_walk(self):
        self.goal = self.__random_goal()
    
    def update(self, delta: float):
        super(Fish, self).update(delta)
        if np.linalg.norm(self.pos - self.goal) <= 5:
            self.goal = self.__random_goal()
            
    def draw(self, surface: pg.Surface):
        super(Fish, self).draw(surface)
        
    def process_quick(self, repulsors: np.ndarray, attractors: np.ndarray):
        repulsors = np.apply_along_axis(self.__norm_position, 1, repulsors)
        attractors = np.apply_along_axis(self.__norm_position, 1, attractors)
        pos = self.__norm_position(self.pos)
        # Compute repulsing forces
        rep_diff = repulsors - pos
        rep_dist = np.power(np.linalg.norm(rep_diff, axis=1), 2)
        rep_dist[rep_dist == 0] = Fish.__DEFAULT_DIST
        rep = np.sum(rep_diff/np.transpose(np.array([rep_dist])), axis=0) * -1
        # Compute attracting forces
        attr_diff = attractors - pos
        attr_dist = np.power(np.linalg.norm(attr_diff, axis=1), 1)
        attr_dist[attr_dist == 0] = Fish.__DEFAULT_DIST
        attr = np.sum(attr_diff/np.transpose(np.array([attr_dist])), axis=0)
        # Combine
        balance = aspect_ratio((len(repulsors), len(attractors)))
        overall_vec = (balance[0] * Fish.__ATTR_CONST * attr) + (balance[1] * Fish.__REP_CONST * rep)
        overall_vec = Fish.__DEFAULT_FORCING * overall_vec
        speed = min(max(-Fish.__SPD_MAX, np.linalg.norm(overall_vec)), Fish.__SPD_MAX)
        self.velocity = speed * unit_vec(overall_vec)

    def __norm_position(self, vec):
        n = vec.copy()
        n[0] = self.norm_dim[0] * (n[0]/self.dim[0])
        n[1] = self.norm_dim[1] * (n[1]/self.dim[1])
        return n