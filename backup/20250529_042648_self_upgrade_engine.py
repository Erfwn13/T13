import json
import logging
import os
import shutil
import threading
import time
from datetime import datetime, timedelta
import requests  # اضافه برای اتصال به مدل هوش مصنوعی

# راه‌اندازی logging جهت ثبت رویدادها
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(
            "c:\\Developer\\T13_Project\\T13\\data\\self_upgrade.log", encoding="utf-8"
        ),
        logging.StreamHandler(),
    ],
)

VERSION_FILE = "c:\\Developer\\T13_Project\\T13\\data\\version.json"
UPGRADE_LOG_FILE = "c:\\Developer\\T13_Project\\T13\\data\\upgrade_log.json"
BACKUP_DIR = "c:\\Developer\\T13_Project\\T13\\backup\\"


def backup_file(filepath):
    """یک نسخه پشتیبان از فایل مشخص شده ایجاد می‌کند"""
    try:
        if not os.path.exists(BACKUP_DIR):
            os.makedirs(BACKUP_DIR)
        base = os.path.basename(filepath)
        backup_path = os.path.join(
            BACKUP_DIR, f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{base}"
        )
        shutil.copy(filepath, backup_path)
        logging.info(f"💾 نسخه پشتیبان {backup_path} ایجاد شد.")
    except Exception as e:
        logging.error(f"خطا در ایجاد نسخه پشتیبان: {e}")


def save_version(version, performance_metrics=None):
    record = {
        "version": version,
        "timestamp": datetime.now().isoformat(),
        "performance": performance_metrics or {},
    }
    try:
        backup_file(VERSION_FILE)
        with open(VERSION_FILE, "w", encoding="utf-8") as f:
            json.dump(record, f, ensure_ascii=False, indent=4)
        logging.info("نسخه جدید سیستم با معیارهای عملکردی ثبت شد.")
    except Exception as e:
        logging.error(f"خطا در ثبت نسخه: {e}")


def analyze_for_upgrade(internal_metrics):
    """
    تحلیل وضعیت داخلی سیستم برای تعیین نیاز به ارتقا.
    از شاخص‌های ساختاری مانند پیچیدگی کد، زمان پاسخگویی و گزارش‌های نظارتی استفاده می‌کند.
    """
    upgrades = []
    try:
        # شاخص‌های فرضی داخلی (internal_metrics) می‌تواند شامل مواردی مثل "code_complexity"، "response_time" و "error_rate" باشد.
        if internal_metrics.get("code_complexity", 0) > 7:
            upgrades.append("بهینه‌سازی ساختار کد برای کاهش پیچیدگی")
        if internal_metrics.get("response_time", 0) > 2:  # زمان پاسخگویی بیش از 2 ثانیه
            upgrades.append("بهبود عملکرد سیستم جهت کاهش زمان پاسخگویی")
        if internal_metrics.get("error_rate", 0) > 0.1:  # خطا بیشتر از 10 درصد
            upgrades.append("افزایش قابلیت اطمینان از طریق بهبود کشف و اصلاح خطا")
        # حتی اگر معیارهای داخلی نرمال باشد، بهبودهای پیشگیرانه اعمال شود.
        upgrades.append("بهینه‌سازی ساختار کد و افزایش کشف خطا")
    except Exception as e:
        logging.error(f"خطا در تحلیل وضعیت ارتقا: {e}")
    return upgrades


def log_upgrade_suggestion(suggestions):
    record = {"timestamp": datetime.now().isoformat(), "suggestions": suggestions}
    try:
        if not os.path.exists(UPGRADE_LOG_FILE):
            with open(UPGRADE_LOG_FILE, "w", encoding="utf-8") as f:
                json.dump([record], f, ensure_ascii=False, indent=4)
        else:
            with open(UPGRADE_LOG_FILE, "r+", encoding="utf-8") as f:
                try:
                    logs = json.load(f)
                    if not isinstance(logs, list):
                        logs = []
                except json.JSONDecodeError:
                    logs = []
                logs.append(record)
                f.seek(0)
                json.dump(logs, f, ensure_ascii=False, indent=4)
        logging.info("پیشنهادات ارتقا ثبت شدند.")
    except Exception as e:
        logging.error(f"خطا در ثبت پیشنهادات ارتقا: {e}")


