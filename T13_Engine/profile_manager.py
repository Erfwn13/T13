# profile_manager.py

import os
import json

PROFILE_DIR = "profiles"

def save_profile(name, data):
    if not os.path.exists(PROFILE_DIR):
        os.makedirs(PROFILE_DIR)

    filepath = os.path.join(PROFILE_DIR, f"{name}.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return f"✅ Profile '{name}' saved successfully."

def load_profile(name):
    filepath = os.path.join(PROFILE_DIR, f"{name}.json")
    if not os.path.exists(filepath):
        print("❌ Profile not found!")
        return None, "Profile not found."

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    print("✅ Profile loaded successfully.")
    return data, f"Profile '{name}' loaded."

def list_profiles():
    if not os.path.exists(PROFILE_DIR):
        return []

    files = os.listdir(PROFILE_DIR)
    profiles = [f.replace(".json", "") for f in files if f.endswith(".json")]
    return profiles
