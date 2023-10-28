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
from utilities import ang_to_vec


class Fish(Mobile):
    def __init__(self, pos: np.ndarray, screen_dim: (int, int)):
        super(Fish, self).__init__(pos, 50, pg.image.load("fish_sprite.png"), screen_dim)
        self.goal = self.__random_goal()
    
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
        repulse_factor = 15 * self.sprite.get_width()
        attraction_factor = 50
        overall_vec = attraction_factor * ((self.goal - self.pos)/np.linalg.norm(self.goal - self.pos))
        for fish in fishes:
            if self == fish:
                continue
            vec_between = self.pos - fish.pos
            dist = np.linalg.norm(vec_between)
            if dist == 0:
                dist += 10 ** -5
            unit = vec_between / dist
            repulse = (repulse_factor/dist) * unit
            overall_vec += repulse
        overall_vec = overall_vec/np.linalg.norm(overall_vec)
        self.set_facing(np.arctan2(*overall_vec))
