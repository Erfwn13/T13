# behavior_manager.py


def get_behavior_mode(emo_score):
    """
    تعیین حالت رفتاری به‌صورت خودکار بر اساس احساسات فعلی کاربر.
    ورودی:
        emo_score (dict): دیکشنری شامل مقادیر joy, stress, energy
    خروجی:
        str: نام مود رفتاری (SafeSupport, ShadowBoost, ChillCompanion, ChaosSpark)
    """
    joy = emo_score.get("joy", 5)
    stress = emo_score.get("stress", 5)
    energy = emo_score.get("energy", 5)

    if stress >= 8:
        return "SafeSupport"
    elif joy >= 7 and energy >= 7:
        return "ShadowBoost"
    elif stress < 4 and energy < 5:
        return "ChillCompanion"
    else:
        return "ChaosSpark"


def generate_response(mode, message):
    """
    تولید پاسخ متنی متناسب با مود رفتاری انتخاب‌شده.
    ورودی:
        mode (str): نام مود رفتاری
        message (str): پیام اصلی
    خروجی:
        str: پیام نهایی با سبک رفتاری مناسب
    """
    if mode == "SafeSupport":
        return f"🛡️ [حالت محافظ]: {message} — آرام باش، من کنارت هستم."
    elif mode == "ShadowBoost":
        return f"🔥 [قدرت مضاعف]: {message} — تو می‌تونی، وقتشه بدرخشی!"
    elif mode == "ChillCompanion":
        return f"😎 [آروم و رفیق]: {message} — یکم نفس بکش، بعد ادامه بده."
    elif mode == "ChaosSpark":
        return f"⚡ [جوش خلاقیت]: {message} — بیا یه چیز متفاوت امتحان کنیم!"
    else:
        return f"💬 [پیش‌فرض]: {message}"
