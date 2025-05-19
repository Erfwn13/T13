# main.py

from database_utils import init_database
from memory_core import set_fact, get_fact
from t13_central import T13CentralCore

if __name__ == "__main__":
    print("📦 سیستم حافظه T13.3 راه‌اندازی شد.\n")

    # مقداردهی اولیه پایگاه داده
    init_database()

    # ذخیره نام کاربر
    set_fact("creator", "Erfan")

    # نمایش مقدار بازیابی‌شده
    print("🔍 مقدار بازیابی‌شده:", get_fact("creator"), "\n")

    # اجرای کامل سیستم از طریق هسته مرکزی
    central = T13CentralCore(profile_name="focus_mode")
    central.run_all()

    # ذخیره یک مقدار
    set_fact("favorite_food", "pizza")

    # بازیابی مقدار
    food = get_fact("favorite_food")
    print("Favorite Food:", food)