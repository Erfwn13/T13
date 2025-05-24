import sys
import time
import torch
from t13_core import T13Engine
from t13_core_persona import T13Persona
from deep_learning_model import DeepConversationalModel
from digital_selfcare import get_system_health, print_health_report
from trend_analyzer import analyze_trend
from self_upgrade_engine import auto_refactor, save_version, analyze_for_upgrade, log_upgrade_suggestion, self_optimize_code
from self_adaptive_module import SelfAdaptiveModule
from performance_monitor import PerformanceMonitor  # ماژول نظارتی
import logging

class T13CentralCoreV4:
    def __init__(self, profile_name="focus_mode"):
        self.profile_name = profile_name
        self.user = "Erfan"  # در سیستم واقعی از پایگاه داده خوانده می‌شود
        self.ai = T13Engine(user_name=self.user)
        self.persona = T13Persona(self.ai)
        # بارگذاری مدل پاسخگوی عمیق fine-tuned
        self.deep_model = DeepConversationalModel(device="cuda" if torch.cuda.is_available() else "cpu")
        self.adaptive_memory = {}
        # راه‌اندازی ماژول Adaptive با state_dim=3 (شاخص‌های داخلی: پیچیدگی کد، زمان پاسخ و نرخ خطا) و 3 عملکرد پیشنهادی
        self.adaptive_module = SelfAdaptiveModule(state_dim=3, action_dim=3)
        # ایجاد نمونه PerformanceMonitor جهت ثبت معیارهای عملکرد
        self.monitor = PerformanceMonitor(log_file="performance.log")
    
    def extract_system_state(self, internal_metrics, trends):
        """
        استخراج وضعیت سیستم به صورت یک لیست عددی (state) شامل سه شاخص نرمال‌شده:
        code_complexity (1-10), response_time (ثانیه) و error_rate (0-1)
        نرمال‌سازی هر شاخص به صورت نمونه انجام می‌شود.
        """
        state = [
            internal_metrics.get("code_complexity", 0) / 10.0,
            internal_metrics.get("response_time", 0) / 10.0,   # فرض بر این است که زمان پاسخ حداکثر 10 ثانیه است
            internal_metrics.get("error_rate", 0)  # نرخ خطا معمولا بین 0 و 1 است
        ]
        return state
    
    def auto_apply_optimizations(self, suggestions):
        """
        اعمال خودکار پیشنهادات بهینه‌سازی داخلی
        """
        try:
            logging.info("🔧 آغاز اعمال بهینه‌سازی داخلی کد به صورت خودکار...")
            for sug in suggestions:
                logging.info(f"➤ در حال اعمال بهینه‌سازی: {sug}")
                # اینجا منطق واقعی جهت اعمال تغییرات پیاده‌سازی خواهد شد
                time.sleep(0.5)
            logging.info("✅ بهینه‌سازی داخلی کد با موفقیت اعمال شد.")
        except Exception as e:
            logging.error(f"خطا در اعمال بهینه‌سازی داخلی: {e}")
    
    def internal_upgrade(self, internal_metrics):
        """
        اجرای ارتقای درونی سیستم به‌گونه‌ای که پیشنهادات بهینه‌سازی داخلی به‌طور خودکار اعمال شوند.
        """
        try:
            logging.info("🔧 آغاز ارتقای درونی سیستم برای بهبود کدنویسی...")
            suggestions = self_optimize_code()
            if suggestions:
                self.auto_apply_optimizations(suggestions)
            else:
                logging.info("✅ سیستم از نظر بهینه‌سازی داخلی در وضعیت بهینه قرار دارد.")
        except Exception as e:
            print(f"⚠️ خطا در ارتقای درونی سیستم: {str(e)}")
    
    def run_all(self):
        internal_metrics = self.load_internal_metrics()
        print("📦 T13 Central Core V4 Activated")
        print(f"👤 User: {self.user}")
        print(f"📂 Profile Loaded: {self.profile_name}")
        print("📊 شاخص‌های داخلی:", internal_metrics)
        
        # گزارش زمان شروع
        self.monitor.log_performance({"Process Start": time.strftime("%Y-%m-%d %H:%M:%S")})
        self.monitor.report_elapsed_time()
        
        # اجرای بخش‌های اصلی سیستم
        try:
            self.ai.run_memory()
            self.ai.run_emotion(internal_metrics)  # در صورت نیاز، می‌توان این خط را نیز حذف یا تغییر داد
            self.ai.run_decision(["Continue Project", "Take a Break", "Postpone"])
            self.ai.run_behavior()
            self.ai.run_upgrade()
            self.ai.run_health()
            self.ai.run_trend_analysis()
            self.ai.run_multiverse()
        except Exception as e:
            print(f"⚠️ Error in AI modules: {str(e)}")
        
        # پردازش و تحلیل شخصیت (در صورت نیاز می‌توان حذف یا تغییر داد)
        try:
            self.persona.set_mood(internal_metrics)
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
            print("\n📊 تحلیل روند:")
            for t in trends:
                print("➤", t)
            print("📈 میانگین شاخص‌های سیستم:")
            for k, v in avg.items():
                print(f" - {k}: {round(v, 2)}")
            # ثبت معیارهای عملکرد
            avg_metric = sum(internal_metrics.values()) / len(internal_metrics)
            self.monitor.log_performance({"avg_metric": avg_metric})
        except Exception as e:
            print(f"⚠️ Error in system diagnostics: {str(e)}")
        
        # تولید ایده خلاقانه با مدل Deep
        try:
            prompt = "Generate innovative ideas for internal system optimization and self-improvement."
            innovative_idea = self.deep_model.generate_response(prompt, max_length=150)
            print("\n💡 ایده خلاقانه تولید‌شده:", innovative_idea)
        except Exception as e:
            print(f"⚠️ Error in generating innovative ideas: {str(e)}")
        
        # ذخیره نسخه سیستم و ثبت شاخص‌های عملکرد
        try:
            performance = {"avg_metric": avg_metric}
            save_version("T13.3_V4", performance_metrics=performance)
            suggestions = analyze_for_upgrade(internal_metrics)
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
        
        # اجرای ارتقای درونی جهت بهبود بهینه‌سازی داخلی کد به صورت خودکار
        self.internal_upgrade(internal_metrics)
        
        self.adaptive_decision(avg, internal_metrics)
        # گزارش زمان پایان و محاسبه کلی زمان اجرا
        self.monitor.report_elapsed_time()
    
    def adaptive_decision(self, avg, internal_metrics):
        """
        استفاده از ماژول Adaptive جهت انتخاب بهترین استراتژی بعدی بر مبنای وضعیت سیستم.
        """
        try:
            state = self.extract_system_state(internal_metrics, avg)
            action = self.adaptive_module.act(state)
            actions_mapping = {
                0: "SafeSupport",  # حالت احتیاطی
                1: "ChaosSpark",   # حالت خلاق و پویا
                2: "BalancedPath"  # حالت متعادل
            }
            print("\n🚀 پیشنهاد تصمیم بر اساس یادگیری تطبیقی:")
            print(f"➤ عملکرد انتخابی: {actions_mapping.get(action, 'BalancedPath')}")
            # محاسبه ساده پاداش بر مبنای بهبود شاخص‌ها
            reward = (10 - internal_metrics.get("code_complexity", 0)) - internal_metrics.get("response_time", 0) - (internal_metrics.get("error_rate", 0) * 10)
            next_state = state  # فرض بر این است که حالت بعدی همان حالت فعلی است
            done = False
            self.adaptive_module.remember(state, action, reward, next_state, done)
            loss = self.adaptive_module.replay()
            if loss:
                print(f"Adaptive Module Loss: {loss:.4f}")
        except Exception as e:
            print(f"⚠️ Error in adaptive decision process: {str(e)}")
    
    def load_internal_metrics(self):
        """
        بارگذاری یا محاسبه شاخص‌های داخلی سیستم جهت استفاده در تصمیم‌گیری‌های ارتقایی.
        در این مثال، یک دیکشنری نمونه برگردانده می‌شود.
        """
        # شاخص‌های فرضی: code_complexity (مقیاس 1 تا 10)، response_time (به ثانیه) و error_rate (بین 0 و 1)
        return {"code_complexity": 8, "response_time": 2.5, "error_rate": 0.15}

if __name__ == "__main__":
    core = T13CentralCoreV4(profile_name="focus_mode")
    core.run_all()