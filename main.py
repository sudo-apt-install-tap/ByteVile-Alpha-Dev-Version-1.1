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

        # POI E.G

        if result["tile"] == "~" and result["moved"]:
            textfx.slow_print("> You step into cold water. \n")

# Entrypoint

if __name__=="__main__":
    main()
    