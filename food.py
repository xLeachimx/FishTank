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
    def __init__(self, pos: np.ndarray):
        self.pos = pos
    
    def draw(self, surf: pg.Surface):
        pass