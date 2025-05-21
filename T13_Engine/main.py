from database_utils import init_database, save_conversation, load_conversation
from memory_core import set_fact, get_fact
from t13_central import T13CentralCore
from interaction_module import TextInteraction
from self_upgrade_engine import upgrade_scheduler


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
    central = T13CentralCore(profile_name="focus_mode")
    central.run_all()

    upgrade_scheduler(interval_minutes=1) # برای تست، هر 6 ثانیه اجرا می‌شود؛ تغییر به مقدار مناسب در محیط عملیاتی

    # شروع تعامل متنی
    print("\n💬 سیستم آماده تعامل است. (برای خروج 'exit' را تایپ کنید)\n")
    while True:
        try:
            user_input = input("👤 شما: ")
            if user_input.lower() == "exit":
                print("👋 خداحافظ!")
                save_conversation(interaction.conversation_history)  # ذخیره تاریخچه مکالمات
                break
            response = interaction.respond(user_input)
            print("🤖 T13:", response)
        except Exception as e:
            print("⚠️ خطایی رخ داد:", str(e))

if __name__ == "__main__":
    main()
