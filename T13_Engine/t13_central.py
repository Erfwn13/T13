# t13_central.py

from t13_core import T13Engine
from t13_core_persona import T13Persona
from profile_manager import load_profile
from memory_core import get_fact
from digital_selfcare import get_system_health, print_health_report
from trend_analyzer import analyze_trend
from multiverse_core import ScenarioBuilder, MultiProjectSync, CreativityPulse
from echo_engine import echo_response
from decision_layered import layered_decision
from self_decider import choose_best_path

class T13CentralCore:
    def __init__(self, profile_name="focus_mode"):
        self.profile_name = profile_name
        self.user = get_fact("creator") or "Erfan"
        self.profile, self.msg = load_profile(self.profile_name)
        self.ai = T13Engine(user_name=self.user)
        self.persona = T13Persona(self.ai)

    def run_all(self):
        if not self.profile:
            print("❌ Profile not found.")
            return

        feelings = self.profile
        print("📦 T13 Central Core Activated")
        print(f"👤 User: {self.user}")
        print(f"📂 Profile Loaded: {self.profile_name}")
        print("🧠 احساسات:", feelings)

        # اجرای موتور اصلی
        self.ai.run_all(feelings, ["Continue Project", "Take a Break", "Postpone"])

        # مسیرهای تصمیم‌یار
        print("\n🧭 مسیرهای پیشنهادی T13.3:")
        options = layered_decision(feelings)
        for i, opt in enumerate(options, 1):
            print(f"\n🔹 گزینه {i}: {opt['title']}")
            print(f"   ✅ مزیت: {opt['reward']}")
            print(f"   ⚠️ ریسک: {opt['risk']}")
            print(f"   📌 چرا؟ {opt['why']}")



        # تحلیل شخصیت + پاسخ بازتابی
        self.persona.set_mood(feelings)
        mood = self.persona.mood
        behavior = self.persona.execute_behavior()
        echo = self.persona.adapt_response()

        print("\n🧠 تحلیل شخصیت:")
        print(f" - حالت فعلی: {mood}")
        print(f" - مود رفتاری پیشنهادی: {behavior}")
        print(f" - واکنش احساسی تطبیقی:\n{echo}")

        # وضعیت سلامت
        print("\n🩺 وضعیت سلامت سیستم:")
        health = get_system_health()
        print_health_report(health)

        # روند احساسات
        print("\n📊 تحلیل روند احساسی:")
        trends, avg = analyze_trend()
        for t in trends:
            print("➤", t)
        print("📈 میانگین احساسات اخیر:")
        for k, v in avg.items():
            print(f" - {k}: {round(v, 2)}")

        # دنیاسازی + ایده‌پردازی
        print("\n🌀 دنیای مجازی:")
        print(ScenarioBuilder("آینده هوش مصنوعی"))

        projects = [
            {"title": "T13.3 Core AI", "status": "در حال توسعه"},
            {"title": "Shadow Channel Launch", "status": "برنامه‌ریزی"},
            {"title": "AI Story World", "status": "در حال تست"}
        ]
        print("\n📂 پروژه‌های فعال:")
        print(MultiProjectSync(projects))

        print("\n🎇 ایده خلاقانه T13:")
        print(CreativityPulse("AI"))

                # انتخاب نهایی توسط T13 و ذخیره‌سازی
        final = choose_best_path(feelings)
        print("\n🧠 تصمیم نهایی T13:")
        print(f"🔹 مسیر انتخاب‌شده: {final['title']}")
        print(f"✅ مزیت: {final['reward']} | ⚠️ ریسک: {final['risk']}")
        print(f"📌 دلیل انتخاب: {final['why']}")


        # پیشنهاد گام بعدی
        self.suggest_next_step(mood, avg)

    def suggest_next_step(self, mood, avg):
        print("\n🚀 پیشنهاد گام بعدی:")
        if mood == "stressed" or avg.get("stress", 0) > 6:
            print("🛑 استراحت کن یا از SafeSupport استفاده کن.")
        elif mood == "energized":
            print("⚡ ایده‌پردازی کن یا ChaosSpark رو فعال کن.")
        elif avg.get("joy", 0) > 7:
            print("✅ الان زمان اجرای پروژه‌هاست — برو برای توسعه نهایی!")
        else:
            print("🧩 حالت متعادل — می‌تونی هر مسیر دلخواهی رو پیش ببری.")
