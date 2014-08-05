# magic spells to include files from outer dir
import os
import sys
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from include.python_stl import *
from include.common import *
import random
import math


def main_implementation(ai_state, world_state):
    # Just world
    return (0, 2)

def main(ai_state, world):
    return main_implementation(ai_state, world)
