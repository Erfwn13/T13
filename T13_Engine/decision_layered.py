# decision_layered.py

from self_upgrade_engine import analyze_for_upgrade

def layered_decision(feelings):
    """
    شبیه‌سازی تصمیم‌های چندمرحله‌ای بر اساس احساسات
    """
    decisions = []
    
    # بخش تولید تصمیم های اولیه (مثال فرضی)
    decisions.append("ادامه پروژه")
    decisions.append("استراحت")
    
    # بررسی پیشنهادات ارتقا بر اساس احساسات
    upgrade_suggestions = analyze_for_upgrade(feelings)
    if upgrade_suggestions:
        decisions.append({"title": "ارتقا سیستم", "suggestions": upgrade_suggestions})
    
    return decisions