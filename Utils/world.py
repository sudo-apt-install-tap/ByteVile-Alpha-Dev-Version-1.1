import Utils.procgen as procgen

WORLD_WIDTH = 40
WORLD_HEIGHT = 20

def create_world():
    """
    Creates and returns the intital world stage
    """

    world_map = procgen.generate_world(WORLD_WIDTH, WORLD_HEIGHT)

    world={
        "map":world_map,
        "width":WORLD_WIDTH,
        "height":WORLD_HEIGHT,
        "player": {
            "x":0,
            "y":0
        }
    }

    place_player(world)
    return world

def place_player(world):
    for y, row in enumerate(world["map"]):
        for x, tile in enumerate(row):
            if tile == procgen.FLOOR:
                world["player"]["x"]=x
                world["player"]["y"]=y
                return
