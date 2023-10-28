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
from utilities import aspect_ratio

def main():
    pg.display.init()
    scale = 50
    pg.mouse.set_visible(True)
    pg.mouse.set_cursor(*pg.cursors.diamond)
    screen_dim = pg.display.Info()
    screen_dim = aspect_ratio((screen_dim.current_w, screen_dim.current_h))
    screen_dim = screen_dim[0]*scale, screen_dim[1]*scale
    tank = FishTank(15, screen_dim)
    screen = pg.display.set_mode(screen_dim, flags=pg.FULLSCREEN | pg.SCALED)
    pg.display.set_caption("Amoeba Tank")
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
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == pg.BUTTON_LEFT:
                        tank.drop_food(np.array(event.pos, dtype=float))
                    elif event.button == pg.BUTTON_RIGHT:
                        tank.pick_food()
                elif event.type == pg.MOUSEMOTION and 1 in event.buttons:
                    tank.drop_food(np.array(event.pos, dtype=float))
                elif event.type == pg.KEYDOWN and event.key in [pg.K_q, pg.K_ESCAPE]:
                    running = False
                    
                    
    pg.display.quit()
    
if __name__ == '__main__':
    main()