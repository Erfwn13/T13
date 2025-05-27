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
        "energy": sum(e["energy"] for e in recent) / last_n,
    }

    return interpret_trend(trend), trend


def interpret_trend(avg):
    suggestions = []

    if avg["stress"] > 7:
        suggestions.append(
            "📛 افزایش استرس در روزهای اخیر – پیشنهاد: استراحت یا کاهش فشار کاری"
        )
    if avg["hope"] < 4:
        suggestions.append(
            "🕳️ افت امید – پیشنهاد: تمرکز بر موفقیت‌های قبلی یا اهداف کوچک‌تر"
        )
    if avg["joy"] >= 8 and avg["energy"] >= 8:
        suggestions.append("✅ حالت مثبت پایدار – ادامه بده همین‌طوری!")

    if not suggestions:
        suggestions.append("📘 روند احساسی پایدار است – هیچ مورد بحرانی یافت نشد.")

    return suggestions


class TrendAnalyzer:
    def __init__(self, conversation_history):
        self.conversation_history = conversation_history

    def analyze_trends(self):
        """
        تحلیل روندهای احساسی بر اساس تاریخچه مکالمات
        """
        sentiment_scores = [
            entry.get("sentiment", 0)
            for entry in self.conversation_history
            if "sentiment" in entry
        ]
        if not sentiment_scores:
            return "روند مشخصی یافت نشد."

        avg_sentiment = sum(sentiment_scores) / len(sentiment_scores)
        if avg_sentiment > 0.5:
            return "روند کلی مثبت است. ادامه بده!"
        elif avg_sentiment < -0.5:
            return "روند کلی منفی است. شاید نیاز به تغییر داشته باشی."
        else:
            return "روند کلی خنثی است. شاید بخوای چیز جدیدی امتحان کنی."
