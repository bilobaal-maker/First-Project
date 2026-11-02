import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

os.makedirs(DATA_DIR, exist_ok=True)

TASKS_FILE = os.path.join(DATA_DIR, "tasks.json")
USER_FILE = os.path.join(DATA_DIR, "user.json")
SETTINGS_FILE = os.path.join(DATA_DIR, "settings.json")


def load_json(file_path, default):
    if not os.path.exists(file_path):
        save_json(default, file_path)
        return default

    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print(f"Error: Corrupted file {file_path}")
        return default


def save_json(data, file_path):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)


# -----------------------
# TASKS
# -----------------------

def load_tasks():
    return load_json(TASKS_FILE, [])


def save_tasks(tasks):
    save_json(tasks, TASKS_FILE)


# -----------------------
# USER
# -----------------------

def load_user():
    return load_json(USER_FILE, {
        "name": "Default User",
        "points": 0,
        "level": 1,
        "achievements": [],
        "unlocked_features": []
    })


def save_user(user_data):
    save_json(user_data, USER_FILE)


# -----------------------
# SETTINGS
# -----------------------

def load_settings():
    return load_json(SETTINGS_FILE, {
        "theme": "light",
        "scheduler_unlocked": False
    })


def save_settings(settings):
    save_json(settings, SETTINGS_FILE)

