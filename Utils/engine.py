import json
import Utils.textfx as fx
import Utils.save_system as save

CURRENT_NODE = "intro"

def load_story():
    with open("Data/story.json", "r") as f:
        return json.load(f)

def start_game():
    global CURRENT_NODE
    story = load_story()
    
    while True:
        node = story[CURRENT_NODE]
        fx.slow_print("\n" + node["text"] + "\n")
        
        if "choices" not in node or not node["choices"]:
            fx.slow_print("The story ends here. Type 'exit' to quit or 'start' to restart.\n")
            break
        
        fx.slow_print("Choices:")
        for key in node["choices"]:
            fx.slow_print(f"- {key}")
        
        choice = input(">> ").strip().lower()
        
        if choice == "exit":
            fx.slow_print("\nShutting down... see you next boot.\n")
            break
        elif choice in node["choices"]:
            CURRENT_NODE = node["choices"][choice]
            save.save_game({"current_node": CURRENT_NODE})
        else:
            fx.slow_print("Invalid choice. Try again.")
