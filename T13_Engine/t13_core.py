# t13_core.py
import os
from memory_core import set_fact, get_fact
from emotion_stack import analyze_emotion, adaptive_reaction
from decision_node import rank_options
from behavior_manager import get_behavior_mode, generate_response
from self_upgrade_engine import save_version, analyze_for_upgrade, log_upgrade_suggestion
from digital_selfcare import get_system_health, print_health_report
from trend_analyzer import analyze_trend
from multiverse_core import ScenarioBuilder, MultiProjectSync, CreativityPulse
from self_upgrade_engine import save_version, analyze_for_upgrade, log_upgrade_suggestion, auto_refactor


class T13Engine:
    def __init__(self, user_name="Erfan"):
        self.user = user_name
        self.emotion_score = {}
        self.best_option = {}
        self.behavior_mode = ""
        self.projects = [
            {"title": "T13.3 Core AI", "status": "در حال توسعه"},
            {"title": "Shadow Channel Launch", "status": "برنامه‌ریزی"},
            {"title": "AI Story World", "status": "در حال تست"}
        ]
        # اضافه کردن ویژگی interaction به عنوان نمونه کلاس TextInteraction
        from interaction_module import TextInteraction
        self.interaction = TextInteraction()

    def run_memory(self):
        print("📦 سیستم حافظه T13.3 راه‌اندازی شد.\n")
        set_fact("creator", self.user)
        print("🔍 مقدار بازیابی‌شده:", get_fact("creator"), "\n")

    def run_emotion(self, feelings):
        self.emotion_score = analyze_emotion(feelings)
        print("📊 تحلیل احساسات:", self.emotion_score, "\n")
        print("💬 واکنش:", adaptive_reaction(self.emotion_score), "\n")

    def run_decision(self, options, goal="پیشرفت سریع"):
        self.best_option, _ = rank_options(options, self.emotion_score, goal)
        print("🧭 تصمیم‌گیری هوشمند:\n")
        print("✅ بهترین گزینه:", self.best_option["option"])
        print("📈 امتیاز:", self.best_option["score"])
        print("📌 دلایل:", " | ".join(self.best_option["why"]), "\n")

    def run_behavior(self):
        self.behavior_mode = get_behavior_mode(self.emotion_score)
        response = generate_response(self.behavior_mode, "الان باید تصمیم بگیری، چه راهی رو انتخاب می‌کنی؟")
        print("🎭 سبک رفتاری انتخاب‌شده:", self.behavior_mode, "\n")
        print(response, "\n")

    def run_upgrade(self):
        performance = {"avg_emotion": self.emotion_score}
        save_version("T13.3+", performance_metrics=performance)
        
        suggestions = analyze_for_upgrade(self.emotion_score)
        if suggestions:
            print("🧬 پیشنهادات ارتقا:")
            for s in suggestions:
                print("➤", s)
            log_upgrade_suggestion(suggestions)
        else:
            print("✅ وضعیت پایدار: ارتقا نیاز نیست.\n")
        
        auto_refactor()  # اجرای بازنویسی خودکار سیستم

    def run_health(self):
        status = get_system_health()
        print_health_report(status)

    def run_trend_analysis(self):
        suggestions, avg = analyze_trend()
        print("\n📊 تحلیل روند احساسی بلندمدت:")
        for s in suggestions:
            print("➤", s)
        print("📈 میانگین ۵ احساس آخر:")
        for k, v in avg.items():
            print(f" - {k}: {round(v, 2)}")
        print()

    def run_multiverse(self):
        print("🌀 دنیاسازی:")
        print(ScenarioBuilder("آینده هوش مصنوعی"))
        print("\n📂 پروژه‌ها:")
        print(MultiProjectSync(self.projects))
        print("\n🎇 ایده خلاقانه:")
        print(CreativityPulse("AI"))

    def run_all(self, feelings, options):
        self.run_memory()
        self.run_emotion(feelings)
        self.run_decision(options)
        self.run_behavior()
        self.run_upgrade()
        self.run_health()
        self.run_trend_analysis()
        self.run_multiverse()
