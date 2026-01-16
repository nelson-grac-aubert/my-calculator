import json
import os

HISTORY_FILE = "history.json"
history = []

def load_history():
    """ Gets current state of history from .json file """
    global history
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return[]

def save_history(history):
    """ Save history after new entry, after clearing """
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4)