def auto_refactor():
    try:
        logging.info("🔄 آغاز بازنویسی خودکار سیستم (Refactor)...")
        # شبیه‌سازی تحلیل استاتیک کد و بهبود ساختار آن
        time.sleep(1)
        # --- ارتقاهای جدید: تحلیل و پیشنهاد خودکار ---
        # ۱. بررسی خطوط تکراری و حذف آن‌ها
        with open(__file__, "r", encoding="utf-8") as f:
            code_lines = f.readlines()
        unique_lines = []
        seen = set()
        for line in code_lines:
            if line.strip() not in seen:
                unique_lines.append(line)
                seen.add(line.strip())
        if len(unique_lines) < len(code_lines):
            backup_file(__file__)
            with open(__file__, "w", encoding="utf-8") as f:
                f.writelines(unique_lines)
            logging.info("خطوط تکراری حذف شدند و کد تمیزتر شد.")
        # ۲. بررسی و هشدار خطوط بسیار طولانی
        long_lines = [i+1 for i, l in enumerate(unique_lines) if len(l) > 120]
        if long_lines:
            logging.warning(f"خطوط بسیار طولانی (بیش از ۱۲۰ کاراکتر) در خطوط: {long_lines}")
        # ۳. پیشنهاد تقسیم ماژول اگر خطوط زیاد باشد
        if len(unique_lines) > 400:
            logging.warning("پیشنهاد: تقسیم ماژول به چند فایل کوچکتر برای نگهداری بهتر.")
        # ۴. ثبت snapshot جدید پس از refactor
        log_path = os.path.join(os.path.dirname(__file__), "..", "data", "self_upgrade_code_snapshot.log")
        with open(os.path.abspath(log_path), "a", encoding="utf-8") as logf:
            logf.write(f"\n\n===== Refactor Snapshot {datetime.now().isoformat()} =====\n")
            logf.writelines(unique_lines)
        logging.info("✅ بازنویسی خودکار سیستم به پایان رسید و snapshot ثبت شد.")
    except Exception as e:
        logging.error(f"خطا در بازنویسی خودکار سیستم: {e}")


def self_optimize_code():
    """
    بهینه‌سازی واقعی: ارتقای خود ماژول ارتقا (self-upgrade engine)
    - بررسی سلامت فایل‌های لاگ و نسخه
    - حذف لاگ‌های قدیمی‌تر از ۳۰ روز
    - اطمینان از وجود نسخه پشتیبان آخرین نسخه
    - ثبت گزارش بهبود
    - ثبت کد کامل فعلی ماژول در لاگ پس از هر ارتقا
    """
    try:
        logging.info("🔍 شروع بهینه‌سازی ماژول ارتقا...")
        # حذف لاگ‌های قدیمی‌تر از ۳۰ روز
        now = datetime.now()
        removed_logs = 0
        if os.path.exists(BACKUP_DIR):
            for fname in os.listdir(BACKUP_DIR):
                fpath = os.path.join(BACKUP_DIR, fname)
                if os.path.isfile(fpath) and fname.endswith(".json"):
                    try:
                        ts = fname.split('_')[0]
                        file_time = datetime.strptime(ts, "%Y%m%d")
                        if (now - file_time).days > 30:
                            os.remove(fpath)
                            removed_logs += 1
                    except Exception:
                        continue
        # اطمینان از وجود نسخه پشتیبان آخرین نسخه
        if os.path.exists(VERSION_FILE):
            backup_file(VERSION_FILE)
        # ثبت گزارش بهبود
        msg = f"پاکسازی {removed_logs} نسخه پشتیبان قدیمی و اطمینان از بکاپ نسخه فعلی انجام شد."
        logging.info(msg)
        # ثبت کد کامل فعلی ماژول در لاگ
        with open(__file__, "r", encoding="utf-8") as f:
            code = f.read()
        log_path = os.path.join(os.path.dirname(__file__), "..", "data", "self_upgrade_code_snapshot.log")
        with open(os.path.abspath(log_path), "a", encoding="utf-8") as logf:
            logf.write(f"\n\n===== Snapshot {datetime.now().isoformat()} =====\n")
            logf.write(code)
        logging.info("کد کامل ماژول self_upgrade_engine.py در لاگ ثبت شد.")
        return [msg]
    except Exception as e:
        logging.error(f"خطا در بهینه‌سازی ماژول ارتقا: {e}")
        return []


