import os
import sys
import tty
import termios

from Utils import world, movement, textfx, procgen

# Terminal input

def getch():
    """
    Reads single charecters from stdin
    """
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

# Render world

def render(world_state):
    os.system("clear")
    wmap = [list(row) for row in world_state["map"]]

    px = world_state["player"]["x"]
    py = world_state["player"]["y"]
    wmap[py][px]="@"
    # Level label in the lower-right quadrant
    try:
        lvl = world_state.get("level", 1)
        max_lvl = world_state.get("max_levels", 150)
        label = f"Lvl {lvl}/{max_lvl}"

        width = world_state.get("width", len(wmap[0]) if wmap else 0)
        height = world_state.get("height", len(wmap))

        # target position in lower-right quadrant
        tx = max(0, int(width * 3 / 4))
        ty = max(0, int(height * 3 / 4))

        # ensure label fits horizontally; if not, shift left
        if tx + len(label) > width:
            tx = max(0, width - len(label) - 1)

        # ensure ty within bounds
        if ty >= height:
            ty = height - 1

        # overlay label without overwriting the player '@'
        for i, ch in enumerate(label):
            lx = tx + i
            if 0 <= ty < height and 0 <= lx < width:
                if wmap[ty][lx] != "@":
                    wmap[ty][lx] = ch
    except Exception:
        # if anything goes wrong, skip the label silently
        pass

    for row in wmap:
        print("".join(row))

# Direction Mapping

DIRECTION ={
    "w": (0,-1),
    "s": (0,1),
    "a": (-1,0),
    "d": (1,0)
}

# Main Loop

def main():
    world_state=world.create_world()

    textfx.slow_print("> Welcome toByteVile. Use WASD to move. Press Q to quit")

    while True:
        render(world_state)
        key = getch().lower()

        if key == "q":
            textfx.slow_print("\n> Shutting down........\n")
            break

        if key not in DIRECTION:
            continue

        dx, dy = DIRECTION[key]
        result = movement.attempt_move(world_state, world_state["player"], dx, dy)

        # POI and special tile handling
        if result["moved"]:
            # If player stepped onto a door, handle level progression
            if result.get("tile") == procgen.DOOR:
                # If already at or beyond max levels, the dungeon ends
                if world_state.get("level", 1) >= world_state.get("max_levels", 150):
                    textfx.slow_print("> You step through the final door... the dungeon yields to you.\n")
                    textfx.slow_print("> Victory. Exiting...\n")
                    break

                textfx.slow_print("> You step through the door...\n")
                world.next_level(world_state)
                # re-render the newly generated level
                render(world_state)
                continue

            # Check for POIs at the new position
            px, py = result["new_pos"]
            poi = world.get_poi(world_state, px, py)
            if poi:
                # show POI text
                textfx.slow_print(f"> {poi.get('text','You see something interesting.') }\n")
                # remove if it's a one-time POI
                if poi.get("once"):
                    world.remove_poi(world_state, px, py)

        # Tile-based example (water)
        if result["tile"] == "~" and result["moved"]:
            textfx.slow_print("> You step into cold water. \n")

# Entrypoint

if __name__=="__main__":
    main()
    