import time
import sys

def slow_print(text, delay=0.03):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()

def start_game():
    print("\n[Booting story engine...]\n")
    print("You wake up in a broken system. The air hums with static.")
    print("Something deep in the code calls your name.\n")
    print("(This is placeholder story logic for now.)\n")
