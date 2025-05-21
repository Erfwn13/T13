import re

def generate_smart_response(user_input, memory):
    lower_input = user_input.lower()
    
    # پاسخ به حالات احوالپرسی
    if any(phrase in lower_input for phrase in ["سلام", "درود"]):
        return "سلام! چه خبر؟"
    elif any(phrase in lower_input for phrase in ["خداحافظ", "بای"]):
        return "خداحافظ! امیدوارم زود دوباره صحبت کنیم."
    elif any(phrase in lower_input for phrase in ["حال خودت چطوره", "تو چطوری", "چطوری پیش می‌ره"]):
        return "من عالی هستم! همیشه دارم یاد می‌گیرم. شما چطورید؟"
    
    # بررسی اطلاعات ذخیره‌شده در حافظه برای پاسخ‌های مربوط
    for key, value in memory.items():
        if key in lower_input:
            return f"به نظر میاد درباره {key} صحبت کردید؛ چون من یاد گرفتم که {key} برابر است با {value}."
    
    # اگر هیچ شرطی صدق نکرد، fallback پیشرفته
    return "متأسفم دقیقاً نفهمیدم منظورت چیه. می‌تونی کمی بیشتر توضیح بدی؟"