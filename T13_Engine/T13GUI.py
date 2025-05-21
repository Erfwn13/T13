import sqlite3
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
from t13_central import T13CentralCoreV4
from digital_selfcare import get_system_health
from multiverse_core import WorldBuilder
from emotion_stack import EmotionStack
from database_utils import initialize_database
from performance_dashboard import PerformanceDashboard  # وارد کردن داشبورد عملکرد

class T13GUI:
    def __init__(self):
        initialize_database()

        self.window = tk.Tk()
        self.window.title("T13.3 - سیستم تعامل هوشمند (تم مشکی-قرمز)")
        self.window.geometry("980x720")
        self.window.configure(bg="#000000")

        self.style = ttk.Style(self.window)
        self.style.theme_use("clam")
        self.style.configure("TButton", background="#1a1a1a", foreground="#ff3333",
                             font=("Segoe UI", 10, "bold"), padding=8)
        self.style.configure("TLabel", background="#000000", foreground="#ffffff",
                             font=("Segoe UI", 10))
        self.style.configure("TEntry", font=("Segoe UI", 11), padding=8)

        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # تب چت
        self.chat_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.chat_frame, text="Chat Interface")
        self.setup_chat_ui()

        # تب داشبورد عملکرد
        self.dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.dashboard_frame, text="Performance Dashboard")
        self.dashboard = PerformanceDashboard(self.dashboard_frame)

        # نمونه‌های قابلیت‌های سیستم
        self.world_builder = WorldBuilder()
        self.emotion_stack = EmotionStack()
        self.central_core = T13CentralCoreV4(profile_name="focus_mode")

    def setup_chat_ui(self):
        self.chat_display = scrolledtext.ScrolledText(
            self.chat_frame, wrap=tk.WORD, state="disabled", height=25, width=90,
            bg="#000000", fg="#00FF00", font=("Consolas", 11, "bold"),
            borderwidth=3, relief="groove"
        )
        self.chat_display.grid(row=0, column=0, columnspan=2, padx=20, pady=20)
        self.chat_display.tag_configure("right", justify="right")

        self.user_input = ttk.Entry(self.chat_frame, width=70)
        self.user_input.grid(row=1, column=0, padx=20, pady=10, sticky="we")
        self.user_input.bind("<Return>", lambda event: self.send_message())

        self.send_button = ttk.Button(self.chat_frame, text="ارسال", command=self.send_message)
        self.send_button.grid(row=1, column=1, padx=20, pady=10)

        self.create_action_buttons()

        self.status_bar = ttk.Label(self.chat_frame, text="وضعیت سیستم: آماده", anchor="w",
                                    font=("Segoe UI", 9, "italic"))
        self.status_bar.grid(row=3, column=0, columnspan=2, sticky="we", padx=20, pady=5)

        # فراخوانی تابع optimize_and_sync هر 60 ثانیه
        self.window.after(60000, self.optimize_and_sync)

    def optimize_and_sync(self):
        try:
            if not self.window.winfo_exists():
                return  # اگر پنجره بسته شده، ادامه نده
            self.update_chat("🔄 همگام‌سازی سیستم و بهینه‌سازی در حال انجام است...")
            self.status_bar.config(text="وضعیت سیستم: به‌روز و هماهنگ")
            self.window.after(60000, self.optimize_and_sync)
        except tk.TclError:
            # در صورت بسته شدن پنجره یا عدم دسترسی به ویجت‌ها، خطا را نادیده بگیر
            pass

    def create_action_buttons(self):
        button_frame = ttk.Frame(self.chat_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        buttons = [
            ("📊 تحلیل احساسات", self.run_emotion_analysis),
            ("🧠 حافظه", self.run_memory),
            ("🧭 تصمیم‌گیری", self.run_decision),
            ("🎭 رفتار", self.run_behavior),
            ("🧬 ارتقا", self.run_upgrade),
            ("🩺 سلامت سیستم", self.run_health),
            ("💾 ذخیره مکالمه", self.save_conversation),
            ("📂 بارگذاری مکالمه", self.load_conversation),
            ("🌍 دنیاسازی", self.run_create_world),
            ("🧠 آخرین احساسات", self.run_emotion_stack)
        ]
        for text, command in buttons:
            btn = ttk.Button(button_frame, text=text, command=command, width=20)
            btn.pack(side="left", padx=5)

    def send_message(self):
        user_message = self.user_input.get()
        if not user_message.strip():
            return
        self.update_chat(f"👤 شما: {user_message}")
        try:
            response = self.central_core.ai.interaction.respond(user_message)
            if not response or not isinstance(response, str):
                response = "من همیشه آماده‌ام باهات صحبت کنم! هر سوالی داشتی بپرس."
        except Exception as e:
            response = f"⚠️ خطا در پاسخ‌دهی: {e}"
        self.update_chat(f"🤖 T13: {response}")
        self.user_input.delete(0, tk.END)

    def update_chat(self, message):
        def reverse_word_order(text):
            words = text.split()
            return " ".join(words[::-1])
        reversed_message = reverse_word_order(message)
        self.chat_display.config(state="normal")
        self.chat_display.insert(tk.END, "\u200F" + reversed_message + "\n", "right")
        self.chat_display.config(state="disabled")
        self.chat_display.see(tk.END)

    def run_emotion_analysis(self):
        self.update_chat("📊 تحلیل احساسات در حال انجام است...")
        self.central_core.ai.run_emotion(self.central_core.ai.emotion_score)
        self.update_chat("✅ تحلیل احساسات کامل شد.")

    def run_memory(self):
        self.update_chat("🧠 حافظه در حال بارگذاری است...")
        self.central_core.ai.run_memory()
        self.update_chat("✅ حافظه بارگذاری شد.")

    def run_decision(self):
        self.update_chat("🧭 تصمیم‌گیری در حال انجام است...")
        self.central_core.ai.run_decision(["ادامه پروژه", "استراحت", "تعویق"])
        self.update_chat("✅ تصمیم‌گیری انجام شد.")

    def run_behavior(self):
        self.update_chat("🎭 رفتار در حال تنظیم است...")
        self.central_core.ai.run_behavior()
        self.update_chat("✅ رفتار تنظیم شد.")

    def run_upgrade(self):
        self.update_chat("🧬 ارتقا در حال بررسی است...")
        self.central_core.ai.run_upgrade()
        self.update_chat("✅ ارتقا انجام شد.")

    def run_health(self):
        self.update_chat("🩺 وضعیت سیستم در حال بررسی است...")
        health = get_system_health()
        self.update_chat(f"🧠 CPU: {health['cpu']}% | 💾 RAM: {health['ram']}% | ⏱️ Latency: {health['latency']} ms")

    def save_conversation(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(self.chat_display.get("1.0", tk.END))
            messagebox.showinfo("ذخیره مکالمه", "مکالمه با موفقیت ذخیره شد.")

    def load_conversation(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
            self.update_chat(content)

    def run_create_world(self):
        theme = "علمی-تخیلی"
        world = self.world_builder.create_world(theme, complexity=5)
        self.update_chat(f"🌍 دنیای جدید ایجاد شد: {world['details']}")

    def run_emotion_stack(self):
        self.emotion_stack.add_emotion("خوشحالی", 8)
        recent = self.emotion_stack.get_recent_emotions()
        self.update_chat(f"🧠 آخرین احساسات ثبت شده: {recent}")

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    gui = T13GUI()
    gui.run()

