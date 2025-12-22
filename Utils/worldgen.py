worldseed=1337

import random

def _rng(x,y):
    return random.Random(worldseed + x * 9999 + y * 8888)

def worldgen():
    r=_rng
    return r