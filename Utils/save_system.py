import json, os

SAVE_PATH = "Saves/save.json"

def init_save_dir():
    if not os.path.exists("Saves"):
        os.makedirs("Saves")

def save_game(data):
    with open(SAVE_PATH, "w") as f:
        json.dump(data, f, indent=2)

def load_game():
    if not os.path.exists(SAVE_PATH):
        return None
    with open(SAVE_PATH, "r") as f:
        return json.load(f)
