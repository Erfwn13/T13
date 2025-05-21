class ConversationManager:
    def __init__(self):
        self.state = None

    def update_state(self, user_input):
        """
        به‌روزرسانی وضعیت مکالمه بر اساس ورودی کاربر
        """
        if "پیشنهاد" in user_input:
            self.state = "suggestion"
        elif "یاد بگیر" in user_input:
            self.state = "learning"
        elif "روند احساسی" in user_input:
            self.state = "trend_analysis"
        else:
            self.state = "general"

    def get_state(self):
        """
        بازگرداندن وضعیت فعلی مکالمه
        """
        return self.state