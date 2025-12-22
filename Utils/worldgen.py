import random

#tiles and seed config!!

wordseed = 1337
 
WALL = "#"
FLOOR = '.'
WATER = '~'
DOOR = '|'

#RNG FUCTION

def _rng(x,y):
    """A deterministic Random Generator For A Coordinates Or Room Index."""
    return random.Random(worldseed + x * 9999 + y *8888)

#Room Generation:-

def generate_room(x0, y0, rw, rh, world):
    """Fills the Room With Symbols"""
    