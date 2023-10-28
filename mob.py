# File: mob.py
# Author: Michael Huelsman
# Created On: 25 Oct 2023
# Lisence: GNU GPLv3
# Purpose:
#   A simple mobile object, with a facing.

import pygame as pg
import numpy as np
from math import degrees, radians
from utilities import ang_to_vec


class Mobile:
    def __init__(self, pos: np.ndarray, speed: float, sprite: pg.Surface, dim: (int, int), init_facing: float = 0.0):
        self.pos = pos
        self.facing = init_facing
        self.speed = speed
        self.base_facing = init_facing
        self.sprite = sprite
        self.dim = dim

    def update(self, delta: float):
        self.pos += delta * self.speed * ang_to_vec(self.facing)
        self.pos[0] = min(max(0, self.pos[0]), self.dim[0])
        self.pos[1] = min(max(0, self.pos[1]), self.dim[1])

    def draw(self, surface: pg.Surface):
        rotated_sprite = pg.transform.rotate(self.sprite, degrees(self.facing-self.base_facing) - 90)
        placement = int(self.pos[0] - rotated_sprite.get_width()/2), int(self.pos[1] - rotated_sprite.get_height()/2)
        surface.blit(rotated_sprite, placement)
        
    def face_towards(self, loc):
        self.facing = np.math.atan2(*(loc - self.pos))
    
    def set_facing(self, angle):
        self.facing = angle