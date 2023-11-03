# File: food.py
# Author: Michael Huelsman
# Created On: 25 Oct 2023
# Lisence: GNU GPLv3
# Purpose:
#   A simple static object for Fish to eat.

import numpy as np
import pygame as pg

class Food:
    __FOOD_COLOR = (50, 230, 50)
    __FOOD_LIMIT = 5
    def __init__(self, pos: np.ndarray):
        self.pos = pos
        self.valid = True
        self.spoil = Food.__FOOD_LIMIT
    
    def draw(self, surf: pg.Surface):
        pg.draw.circle(surf, Food.__FOOD_COLOR, self.pos, 5)

    def eat(self):
        self.valid = False

    def update(self, delta):
        self.spoil -= delta
