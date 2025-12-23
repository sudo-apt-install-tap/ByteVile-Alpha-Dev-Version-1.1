import Utils.engine as engine
import Utils.save_system as save
import Utils.textfx as fx
from Utils.procgen import generate_world, print_world

def main():
    fx.clear()
    fx.banner()
    print("ByteVile Alpha Dev Version 1.1\n")
    print("Welcome back, wanderer. The system remembers you.\n")

    save.init_save_dir()

    while True:
        choice = input(">> ").strip().lower()

        if choice in ["exit", "quit"]:
            print("\nShutting down... see you next boot.\n")
            break

        elif choice == "start":
            engine.start_game()

        elif choice == "load":
            data = save.load_game()
            if data:
                print("Loaded previous state.")
            else:
                print("No save file found.")

        elif choice == "save":
            save.save_game({"example": "game_state"})
            print("Game saved.")
        
        elif choice == "world":
            world = generate_world(40, 20)
            print_world(world)
        else:
            print("Commands: start | save | load | exit")

if __name__ == "__main__":
    main()
