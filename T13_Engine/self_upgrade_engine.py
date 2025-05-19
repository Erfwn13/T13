# self_upgrade_engine.py

import json
import os
from datetime import datetime

VERSION_FILE = "data/version.json"
UPGRADE_LOG = "data/upgrade_log.json"

# اطمینان از وجود پوشه و فایل‌ها
for file_path in [VERSION_FILE, UPGRADE_LOG]:
    dir_name = os.path.dirname(file_path)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump([], f, indent=2, ensure_ascii=False)

def save_version(version_str="T13.3"):
    """ذخیره نسخه فعلی"""
    data = {
        "version": version_str,
        "timestamp": datetime.now().isoformat()
    }
    with open(VERSION_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def analyze_for_upgrade(emotion_score):
    """تحلیل ساده برای پیشنهاد ارتقا بر اساس احساسات"""
    upgrades = []
    if emotion_score["stress"] > 7:
        upgrades.append("پیشنهاد ارتقا ماژول رفتار برای کاهش استرس")
    if emotion_score["hope"] < 4:
        upgrades.append("افزایش قابلیت انگیزشی در ShadowBoost")
    if emotion_score["energy"] < 3:
        upgrades.append("بهینه‌سازی چرخه حافظه برای مصرف کمتر")

    return upgrades

def log_upgrade_suggestion(upgrades):
    with open(UPGRADE_LOG, "r+", encoding="utf-8") as f:
        data = json.load(f)
        data.append({
            "time": datetime.now().isoformat(),
            "suggestions": upgrades
        })
        f.seek(0)
        json.dump(data, f, indent=2, ensure_ascii=False)
