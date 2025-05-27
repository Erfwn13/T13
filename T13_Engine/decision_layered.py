# decision_layered.py

from self_upgrade_engine import analyze_for_upgrade


def layered_decision(feelings):
    """
    شبیه‌سازی تصمیم‌های چندمرحله‌ای بر اساس احساسات
    """
    decisions = ["ادامه پروژه", "استراحت"]

    if upgrade_suggestions := analyze_for_upgrade(feelings):
        decisions.append({"title": "ارتقا سیستم", "suggestions": upgrade_suggestions})

    return decisions