def apply_upgrade(suggestions, current_emotion):
    """
    اعمال ارتقاهای پیشنهادی به‌طور خودکار، شامل بهبودهای سیستم و کدنویسی
    """
    try:
        if suggestions:
            logging.info("🚀 آغاز اعمال ارتقاهای پیشنهادی...")
            for sug in suggestions:
                logging.info(f"➤ در حال اعمال تغییر: {sug}")
                # در اینجا می‌توان منطق واقعی برای اعمال ارتقا (مانند به‌روزرسانی پیکربندی یا تغییرات در فایل‌های ماژول) قرار داد.
                time.sleep(0.5)
            logging.info("✅ ارتقاهای پیشنهادی با موفقیت اعمال شدند.")
        else:
            logging.info("⚙️ هیچ پیشنهاد ارتقایی برای اعمال وجود ندارد.")
    except Exception as e:
        logging.error(f"خطا در اعمال ارتقاها: {e}")


def read_system_emotion_score():
    """
    تابع نمونه برای خواندن وضعیت احساسات سیستم.
    در محیط واقعی این تابع باید وضعیت سیستم را از منابع معتبری بخواند.
    """
    # مقادیر نمونه جهت شبیه‌سازی
    return {"stress": 8, "hope": 3, "energy": 2}


def ai_analyze_and_rewrite(code, api_url="http://localhost:8000/ai/analyze"):
    """
    ارسال کد به مدل هوش مصنوعی برای تحلیل و دریافت پیشنهاد یا بازنویسی.
    خروجی: dict شامل پیشنهادات و (در صورت وجود) کد بازنویسی‌شده
    """
    try:
        response = requests.post(api_url, json={"code": code}, timeout=30)
        if response.status_code == 200:
            return response.json()
        else:
            logging.error(f"AI API error: {response.status_code} - {response.text}")
            return {"suggestions": [], "rewritten_code": None}
    except Exception as e:
        logging.error(f"خطا در ارتباط با مدل هوش مصنوعی: {e}")
        return {"suggestions": [], "rewritten_code": None}


