# File: mob.py
# Author: Michael Huelsman
# Created On: 25 Oct 2023
# Lisence: GNU GPLv3
# Purpose:
#   A simple mobile object, with a facing.

import pygame as pg
import numpy as np
from math import degrees, radians, sin, cos
from utilities import ang_to_vec


class Mobile:
    def __init__(self, pos: np.ndarray, velocity: np.ndarray, sprite: pg.Surface, dim: (int, int)):
        self.pos = pos
        self.velocity = velocity
        self.sprite = sprite
        self.dim = dim

    def update(self, delta: float):
        self.pos += delta * self.velocity
        self.pos[0] = min(max(0, self.pos[0]), self.dim[0])
        self.pos[1] = min(max(0, self.pos[1]), self.dim[1])

    def draw(self, surface: pg.Surface):
        rotated_sprite = pg.transform.rotate(self.sprite, self.__get_facing())
        placement = int(self.pos[0] - rotated_sprite.get_width()/2), int(self.pos[1] - rotated_sprite.get_height()/2)
        surface.blit(rotated_sprite, placement)
        
    def face_towards(self, loc):
        return np.linalg.norm(self.velocity) * ang_to_vec(np.math.atan2(*(loc - self.pos)))
    
    def __get_facing(self):
        return degrees(np.math.atan2(*self.velocity)) - 90.0
    