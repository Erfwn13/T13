import re
from database_utils import set_memory, get_memory
from textblob import TextBlob
from smart_model import generate_smart_response
from conversation_manager import ConversationManager
from behavior_predictor import BehaviorPredictor
import torch
from deep_learning_model import DeepConversationalModel

class TextInteraction:
    def __init__(self, conversation_history=None):
        self.memory = {}
        self.conversation_history = conversation_history if conversation_history else []
        self.conversation_manager = ConversationManager()
        # افزودن BehaviorPredictor جهت پیش‌بینی رفتار کاربر براساس تاریخچه
        self.behavior_predictor = BehaviorPredictor(self.conversation_history)
        # راه‌اندازی مدل یادگیری عمیق جهت تولید پاسخ
        self.deep_model = DeepConversationalModel(device="cuda" if torch.cuda.is_available() else "cpu")
    
    def respond(self, user_input):
        # به‌روزرسانی وضعیت مکالمه
        self.conversation_manager.update_state(user_input)
        _state = self.conversation_manager.get_state()
        # ثبت ورودی کاربر در تاریخچه
        self.conversation_history.append({"user": user_input})
        
        # تلاش برای یادگیری خودکار از طریق تشخیص الگوهای ساده (مانند "X is Y")
        auto_learn_response = self.auto_learn(user_input)
        if auto_learn_response:
            return auto_learn_response
        
        # استفاده از مدل عمیق جهت تولید پاسخ
        deep_response = self.deep_model.generate_response(user_input)
        return deep_response
    
    def auto_learn(self, text):
        """
        تشخیص الگوهای "X is Y" و ذخیره در حافظه
        """
        pattern = re.compile(r"(\w+)\s*(?:is|=)\s*(.+)", re.IGNORECASE)
        match = pattern.search(text)
        if match:
            key = match.group(1).strip().lower()
            value = match.group(2).strip()
            self.learn(key, value)
            return f"آفرین! من به طور خودکار یاد گرفتم که {key} برابر است با {value}."
        return None

    def learn(self, key, value):
        self.memory[key] = value
        set_memory(key, value)
    
    def analyze_sentiment(self, text):
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        if polarity > 0:
            return 1
        elif polarity < 0:
            return -1
        else:
            return 0

    def generate_suggestion(self, sentiment):
        if sentiment > 0:
            return "ادامه بده، عالیه!"
        elif sentiment < 0:
            return "ممکنه نیاز به تغییر رویکرد داشته باشی."
        else:
            return "بیخیال این موضوع..."