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
        buffer = max(self.sprite.get_width(), self.sprite.get_height())
        self.pos[0] = min(max(buffer, self.pos[0]), self.dim[0]-buffer)
        self.pos[1] = min(max(buffer, self.pos[1]), self.dim[1]-buffer)

    def draw(self, surface: pg.Surface):
        facing = self.__get_facing()
        result_sprite = self.sprite
        if 90 <= facing <= 270:
            result_sprite = pg.transform.flip(result_sprite, False, True)
        result_sprite = pg.transform.rotate(result_sprite, facing)
        placement = int(self.pos[0] - result_sprite.get_width()/2), int(self.pos[1] - result_sprite.get_height()/2)
        surface.blit(result_sprite, placement)
        
    def face_towards(self, loc):
        return np.linalg.norm(self.velocity) * ang_to_vec(np.math.atan2(*(loc - self.pos)))
    
    def __get_facing(self):
        base_ang = degrees(np.math.atan2(*self.velocity)) - 90.0
        while base_ang < 0:
            base_ang += 360
        return base_ang
    