import re

def generate_smart_response(user_input, memory, style="default"):
    lower_input = user_input.lower()
    # سبک پاسخ
    prefix = ""
    if style == "formal":
        prefix = "[رسمی] "
    elif style == "friendly":
        prefix = "[دوستانه] "
    elif style == "motivational":
        prefix = "[انگیزشی] "
    # پاسخ به حالات احوالپرسی
    if any(phrase in lower_input for phrase in ["سلام", "درود"]):
        return prefix + "سلام! چه خبر؟ چطور می‌تونم کمکت کنم؟"
    elif any(phrase in lower_input for phrase in ["خداحافظ", "بای"]):
        return prefix + "خداحافظ! امیدوارم زود دوباره صحبت کنیم."
    elif any(phrase in lower_input for phrase in ["حال خودت چطوره", "تو چطوری", "چطوری پیش می‌ره"]):
        return prefix + "من عالی هستم! همیشه دارم یاد می‌گیرم. شما چطورید؟"
    # پاسخ به درخواست راهنمایی
    elif any(phrase in lower_input for phrase in ["راهنما", "کمک", "چطور", "چه کار کنم"]):
        return prefix + "برای هر سوالی اینجا هستم! فقط کافیست بپرسی یا مشکلت را توضیح بده."
    # پاسخ به سوالات انگیزشی
    elif any(phrase in lower_input for phrase in ["انگیزه", "امید", "پیشرفت"]):
        return prefix + "تو قادری به هر چیزی برسی! فقط باید ادامه بدی و ناامید نشی."
    # شوخی و طنز
    elif any(phrase in lower_input for phrase in ["جوک", "شوخی", "بخند"]):
        return prefix + "یه شوخی: چرا کامپیوتر هیچ وقت خسته نمی‌شه؟ چون همیشه روی RAM استراحت می‌کنه! 😄"
    # پاسخ به سوالات درباره پروژه
    elif any(phrase in lower_input for phrase in ["پروژه", "کد", "هوش مصنوعی"]):
        return prefix + "پروژه T13 یک هسته هوش مصنوعی پیشرفته و خودارتقاست. هر سوال فنی داشتی بپرس!"
    # بررسی اطلاعات ذخیره‌شده در حافظه برای پاسخ‌های مربوط
    for key, value in memory.items():
        if key in lower_input:
            return prefix + f"به نظر میاد درباره {key} صحبت کردید؛ چون من یاد گرفتم که {key} برابر است با {value}."
    # اگر هیچ شرطی صدق نکرد، fallback پیشرفته
    return "متأسفم دقیقاً نفهمیدم منظورت چیه. می‌تونی کمی بیشتر توضیح بدی؟"

def generate_smart_response_en(user_input, memory, style="default"):
    lower_input = user_input.lower()
    prefix = ""
    if style == "formal":
        prefix = "[Formal] "
    elif style == "friendly":
        prefix = "[Friendly] "
    elif style == "motivational":
        prefix = "[Motivational] "
    if any(phrase in lower_input for phrase in ["hello", "hi", "hey"]):
        return prefix + "Hello! How can I help you?"
    elif any(phrase in lower_input for phrase in ["bye", "goodbye"]):
        return prefix + "Goodbye! Hope to talk to you soon."
    elif any(phrase in lower_input for phrase in ["how are you", "how's it going", "what's up"]):
        return prefix + "I'm great! Always learning. How about you?"
    elif any(phrase in lower_input for phrase in ["help", "guide", "how do i", "what should i do"]):
        return prefix + "I'm here for any question! Just ask or describe your problem."
    elif any(phrase in lower_input for phrase in ["motivate", "hope", "progress"]):
        return prefix + "You can achieve anything! Just keep going and never give up."
    elif any(phrase in lower_input for phrase in ["joke", "funny", "laugh"]):
        return prefix + "Here's a joke: Why don't computers ever get tired? Because they always take a rest on the RAM! 😄"
    elif any(phrase in lower_input for phrase in ["project", "code", "ai", "artificial intelligence"]):
        return prefix + "T13 project is an advanced self-upgrading AI core. Ask me any technical question!"
    for key, value in memory.items():
        if key in lower_input:
            return prefix + f"It seems you talked about {key}; I learned that {key} means {value}."
    return "Sorry, I didn't get that. Could you explain a bit more?"