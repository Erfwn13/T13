# profile_manager.py

import json
import os

PROFILE_DIR = "profiles"


def save_profile(name, data):
    if not os.path.exists(PROFILE_DIR):
        os.makedirs(PROFILE_DIR)
    # مقداردهی پیش‌فرض کلیدهای مدل و زبان
    if "model" not in data:
        data["model"] = "auto"
    if "lang" not in data:
        data["lang"] = "fa"
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
    # مقداردهی پیش‌فرض اگر کلیدها نبودند
    if "model" not in data:
        data["model"] = "auto"
    if "lang" not in data:
        data["lang"] = "fa"
    print("✅ Profile loaded successfully.")
    return data, f"Profile '{name}' loaded."


def list_profiles():
    if not os.path.exists(PROFILE_DIR):
        return []

    files = os.listdir(PROFILE_DIR)
    return [f.replace(".json", "") for f in files if f.endswith(".json")]


def export_profile(name, export_path):
    filepath = os.path.join(PROFILE_DIR, f"{name}.json")
    if not os.path.exists(filepath):
        return False, "Profile not found."
    try:
        with open(filepath, "r", encoding="utf-8") as src, open(
            export_path, "w", encoding="utf-8"
        ) as dst:
            dst.write(src.read())
        return True, f"Profile '{name}' exported to {export_path}"
    except Exception as e:
        return False, str(e)


def import_profile(import_path):
    if not os.path.exists(import_path):
        return False, "Import file not found."
    try:
        name = os.path.splitext(os.path.basename(import_path))[0]
        dest_path = os.path.join(PROFILE_DIR, f"{name}.json")
        with open(import_path, "r", encoding="utf-8") as src, open(
            dest_path, "w", encoding="utf-8"
        ) as dst:
            dst.write(src.read())
        return True, f"Profile '{name}' imported."
    except Exception as e:
        return False, str(e)
