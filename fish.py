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

class Fish(Mobile):
    def __init__(self, pos: np.ndarray, screen_dim: (int, int)):
        super(Fish, self).__init__(pos, 5, pg.Surface((10, 10)))
        self.screen_dim = screen_dim
        self.goal = self.__random_goal() 

    def __random_goal(self):
        return randrange(0, self.screen_dim[0]), randrange(0, self.screen_dim[1])