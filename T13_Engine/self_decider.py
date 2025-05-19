# self_decider.py

import json
import os
from decision_layered import layered_decision

LOG_FILE = "data/strategic_log.json"

def choose_best_path(feelings, goal="پیشرفت پروژه"):
    # دریافت مسیرهای پیشنهادی از سیستم قبلی
    options = layered_decision(feelings, goal)

    if not options:
        return None

    # انتخاب مسیر با کمترین ریسک و بهترین reward
    ranked = sorted(options, key=lambda x: (x["risk"].count("خطر") + len(x["risk"]), -len(x["reward"])))
    best = ranked[0]

    save_to_log(best, feelings)
    return best

def save_to_log(option, feelings):
    os.makedirs("data", exist_ok=True)
    entry = {
        "decision": option,
        "feelings": feelings,
        "timestamp": feelings.get("timestamp")
    }

    # اگر فایل لاگ وجود داشت، بخون
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = []

    data.append(entry)

    # ذخیره در فایل JSON
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
