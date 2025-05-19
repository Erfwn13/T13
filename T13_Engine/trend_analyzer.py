# trend_analyzer.py

import json
import os

EMO_LOG_FILE = "data/emotion_log.json"

def load_emotion_log():
    if not os.path.exists(EMO_LOG_FILE):
        return []
    with open(EMO_LOG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def analyze_trend(last_n=5):
    log = load_emotion_log()
    if len(log) < last_n:
        return "📉 داده کافی برای تحلیل روند وجود ندارد.", {}

    recent = log[-last_n:]
    trend = {
        "joy": sum(e["joy"] for e in recent) / last_n,
        "stress": sum(e["stress"] for e in recent) / last_n,
        "hope": sum(e["hope"] for e in recent) / last_n,
        "fear": sum(e["fear"] for e in recent) / last_n,
        "energy": sum(e["energy"] for e in recent) / last_n
    }

    return interpret_trend(trend), trend

def interpret_trend(avg):
    suggestions = []

    if avg["stress"] > 7:
        suggestions.append("📛 افزایش استرس در روزهای اخیر – پیشنهاد: استراحت یا کاهش فشار کاری")
    if avg["hope"] < 4:
        suggestions.append("🕳️ افت امید – پیشنهاد: تمرکز بر موفقیت‌های قبلی یا اهداف کوچک‌تر")
    if avg["joy"] >= 8 and avg["energy"] >= 8:
        suggestions.append("✅ حالت مثبت پایدار – ادامه بده همین‌طوری!")

    if not suggestions:
        suggestions.append("📘 روند احساسی پایدار است – هیچ مورد بحرانی یافت نشد.")

    return suggestions
