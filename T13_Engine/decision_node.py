# decision_node.py

def rank_options(options, emo_score, goal="پیشرفت"):
    """
    بررسی و رتبه‌بندی گزینه‌ها بر اساس احساسات فعلی و هدف.
    ورودی:
        options (list[str]): لیست گزینه‌های تصمیم‌گیری
        emo_score (dict): دیکشنری احساسات فعلی (stress, energy, hope و ...)
        goal (str): هدف فعلی (پیش‌فرض: پیشرفت)
    خروجی:
        best (dict): بهترین گزینه با امتیاز و دلایل
        ranked (list[dict]): لیست مرتب‌شده گزینه‌ها با امتیاز و توضیح
    منطق:
        اولویت با شرایط احساسی بحرانی است؛ امتیاز هدف فقط در شرایط پایدار اضافه می‌شود.
    """
    results = []

    for option in options:
        score = 0
        explanation = []
        # پرچم وضعیت بحرانی
        critical = False

        # تاثیر احساسات
        if "استراحت" in option and emo_score.get("stress", 0) > 6:
            score += 40  # افزایش امتیاز برای اولویت واقعی
            explanation.append("استرس بالا، اولویت با استراحت")
            critical = True

        if "ادامه" in option and emo_score.get("energy", 0) > 7:
            score += 25
            explanation.append("انرژی بالاست، ادامه منطقیه")
            # critical را تغییر نمی‌دهیم چون انرژی بالا بحرانی نیست

        if "تعویق" in option and emo_score.get("hope", 0) < 5:
            score += 40  # افزایش امتیاز برای اولویت واقعی
            explanation.append("امید کم، شاید بهتره تعویق بخوره")
            critical = True

        # تاثیر هدف فقط اگر وضعیت بحرانی نبود
        if not critical and "پیشرفت" in goal and "ادامه" in option:
            score += 20
            explanation.append("سازگار با هدف پیشرفت")

        results.append({
            "option": option,
            "score": score,
            "why": explanation
        })

    # مرتب‌سازی براساس امتیاز
    ranked = sorted(results, key=lambda x: x["score"], reverse=True)
    best = ranked[0] if ranked else {"option": None, "score": 0, "why": ["هیچ گزینه‌ای یافت نشد"]}

    return best, ranked
