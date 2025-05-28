import re

import langdetect
import torch
from behavior_predictor import BehaviorPredictor
from conversation_manager import ConversationManager
from database_utils import get_memory, set_memory
from deep_learning_model import DeepConversationalModel
from smart_model import generate_smart_response, generate_smart_response_en
from textblob import TextBlob


def is_persian(text):
    # اگر متن فقط شامل حروف فارسی و فاصله باشد، فارسی است
    return bool(re.match(r"^[\u0600-\u06FF\s\d.,!?؛،؟ـ‌\-()\[\]]+$", text))


def is_english(text):
    # اگر متن فقط شامل حروف انگلیسی و فاصله باشد، انگلیسی است
    return bool(re.match(r"^[A-Za-z0-9\s.,!?\-()\[\]]+$", text))


class TextInteraction:
    def __init__(self, conversation_history=None, style="default"):
        self.memory = {}
        self.conversation_history = conversation_history or []
        self.conversation_manager = ConversationManager()
        # افزودن BehaviorPredictor جهت پیش‌بینی رفتار کاربر براساس تاریخچه
        self.behavior_predictor = BehaviorPredictor(self.conversation_history)
        # راه‌اندازی مدل یادگیری عمیق جهت تولید پاسخ
        self.deep_model = DeepConversationalModel(
            device="cuda" if torch.cuda.is_available() else "cpu"
        )
        self.style = style  # سبک پاسخ (رسمی، دوستانه، انگیزشی، ...)

    def set_style(self, style):
        self.style = style

    def respond(self, user_input):
        # تشخیص زبان ورودی
        try:
            lang = langdetect.detect(user_input)
        except Exception:
            lang = "unknown"
        if is_persian(user_input) or lang == "fa":
            smart_response = generate_smart_response(
                user_input, self.memory, self.style
            )
            if smart_response and not smart_response.startswith("متأسفم دقیقاً نفهمیدم"):
                return smart_response
            # مدل عمیق فارسی
            deep_model_fa = DeepConversationalModel(
                model_name="auto",
                device="cuda" if torch.cuda.is_available() else "cpu",
                lang="fa",
            )
            if hasattr(deep_model_fa, "error") and (
                "HooshvareLab" in deep_model_fa.error
                or "not found" in deep_model_fa.error
                or "404" in deep_model_fa.error
            ):
                return (
                    "مدل GPT2 فارسی نصب نیست. برای نصب مدل فارسی این دستور را اجرا کن:\n"
                    "pip install transformers\n"
                    "سپس:\n"
                    "from transformers import GPT2LMHeadModel, GPT2Tokenizer\n"
                    "GPT2LMHeadModel.from_pretrained('HooshvareLab/gpt2-fa')\n"
                    "GPT2Tokenizer.from_pretrained('HooshvareLab/gpt2-fa')\n"
                    "یا فقط از پاسخ‌های هوشمند فارسی استفاده می‌شود."
                )
            deep_response = deep_model_fa.generate_response(user_input)
            if not re.search(r"[\u0600-\u06FF]", deep_response):
                return "پاسخ مناسبی پیدا نشد. لطفاً سوال را واضح‌تر بپرس یا موضوع را تغییر بده."
            return deep_response
        elif is_english(user_input) or lang == "en":
            smart_response = generate_smart_response_en(
                user_input, self.memory, self.style
            )
            if smart_response and not smart_response.startswith(
                "Sorry, I didn't get that"
            ):
                return smart_response
            # مدل عمیق انگلیسی
            deep_model_en = DeepConversationalModel(
                model_name="auto",
                device="cuda" if torch.cuda.is_available() else "cpu",
                lang="en",
            )
            deep_response = deep_model_en.generate_response(user_input)
            if not re.search(r"[A-Za-z]", deep_response):
                return "No suitable answer found. Please rephrase your question."
            return deep_response
        else:
            return "Please type your message in Persian or English. / لطفاً پیام خود را به فارسی یا انگلیسی وارد کنید."

    def auto_learn(self, text):
        """
        تشخیص الگوهای "X is Y" و ذخیره در حافظه
        """
        pattern = re.compile(r"(\w+)\s*(?:is|=)\s*(.+)", re.IGNORECASE)
        if match := pattern.search(text):
            key = match[1].strip().lower()
            value = match[2].strip()
            self.learn(key, value)
            return f"آفرین! من به طور خودکار یاد گرفتم که {key} برابر است با {value}."
        return None

    def learn(self, key, value):
        self.memory[key] = value
        set_memory(key, value)

    def analyze_sentiment(self, text):
        blob = TextBlob(str(text))
        polarity = getattr(blob.sentiment, 'polarity', 0)
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
