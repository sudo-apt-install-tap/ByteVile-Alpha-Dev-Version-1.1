import Utils.procgen as procgen
import os
import json
import random

WORLD_WIDTH = 40
WORLD_HEIGHT = 20

def create_world():
    """
    Creates and returns the intital world stage
    """
    # store a stable base seed so different levels can be generated deterministically
    base_seed = procgen.worldseed

    # create world dict and initialize level bookkeeping
    world = {
        "map": None,
        "width": WORLD_WIDTH,
        "height": WORLD_HEIGHT,
        "player": {"x": 0, "y": 0},
        # level bookkeeping
        "level": 1,
        "max_levels": 150,
        "levels": {},
        "seed_base": base_seed
    }

    # generate the first level and store it
    first_map = generate_level(world, 1)
    world["map"] = first_map
    # place player and POIs for level 1
    place_player(world)
    place_default_pois(world)

    # cache level 1 map
    world["levels"][1] = first_map

    return world


def add_poi(world, x, y, poi):
    """Adds a POI dict at x,y. POI is a dict containing keys like id, name, text, story_node, once"""
    if "pois" not in world:
        world["pois"] = {}
    world["pois"][(x, y)] = poi


def get_poi(world, x, y):
    """Returns a POI dict at the given coordinates or None"""
    return world.get("pois", {}).get((x, y))


def remove_poi(world, x, y):
    """Removes a POI at coords, if present"""
    if "pois" in world and (x, y) in world["pois"]:
        del world["pois"][(x, y)]


def place_default_pois(world, count=6):
    """Places a small set of example POIs on floor tiles. Deterministic placement using procgen.worldseed."""
    floor_positions = []
    for y, row in enumerate(world["map"]):
        for x, tile in enumerate(row):
            if tile == procgen.FLOOR:
                floor_positions.append((x, y))

    if not floor_positions:
        return

    # Deterministic RNG
    rng = random.Random(procgen.worldseed)

    # Allow external POI configuration via Data/pois.json (optional)
    sample_pois = None
    data_pois_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Data", "pois.json")
    if os.path.exists(data_pois_path):
        try:
            with open(data_pois_path, "r", encoding="utf-8") as fh:
                sample_pois = json.load(fh)
        except Exception:
            sample_pois = None

    if not sample_pois:
        sample_pois = [
            {"id": "terminal", "name": "Flickering Terminal", "text": "A terminal pulses with a flashing line: INIT: REMEMBER.", "story_node": "terminal", "once": False},
            {"id": "pond", "name": "Shallow Pond", "text": "Cold water laps at your boots.", "story_node": None, "once": False},
            {"id": "scrap_heap", "name": "Scrap Heap", "text": "A pile of scrap and a torn logbook peek through the rubble.", "story_node": "scrap_heap", "once": True},
            {"id": "market_stall", "name": "Quiet Stall", "text": "An empty stall hums with dormant code.", "story_node": "market", "once": False},
            {"id": "warning_hatch", "name": "Sealed Hatch", "text": "A hatch engraved with: 'Wake at your own risk.'", "story_node": "core_path", "once": True},
            {"id": "lantern_vire", "name": "Lantern-construct", "text": "A small construct named Vire turns toward you, its lantern eyes flicker.", "story_node": "market", "once": False}
        ]

    rng.shuffle(floor_positions)

    # Place up to `count` POIs by sampling positions or using provided coords
    placed = 0
    used_positions = set()
    for poi in sample_pois:
        if placed >= count:
            break

        # If POI provides explicit coordinates, try to use them
        px = poi.get("x")
        py = poi.get("y")
        if isinstance(px, int) and isinstance(py, int):
            if 0 <= py < len(world["map"]) and 0 <= px < len(world["map"][0]) and world["map"][py][px] == procgen.FLOOR:
                if (px, py) not in used_positions:
                    add_poi(world, px, py, poi)
                    used_positions.add((px, py))
                    placed += 1
                    continue

        # Otherwise pick an unused floor position from shuffled list
        while floor_positions:
            pos = floor_positions.pop()
            if pos in used_positions:
                continue
            add_poi(world, pos[0], pos[1], poi)
            used_positions.add(pos)
            placed += 1
            break

def place_player(world):
    for y, row in enumerate(world["map"]):
        for x, tile in enumerate(row):
            if tile == procgen.FLOOR:
                world["player"]["x"]=x
                world["player"]["y"]=y
                return


def next_level(world, num_rooms=None):
    """Generate the next level (a new map) and place the player at its entrance.

    This replaces `world['map']` with a fresh procgen map, increments
    `world['level']`, clears POIs and places new default POIs.
    """
    # bump level and enforce max_levels externally (caller should check)
    world.setdefault("level", 1)
    world["level"] += 1
    lvl = world["level"]

    # If we already generated this level, load cached map
    if lvl in world.get("levels", {}):
        new_map = world["levels"][lvl]
    else:
        new_map = generate_level(world, lvl, num_rooms)
        world.setdefault("levels", {})[lvl] = new_map

    # Replace map and reset POIs
    world["map"] = new_map
    if "pois" in world:
        del world["pois"]

    # place player and POIs for the new level
    place_player(world)
    place_default_pois(world)

    return world


def generate_level(world, level_num, num_rooms=None):
    """Generate a level map for `level_num` using a level-aware seed.

    This temporarily adjusts `procgen.worldseed` so the per-tile `_rng`
    behavior produces different maps for each level deterministically
    from `world['seed_base']`.
    """
    orig_seed = getattr(procgen, "worldseed", None)
    base = world.get("seed_base", orig_seed if orig_seed is not None else 1337)
    # use a multiplier to separate level seeds
    level_seed = int(base) + int(level_num) * 10007
    procgen.worldseed = level_seed

    try:
        if num_rooms is None:
            m = procgen.generate_world(world["width"], world["height"])
        else:
            m = procgen.generate_world(world["width"], world["height"], num_rooms)
    finally:
        # restore original module seed
        if orig_seed is not None:
            procgen.worldseed = orig_seed

    return m
