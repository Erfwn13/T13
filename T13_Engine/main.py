from database_utils import init_database, load_conversation, save_conversation
from interaction_module import TextInteraction
from memory_core import get_fact, set_fact
from self_upgrade_engine import upgrade_scheduler
from t13_central import T13CentralCoreV4


def main():
    print("📦 سیستم حافظه T13.3 راه‌اندازی شد.\n")

    # مقداردهی اولیه پایگاه داده
    init_database()

    # بارگذاری تاریخچه مکالمات
    conversation_history = load_conversation()
    interaction = TextInteraction(conversation_history)

    # ذخیره نام کاربر
    set_fact("creator", "Erfan")

    # نمایش مقدار بازیابی‌شده
    print("🔍 مقدار بازیابی‌شده:", get_fact("creator"), "\n")

    # اجرای کامل سیستم از طریق هسته مرکزی
    central = T13CentralCoreV4(profile_name="focus_mode")
    central.run_all()

    upgrade_scheduler(
        interval_minutes=1
    )  # برای تست، هر 6 ثانیه اجرا می‌شود؛ تغییر به مقدار مناسب در محیط عملیاتی

    # شروع تعامل متنی
    print("\n💬 سیستم آماده تعامل است. (برای خروج 'exit' را تایپ کنید)\n")
    while True:
        try:
            user_input = input("👤 شما: ")
            if user_input.lower() == "exit":
                print("👋 خداحافظ!")
                save_conversation(
                    interaction.conversation_history
                )  # ذخیره تاریخچه مکالمات
                break
            response = interaction.respond(user_input)
            print("🤖 T13:", response)
        except Exception as e:
            print("⚠️ خطایی رخ داد:", e)


if __name__ == "__main__":
    main()