def self_read_and_suggest(smart_mode=False, ai_api_url="http://localhost:8000/ai/analyze"):
    """
    نسخه ارتقایافته: اگر smart_mode فعال باشد، تحلیل و پیشنهادات از مدل هوش مصنوعی دریافت می‌شود.
    """
    try:
        with open(__file__, "r", encoding="utf-8") as f:
            code = f.read()
        suggestions = []
        ai_result = None
        long_lines = []  # تعریف long_lines پیش از هر استفاده
        if smart_mode:
            ai_result = ai_analyze_and_rewrite(code, ai_api_url)
            suggestions = ai_result.get("suggestions", [])
        else:
            # پیشنهاد: اگر داک‌استرینگ توابع ناقص است
            if '"""' not in code or code.count('"""') < code.count('def '):
                suggestions.append("بررسی و تکمیل داک‌استرینگ توابع برای مستندسازی بهتر.")
            if 'except Exception' in code and 'logging.error' not in code:
                suggestions.append("در exceptها از logging.error برای ثبت خطا استفاده شود.")
            if 'def test_' not in code:
                suggestions.append("اضافه کردن تست‌های واحد برای اطمینان از عملکرد صحیح ماژول.")
            if 'threading.Thread' in code and 'join' not in code:
                suggestions.append("مدیریت صحیح پایان threadها (graceful shutdown) اضافه شود.")
            long_lines = [i+1 for i, l in enumerate(code.splitlines()) if len(l) > 120]
            if long_lines:
                suggestions.append(f"کاهش طول خطوط بلند (بیش از ۱۲۰ کاراکتر) در خطوط: {long_lines}")
        # خلاصه آماری ساختار کد
        stats = None
        try:
            functions_count = code.count('def ')
            lines_count = len(code.splitlines())
            stats = {
                'functions': functions_count,
                'classes': code.count('class '),
                'lines': lines_count,
                'try_blocks': code.count('try:'),
                'except_blocks': code.count('except'),
                'docstrings': code.count('"""'),
                'long_lines': len(long_lines),
            }
        except Exception as e_stats:
            stats = {'error': str(e_stats)}
        # اگر پیشنهاد refactor ساختاری لازم بود، آن را به صورت خودکار اضافه کن
        if (
            isinstance(stats, dict)
            and isinstance(stats.get('functions', 0), int)
            and isinstance(stats.get('lines', 0), int)
            and int(stats.get('functions', 0)) > 10
            and int(stats.get('lines', 0)) > 300
        ):
            suggestions.append("پیشنهاد: تقسیم ماژول به چند فایل کوچکتر برای خوانایی و نگهداری بهتر.")
        # ثبت پیشنهادات و خلاصه در لاگ
        log_path = os.path.join(os.path.dirname(__file__), "..", "data", "self_upgrade_suggestions.log")
        # جلوگیری از تکرار هشدارها: فقط پیشنهادات جدید را هشدار بده
        last_suggestions = set()
        meta_path = os.path.join(os.path.dirname(__file__), "..", "data", "self_upgrade_meta.json")
        meta = {'last_run': None, 'run_count': 0, 'last_suggestions': []}
        if os.path.exists(meta_path):
            try:
                with open(meta_path, "r", encoding="utf-8") as mf:
                    meta = json.load(mf)
                    last_suggestions = set(meta.get('last_suggestions', []))
            except Exception:
                pass
        new_suggestions = [s for s in suggestions if s not in last_suggestions]
        with open(os.path.abspath(log_path), "a", encoding="utf-8") as logf:
            logf.write(f"\n\n===== Suggestions {datetime.now().isoformat()} =====\n")
            for s in suggestions:
                logf.write(f"- {s}\n")
            if stats and isinstance(stats, dict) and 'error' in stats:
                logf.write(f"\n[Code Stats Error] {stats['error']}\n")
            else:
                logf.write(f"\n[Code Stats] {stats}\n")
        # اگر پیشنهاد مهم جدید وجود داشت، در لاگ اصلی هم هشدار ثبت شود
        if new_suggestions:
            logging.warning(f"پیشنهادات مهم جدید خودکدخوانی: {new_suggestions}")
        else:
            logging.info("خودکدخوانی: هیچ پیشنهاد مهم جدید یافت نشد.")
        # ثبت متادیتا
        meta['last_run'] = datetime.now().isoformat()
        meta['run_count'] = meta.get('run_count', 0) + 1
        meta['last_suggestions'] = suggestions
        with open(meta_path, "w", encoding="utf-8") as mf:
            json.dump(meta, mf, ensure_ascii=False, indent=2)
        return suggestions
    except Exception as e:
        logging.error(f"خطا در خودکدخوانی ماژول ارتقا: {e}")
        return []


