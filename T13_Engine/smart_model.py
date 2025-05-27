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
        return f"{prefix}خداحافظ! امیدوارم زود دوباره صحبت کنیم."
    elif any(
        phrase in lower_input
        for phrase in ["حال خودت چطوره", "تو چطوری", "چطوری پیش می‌ره"]
    ):
        return prefix + "من عالی هستم! همیشه دارم یاد می‌گیرم. شما چطورید؟"
    elif any(
        phrase in lower_input for phrase in ["راهنما", "کمک", "چطور", "چه کار کنم"]
    ):
        return f"{prefix}برای هر سوالی اینجا هستم! فقط کافیست بپرسی یا مشکلت را توضیح بده."
    elif any(phrase in lower_input for phrase in ["انگیزه", "امید", "پیشرفت"]):
        return f"{prefix}تو قادری به هر چیزی برسی! فقط باید ادامه بدی و ناامید نشی."
    elif any(phrase in lower_input for phrase in ["جوک", "شوخی", "بخند"]):
        return (
            prefix
            + "یه شوخی: چرا کامپیوتر هیچ وقت خسته نمی‌شه؟ چون همیشه روی RAM استراحت می‌کنه! 😄"
        )
    elif any(phrase in lower_input for phrase in ["پروژه", "کد", "هوش مصنوعی"]):
        return f"{prefix}پروژه T13 یک هسته هوش مصنوعی پیشرفته و خودارتقاست. هر سوال فنی داشتی بپرس!"
    return next(
        (
            (
                prefix
                + f"به نظر میاد درباره {key} صحبت کردید؛ چون من یاد گرفتم که {key} برابر است با {value}."
            )
            for key, value in memory.items()
            if key in lower_input
        ),
        "متأسفم دقیقاً نفهمیدم منظورت چیه. می‌تونی کمی بیشتر توضیح بدی؟",
    )


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
        return f"{prefix}Hello! How can I help you?"
    elif any(phrase in lower_input for phrase in ["bye", "goodbye"]):
        return f"{prefix}Goodbye! Hope to talk to you soon."
    elif any(
        phrase in lower_input
        for phrase in ["how are you", "how's it going", "what's up"]
    ):
        return f"{prefix}I'm great! Always learning. How about you?"
    elif any(
        phrase in lower_input
        for phrase in ["help", "guide", "how do i", "what should i do"]
    ):
        return f"{prefix}I'm here for any question! Just ask or describe your problem."
    elif any(phrase in lower_input for phrase in ["motivate", "hope", "progress"]):
        return f"{prefix}You can achieve anything! Just keep going and never give up."
    elif any(phrase in lower_input for phrase in ["joke", "funny", "laugh"]):
        return (
            prefix
            + "Here's a joke: Why don't computers ever get tired? Because they always take a rest on the RAM! 😄"
        )
    elif any(
        phrase in lower_input
        for phrase in ["project", "code", "ai", "artificial intelligence"]
    ):
        return (
            prefix
            + "T13 project is an advanced self-upgrading AI core. Ask me any technical question!"
        )
    return next(
        (
            (
                prefix
                + f"It seems you talked about {key}; I learned that {key} means {value}."
            )
            for key, value in memory.items()
            if key in lower_input
        ),
        "Sorry, I didn't get that. Could you explain a bit more?",
    )
