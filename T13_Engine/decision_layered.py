# decision_layered.py

def layered_decision(feelings, goal="پیشرفت پروژه", context=None):
    joy = feelings.get("joy", 5)
    stress = feelings.get("stress", 5)
    hope = feelings.get("hope", 5)
    fear = feelings.get("fear", 5)
    energy = feelings.get("energy", 5)

    suggestions = []

    # مسیر ۱: تهاجمی / پیشرو
    if energy > 6 and joy > 6:
        suggestions.append({
            "title": "شروع فوری کار",
            "risk": "خستگی احتمالی",
            "reward": "پیشرفت سریع",
            "why": "انرژی و انگیزه بالاست. ادامه بده تا اوج."
        })

    # مسیر ۲: متعادل / هوشمند
    if stress > 4 and fear > 4:
        suggestions.append({
            "title": "برنامه‌ریزی مجدد و تحلیل ریسک",
            "risk": "کمی تأخیر",
            "reward": "اطمینان و نظم",
            "why": "احساس فشار دیده می‌شه. یک مرحله عقب‌نشینی تاکتیکی پیشنهاد می‌شه."
        })

    # مسیر ۳: خلاقانه / خارج از چارچوب
    if hope >= 6 and energy >= 6:
        suggestions.append({
            "title": "جستجوی ایده جدید",
            "risk": "عدم قطعیت",
            "reward": "دستاورد نوآورانه",
            "why": "ترکیب امید و انرژی نشونه‌ای از آمادگی ذهنی برای خلاقیت جدیده."
        })

    # اگر هیچ مسیر منطبق نشد
    if not suggestions:
        suggestions.append({
            "title": "حفظ وضعیت فعلی",
            "risk": "رکود",
            "reward": "ثبات",
            "why": "احساسات در سطح متوسط قرار دارن. تثبیت بهترین گزینه‌ست."
        })

    return suggestions
