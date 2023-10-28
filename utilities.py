# File: mob.py
# Author: Michael Huelsman
# Created On: 25 Oct 2023
# Lisence: GNU GPLv3
# Purpose:
#   A simple mobile object, with a facing.

import numpy as np
from math import sin, cos

def ang_to_vec(angle: float):
    return np.array([sin(angle), cos(angle)])