class BehaviorPredictor:
    def __init__(self, conversation_history):
        self.conversation_history = conversation_history

    def predict_next_action(self):
        """
        پیش‌بینی رفتار بعدی کاربر بر اساس تاریخچه مکالمات.
        اگر تاریخچه خالی باشد، پیغام مناسب باز می‌گرداند.
        همچنین با تحلیل آخرین ورودی کاربر، تصمیم می‌گیرد که به احتمال زیاد کاربر چه عملی را مدنظر دارد.
        """
        if not self.conversation_history:
            return "اطلاعات کافی برای پیش‌بینی وجود ندارد."

        # تحلیل آخرین ورودی کاربر
        last_user_input = self.conversation_history[-1].get("user", "").lower()

        # بررسی الگوهای بیشتر برای پیش‌بینی دقیق‌تر
        if "پیشنهاد" in last_user_input:
            return "کاربر احتمالاً به دنبال پیشنهادات جدید است."
        elif "یاد بگیر" in last_user_input:
            return "کاربر احتمالاً می‌خواهد اطلاعات جدیدی ذخیره کند."
        elif "روند احساسی" in last_user_input:
            return "کاربر احتمالاً به دنبال تحلیل احساسات است."
        elif "ذخیره" in last_user_input:
            return "کاربر می‌خواهد اطلاعات یا مکالمه را ذخیره کند."
        elif "بارگذاری" in last_user_input:
            return "کاربر قصد دارد مکالمه یا اطلاعات قبلی را بارگذاری کند."
        else:
            # حالت پیش‌فرض برای تعامل عمومی
            return "کاربر احتمالاً به دنبال تعامل عمومی است."

# Example usage (برای تست در صورت نیاز):
if __name__ == "__main__":
    conversation_history = [
        {"user": "سلام، پیشنهاد بده"},
        {"user": "دیگه یاد بگیر چیزهای جدید"},
    ]
    predictor = BehaviorPredictor(conversation_history)
    print("پیش‌بینی رفتار بعدی:", predictor.predict_next_action())