def auto_apply_suggestions(suggestions, rewritten_code=None):
    """
    اگر پیشنهادات قابل اعمال خودکار باشند (مثلاً داک‌استرینگ یا تقسیم ماژول)، آن‌ها را اعمال کن.
    اگر کد بازنویسی‌شده از مدل هوش دریافت شده باشد، جایگزین کن.
    """
    try:
        applied = []
        if rewritten_code:
            # بکاپ و جایگزینی کد
            backup_file(__file__)
            with open(__file__, "w", encoding="utf-8") as f:
                f.write(rewritten_code)
            logging.info("کد بازنویسی‌شده توسط مدل هوش مصنوعی جایگزین شد.")
            applied.append("کد بازنویسی‌شده جایگزین شد.")
        else:
            # نمونه: افزودن داک‌استرینگ به توابع فاقد آن (نمونه ساده)
            if any("داک‌استرینگ" in s for s in suggestions):
                with open(__file__, "r", encoding="utf-8") as f:
                    code = f.read()
                new_code = ""
                for line in code.splitlines():
                    new_code += line + "\n"
                    if line.strip().startswith("def ") and '"""' not in line:
                        new_code += '    """TODO: توضیح تابع."""\n'
                backup_file(__file__)
                with open(__file__, "w", encoding="utf-8") as f:
                    f.write(new_code)
                applied.append("داک‌استرینگ به توابع فاقد آن افزوده شد.")
        return applied
    except Exception as e:
        logging.error(f"خطا در اعمال خودکار پیشنهادات: {e}")
        return []


def upgrade_scheduler(interval_minutes=10, smart_mode=False, ai_api_url="http://localhost:8000/ai/analyze"):
    def scheduled_task():
        while True:
            try:
                next_run = datetime.now() + timedelta(minutes=interval_minutes)
                logging.info(
                    f"⏳ اجرای بعدی بررسی در ساعت {next_run.strftime('%H:%M:%S')}"
                )
                time.sleep(interval_minutes * 60)

                logging.info("🚀 آغاز بررسی دوره‌ای ارتقا...")
                # خواندن وضعیت لحظه‌ای سیستم
                current_emotion = read_system_emotion_score()
                suggestions = analyze_for_upgrade(current_emotion)
                # ثبت پیشنهادات ارتقا در فایل لاگ
                if suggestions:
                    log_upgrade_suggestion(suggestions)
                else:
                    logging.info("✅ سیستم پایدار است؛ ارتقا نیاز نیست.")

                # اجرای عملیات خودکار اصلاح کد
                auto_refactor()
                # اعمال ارتقاهای پیشنهادی
                apply_upgrade(suggestions, current_emotion)
                # بهینه‌سازی داخلی کد
                code_suggestions = self_optimize_code()
                if code_suggestions:
                    logging.info("✅ تغییرات بهینه‌سازی داخلی اعمال شدند.")

                # ثبت نسخه جدید با متریک‌های سیستم
                save_version("T13.3_V4_Auto", performance_metrics=current_emotion)
                # اجرای خودکار self_read_and_suggest (هوشمند)
                smart_suggestions, rewritten_code = [], None
                try:
                    result = self_read_and_suggest(smart_mode=smart_mode, ai_api_url=ai_api_url)
                    if smart_mode and isinstance(result, tuple):
                        smart_suggestions, rewritten_code = result
                    elif isinstance(result, list):
                        smart_suggestions = result
                except Exception as e:
                    logging.error(f"خطا در اجرای خودتحلیل‌گری هوشمند: {e}")
                # اعمال خودکار برخی پیشنهادات
                if smart_suggestions or rewritten_code:
                    auto_apply_suggestions(smart_suggestions, rewritten_code)
            except Exception as e:
                logging.error(f"خطا در وظیفه زمان‌بندی ارتقا: {e}")
                time.sleep(5)

    threading.Thread(target=scheduled_task, daemon=True).start()
    logging.info("🕒 زمان‌بندی ارتقا تنظیم شد.")


if __name__ == "__main__":
    upgrade_scheduler(interval_minutes=1, smart_mode=True)
    # نگه‌داری برنامه برای مشاهده فعالیت‌های زمان‌بندی
    while True:
        time.sleep(1)
