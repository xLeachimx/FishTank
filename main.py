# File: main.py
# Author: Michael Huelsman
# Created On: 25 Oct 2023
# Lisence: GNU GPLv3
# Purpose:
#   A simple little game AI tech demo for open houses.

import pygame as pg
import numpy as np
from fish_tank import FishTank
from time import perf_counter

def main():
    pg.display.init()
    tank = FishTank(20, (500, 500))
    screen = pg.display.set_mode((500, 500))
    pg.display.set_caption("Ameboa Tank")
    pg.display.set_icon(pg.image.load("fish_sprite.png"))
    running = True
    frame_delta = 1/30
    frame_timer = perf_counter()
    while running:
        if (perf_counter() - frame_timer) >= frame_delta:
            frame_timer = perf_counter()
            tank.update(frame_delta)
            tank.draw(screen)
            pg.display.flip()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    tank.drop_food(np.array(event.pos, dtype=float))
                if event.type == pg.MOUSEMOTION and 1 in event.buttons:
                    tank.drop_food(np.array(event.pos, dtype=float))
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 3:
                    tank.pick_food()
                if event.type == pg.FINGERMOTION:
                    tank.drop_food(np.array([event.x, event.y], dtype=float))
                if event.type == pg.FINGERUP:
                    tank.pick_food()
                    
    pg.display.quit()
    
if __name__ == '__main__':
    main()