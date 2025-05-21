# emotion_stack.py

import json
import os
from datetime import datetime

EMO_LOG_FILE = "data/emotion_log.json"

# بررسی پوشه و فایل
if not os.path.exists("data"):
    os.makedirs("data")

if not os.path.exists(EMO_LOG_FILE):
    with open(EMO_LOG_FILE, "w", encoding="utf-8") as f:
        json.dump([], f, indent=2, ensure_ascii=False)

def analyze_emotion(input_data):
    emo_score = {
        "joy": input_data.get("joy", 5),
        "stress": input_data.get("stress", 5),
        "hope": input_data.get("hope", 5),
        "fear": input_data.get("fear", 5),
        "energy": input_data.get("energy", 5),
        "timestamp": datetime.now().isoformat()
    }

    save_to_log(emo_score)
    return emo_score

def save_to_log(score):
    with open(EMO_LOG_FILE, "r+", encoding="utf-8") as f:
        data = json.load(f)
        data.append(score)
        f.seek(0)
        json.dump(data, f, indent=2, ensure_ascii=False)

def adaptive_reaction(score):
    if score["stress"] > 7:
        return "🔴 وضعیت پرتنش! پیشنهاد می‌کنم استراحت کنی."
    elif score["joy"] >= 8 and score["energy"] >= 8:
        return "🟢 انرژی و شادی در اوجه! ادامه بده!"
    elif score["hope"] < 4:
        return "🟡 سطح امید پایین گزارش شده. آیا کمکی از من برمیاد؟"
    else:
        return "⚪ وضعیت احساسی پایدار."

class EmotionStack:
    def __init__(self, max_size=200):
        self.emotions = []
        self.max_size = max_size

    def add_emotion(self, emotion, intensity):
        entry = {"emotion": emotion, "intensity": intensity, "timestamp": datetime.now()}
        self.emotions.append(entry)
        if len(self.emotions) > self.max_size:
            self.emotions.pop(0)

    def get_recent_emotions(self, count=5):
        return self.emotions[-count:]