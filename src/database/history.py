import json
import os
from datetime import datetime

# Path: root/data/history.json
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
HISTORY_FILE = os.path.join(DATA_DIR, "history.json")

# Make sure /data folder exists
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Create history.json if missing
if not os.path.isfile(HISTORY_FILE):
    with open(HISTORY_FILE, "w") as f:
        json.dump([], f)

def save_history(entry: dict):
    """Append a new record to history.json"""
    with open(HISTORY_FILE, "r") as f:
        logs = json.load(f)

    entry["timestamp"] = datetime.utcnow().isoformat()
    logs.append(entry)

    with open(HISTORY_FILE, "w") as f:
        json.dump(logs, f, indent=4)

def load_history():
    """Return all saved history entries"""
    with open(HISTORY_FILE, "r") as f:
        return json.load(f)
