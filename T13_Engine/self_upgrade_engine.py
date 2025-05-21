import json
from datetime import datetime, timedelta
import time
import threading

def save_version(version, performance_metrics=None):
    version_file = "c:\\Developer\\T13_Project\\T13\\data\\version.json"
    record = {
        "version": version,
        "timestamp": datetime.now().isoformat(),
        "performance": performance_metrics or {}
    }
    try:
        with open(version_file, "w", encoding="utf-8") as f:
            json.dump(record, f, ensure_ascii=False, indent=4)
        print("نسخه جدید سیستم با معیارهای عملکردی ثبت شد.")
    except Exception as e:
        print(f"⚠️ خطا در ثبت نسخه: {e}")

def analyze_for_upgrade(emotion_score):
    upgrades = []
    if emotion_score.get("stress", 0) > 7:
        upgrades.append("پیشنهاد ارتقا ماژول رفتار برای کاهش استرس")
    if emotion_score.get("hope", 0) < 4:
        upgrades.append("افزایش قابلیت انگیزشی در ShadowBoost")
    if emotion_score.get("energy", 0) < 3:
        upgrades.append("بهینه‌سازی چرخه حافظه برای مصرف کمتر")
    return upgrades

def log_upgrade_suggestion(suggestions):
    log_file = "c:\\Developer\\T13_Project\\T13\\data\\upgrade_log.json"
    record = {"timestamp": datetime.now().isoformat(), "suggestions": suggestions}
    try:
        with open(log_file, "r+", encoding="utf-8") as f:
            logs = json.load(f)
            logs.append(record)
            f.seek(0)
            json.dump(logs, f, ensure_ascii=False, indent=4)
    except Exception:
        with open(log_file, "w", encoding="utf-8") as f:
            json.dump([record], f, ensure_ascii=False, indent=4)
    print("پیشنهادات ارتقا ثبت شدند.")

def auto_refactor():
    print("🔄 شروع بازنویسی خودکار سیستم...")
    time.sleep(1)  # شبیه‌سازی زمان پردازش
    print("✅ بازنویسی خودکار سیستم به پایان رسید.")

def upgrade_scheduler(interval_minutes=10):
    def scheduled_task():
        while True:
            next_run = datetime.now() + timedelta(minutes=interval_minutes)
            print(f"⏳ اجرای بعدی بررسی در ساعت {next_run.time()}")
            time.sleep(interval_minutes * 60)
            
            print("🚀 شروع بررسی دوره‌ای ارتقا...")
            # در اینجا سیستم می‌تواند وضعیت لحظه‌ای خود را بسنجید، به عنوان نمونه:
            sample_emotion_score = {"stress": 8, "hope": 3, "energy": 2}
            suggestions = analyze_for_upgrade(sample_emotion_score)
            if suggestions:
                log_upgrade_suggestion(suggestions)
            else:
                print("✅ سیستم پایدار است؛ ارتقا نیاز نیست.")
            
            auto_refactor()
    threading.Thread(target=scheduled_task, daemon=True).start()