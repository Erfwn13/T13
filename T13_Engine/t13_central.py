import sys
import time
import torch
from t13_core import T13Engine
from t13_core_persona import T13Persona
from deep_learning_model import DeepConversationalModel
from digital_selfcare import get_system_health, print_health_report
from trend_analyzer import analyze_trend
from self_upgrade_engine import auto_refactor, save_version, analyze_for_upgrade, log_upgrade_suggestion
from multiverse_core import ScenarioBuilder, MultiProjectSync, CreativityPulse
from self_adaptive_module import SelfAdaptiveModule
from performance_monitor import PerformanceMonitor  # ماژول نظارتی

class T13CentralCoreV4:
    def __init__(self, profile_name="focus_mode"):
        self.profile_name = profile_name
        self.user = "Erfan"  # در سیستم واقعی از پایگاه داده خوانده می‌شود
        self.ai = T13Engine(user_name=self.user)
        self.persona = T13Persona(self.ai)
        # بارگذاری مدل پاسخگوی عمیق fine-tuned
        self.deep_model = DeepConversationalModel(device="cuda" if torch.cuda.is_available() else "cpu")
        self.adaptive_memory = {}
        # راه‌اندازی ماژول Adaptive با state_dim=5 (برای احساسات: joy, stress, hope, fear, energy) و 3 عملکرد پیشنهادی
        self.adaptive_module = SelfAdaptiveModule(state_dim=5, action_dim=3)
        # ایجاد نمونه PerformanceMonitor جهت ثبت معیارهای عملکرد
        self.monitor = PerformanceMonitor(log_file="performance.log")
    
    def extract_system_state(self, feelings, trends):
        """
        استخراج وضعیت سیستم به صورت یک لیست عددی (state) شامل 5 مقدار نرمال‌شده:
        (مثلاً: joy, stress, hope, fear, energy)
        """
        state = [
            feelings.get("joy", 0) / 10.0,
            feelings.get("stress", 0) / 10.0,
            feelings.get("hope", 0) / 10.0,
            feelings.get("fear", 0) / 10.0,
            feelings.get("energy", 0) / 10.0
        ]
        return state
    
    def run_all(self):
        profile = self.load_profile()
        if not profile:
            print("❌ Profile not found.")
            return

        feelings = profile
        print("📦 T13 Central Core V4 Activated")
        print(f"👤 User: {self.user}")
        print(f"📂 Profile Loaded: {self.profile_name}")
        print("🧠 احساسات:", feelings)
        
        # گزارش زمان شروع
        self.monitor.log_performance({"Process Start": time.strftime("%Y-%m-%d %H:%M:%S")})
        self.monitor.report_elapsed_time()
        
        # اجرای بخش‌های اصلی سیستم
        try:
            self.ai.run_memory()
            self.ai.run_emotion(feelings)
            self.ai.run_decision(["Continue Project", "Take a Break", "Postpone"])
            self.ai.run_behavior()
            self.ai.run_upgrade()
            self.ai.run_health()
            self.ai.run_trend_analysis()
            self.ai.run_multiverse()
        except Exception as e:
            print(f"⚠️ Error in AI modules: {str(e)}")
        
        # پردازش و تحلیل شخصیت
        try:
            self.persona.set_mood(feelings)
            behavior = self.persona.execute_behavior()
            echo = self.persona.adapt_response()
            print("\n🧠 تحلیل شخصیت:")
            print(f" - حالت فعلی: {self.persona.mood}")
            print(f" - مود رفتاری پیشنهادی: {behavior}")
            print(f" - واکنش احساسی تطبیقی:\n{echo}")
        except Exception as e:
            print(f"⚠️ Error in persona processing: {str(e)}")
        
        # گزارش سلامت سیستم و تحلیل روند
        try:
            health = get_system_health()
            print("\n🩺 وضعیت سلامت سیستم:")
            print_health_report(health)
            trends, avg = analyze_trend()
            print("\n📊 تحلیل روند احساسی:")
            for t in trends:
                print("➤", t)
            print("📈 میانگین احساسات ۵ پیام اخیر:")
            for k, v in avg.items():
                print(f" - {k}: {round(v, 2)}")
            # ثبت معیارهای عملکرد
            avg_emotion = sum(feelings.values()) / len(feelings)
            self.monitor.log_performance({"avg_emotion": avg_emotion})
        except Exception as e:
            print(f"⚠️ Error in system diagnostics: {str(e)}")
        
        # تولید ایده خلاقانه با مدل Deep
        try:
            prompt = "Generate innovative ideas for the future of AI and personal growth."
            innovative_idea = self.deep_model.generate_response(prompt, max_length=150)
            print("\n💡 ایده خلاقانه تولید‌شده:", innovative_idea)
        except Exception as e:
            print(f"⚠️ Error in generating innovative ideas: {str(e)}")
        
        self.adaptive_memory.update(feelings)
        
        # ذخیره نسخه سیستم و ثبت متریک عملکرد
        try:
            performance = {"avg_emotion": avg_emotion}
            save_version("T13.3_V4", performance_metrics=performance)
            suggestions = analyze_for_upgrade(feelings)
            if suggestions:
                print("\n🧬 پیشنهادات ارتقا:")
                for s in suggestions:
                    print("➤", s)
                log_upgrade_suggestion(suggestions)
            else:
                print("✅ سیستم پایدار است؛ ارتقا نیاز نیست.")
        except Exception as e:
            print(f"⚠️ Error in upgrade procedures: {str(e)}")
        
        # اجرای خودکار refactor
        try:
            auto_refactor()
        except Exception as e:
            print(f"⚠️ Error in auto-refactor: {str(e)}")
        
        self.adaptive_decision(avg, feelings)
        # گزارش زمان پایان و محاسبه کلی زمان اجرا
        self.monitor.report_elapsed_time()
    
    def adaptive_decision(self, avg, feelings):
        """
        استفاده از ماژول Adaptive جهت انتخاب بهترین استراتژی بعدی بر مبنای وضعیت سیستم.
        """
        try:
            state = self.extract_system_state(feelings, avg)
            action = self.adaptive_module.act(state)
            actions_mapping = {
                0: "SafeSupport",  # حالت استرس‌زا
                1: "ChaosSpark",   # حالت پرانرژی و خلاق
                2: "BalancedPath"  # حالت متعادل
            }
            print("\n🚀 پیشنهاد تصمیم بر اساس یادگیری تطبیقی:")
            print(f"➤ عملکرد انتخابی: {actions_mapping.get(action, 'BalancedPath')}")
            # محاسبه ساده پاداش بر مبنای تفاوت joy و stress
            reward = feelings.get("joy", 0) - feelings.get("stress", 0)
            next_state = state  # فرض بر این است که حالت بعدی همان حالت فعلی است
            done = False
            self.adaptive_module.remember(state, action, reward, next_state, done)
            loss = self.adaptive_module.replay()
            if loss:
                print(f"Adaptive Module Loss: {loss:.4f}")
        except Exception as e:
            print(f"⚠️ Error in adaptive decision process: {str(e)}")
    
    def load_profile(self):
        """
        در این مثال، از یک پروفایل نمونه استفاده می‌کنیم؛ در سیستم واقعی این اطلاعات از پایگاه داده یا فایل خوانده می‌شود.
        """
        return {"joy": 8, "stress": 2, "hope": 7, "fear": 2, "energy": 9}

if __name__ == "__main__":
    core = T13CentralCoreV4(profile_name="focus_mode")
    core.run_all()