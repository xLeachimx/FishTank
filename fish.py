# File: fish.py
# Author: Michael Huelsman
# Created On: 26 Oct 2023
# Lisence: GNU GPLv3
# Purpose:
#   A simple fish object
#  TODO: Normal position during repulsor calculation for more consistent factors

from mob import Mobile
from random import randrange
import numpy as np
import pygame as pg
from math import radians
from utilities import ang_to_vec


class Fish(Mobile):
    __NORM_FAC = 1
    def __init__(self, pos: np.ndarray, screen_dim: (int, int)):
        super(Fish, self).__init__(pos, 50, pg.image.load("fish_sprite.png"), screen_dim)
        self.goal = self.__random_goal()
        self.spd_base = 4
        self.spd_max = 100
        self.spd_min = 10
    
    def __random_goal(self):
        return np.array([randrange(0, self.dim[0]), randrange(0, self.dim[1])], dtype=float)
    
    def random_walk(self):
        self.goal = self.__random_goal()
    
    def update(self, delta: float):
        super(Fish, self).update(delta)
        if np.linalg.norm(self.pos - self.goal) <= 5:
            self.goal = self.__random_goal()
            
    def draw(self, surface: pg.Surface):
        super(Fish, self).draw(surface)
    
    def process(self, fishes: list['Fish']):
        g_norm = self.__pos_norm(self.goal)
        p_norm = self.__pos_norm(self.pos)
        repulse_factor = 1
        attraction_factor = 2 * len(fishes)
        # overall_vec = attraction_factor * ((self.goal - self.pos)/np.linalg.norm(self.goal - self.pos))
        g_dist = np.linalg.norm(g_norm - p_norm)
        overall_vec = attraction_factor * ((g_norm - p_norm)/g_dist)
        for fish in fishes:
            if self == fish:
                continue
            vec_between = p_norm - self.__pos_norm(fish.pos)
            dist = np.linalg.norm(vec_between)
            if dist == 0:
                dist += 10 ** -5
            unit = vec_between / dist
            repulse = (repulse_factor/dist) * unit
            overall_vec += repulse
        # overall_vec = overall_vec/np.linalg.norm(overall_vec)
        self.set_facing(np.arctan2(*overall_vec))
        self.speed = max(self.spd_min, min(self.spd_max, self.spd_base * np.linalg.norm(overall_vec)))

    def __pos_norm(self, vec):
        n = vec.copy()
        n[0] = Fish.__NORM_FAC * (n[0]/self.dim[0])
        n[1] = Fish.__NORM_FAC * (n[1]/self.dim[1])
        return n