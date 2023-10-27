# File: mob.py
# Author: Michael Huelsman
# Created On: 25 Oct 2023
# Lisence: GNU GPLv3
# Purpose:
#   A simple mobile object, with a facing.

import pygame as pg
import numpy as np
from math import degrees
from utilities import ang_to_vec

class Mobile:
    def __init__(self, pos: np.ndarray, speed: float, sprite: pg.Surface, init_facing: float = 0.0):
        self.pos = pos
        self.facing = init_facing
        self.speed = speed
        self.base_facing = init_facing
        self.sprite = sprite

    def update(self):
        self.pos += self.speed * ang_to_vec(self.facing)

    def draw(self, surface: pg.Surface):
        rotated_sprite = pg.transform.rotate(self.sprite, degrees(self.facing-self.base_facing))
        placement = int(self.pos[0] - rotated_sprite.get_width()/2), int(self.pos[1] - rotated_sprite.get_height()/2)
        surface.blit(rotated_sprite, placement)
        
    def face_towards(self, loc):
        self.facing = np.math.atan2(loc - self.pos)
    
    def set_facing(self, angle):
        self.facing = angle