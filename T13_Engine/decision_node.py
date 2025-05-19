# decision_node.py

def rank_options(options, emo_score, goal="پیشرفت"):
    """
    بررسی و رتبه‌بندی گزینه‌ها بر اساس احساسات فعلی و هدف
    """
    results = []

    for option in options:
        score = 0
        explanation = []

        # تاثیر احساسات
        if "استراحت" in option and emo_score["stress"] > 6:
            score += 20
            explanation.append("استرس بالا، اولویت با استراحت")

        if "ادامه" in option and emo_score["energy"] > 7:
            score += 25
            explanation.append("انرژی بالاست، ادامه منطقیه")

        if "تعویق" in option and emo_score["hope"] < 5:
            score += 15
            explanation.append("امید کم، شاید بهتره تعویق بخوره")

        # تاثیر هدف
        if "پیشرفت" in goal and "ادامه" in option:
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
