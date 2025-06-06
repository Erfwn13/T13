import glob
import os
import sqlite3
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk

from database_utils import initialize_database
from digital_selfcare import get_system_health
from emotion_stack import EmotionStack
from multiverse_core import WorldBuilder
from performance_dashboard import PerformanceDashboard
from profile_manager import (export_profile, import_profile, list_profiles,
                             load_profile, save_profile)
from t13_central import T13CentralCoreV4


class T13GUI:
    def add_background_gradient(self):
        # افزودن گرادینت پس‌زمینه با Canvas و قرار دادن آن زیر همه ویجت‌ها
        self.bg_canvas = tk.Canvas(self.window, width=1200, height=800, highlightthickness=0, bd=0)
        self.bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        # رسم گرادینت عمودی
        for i in range(0, 800, 2):
            color = f"#181c24" if i < 400 else f"#23272f"
            self.bg_canvas.create_rectangle(0, i, 1200, i+2, outline="", fill=color)
        # lower حذف شد؛ canvas قبل از سایر ویجت‌ها ساخته می‌شود و در پس‌زمینه قرار می‌گیرد

    def __init__(self):
        initialize_database()
        self.window = tk.Tk()
        self.window.title("T13 Engine GUI")
        self.window.geometry("1200x800")
        self.window.configure(bg="#181c24")
        self.add_background_gradient()  # اضافه کردن گرادینت پس‌زمینه

        # استایل مدرن و تقویت‌شده برای ttk
        style = ttk.Style(self.window)
        style.theme_use("clam")
        # دکمه مدرن با گردی و سایه و افکت hover
        style.configure(
            "TButton",
            background="#23272f",
            foreground="#ff3333",
            font=("Segoe UI", 11, "bold"),
            padding=10,
            borderwidth=0,
            relief="flat",
            focusthickness=3,
            focuscolor="#ff3333"
        )
        style.map(
            "TButton",
            background=[("active", "#ff3333"), ("!active", "#23272f")],
            foreground=[("active", "#fff"), ("!active", "#ff3333")],
            relief=[("pressed", "groove"), ("!pressed", "flat")],
            highlightcolor=[("focus", "#ff3333")]
        )
        # گرد کردن بیشتر دکمه‌ها و سایه
        style.configure("Rounded.TButton", borderwidth=0, relief="flat", padding=12, font=("Segoe UI", 11, "bold"), background="#23272f", foreground="#ff3333")
        style.map("Rounded.TButton", background=[("active", "#ff3333")], foreground=[("active", "#fff")])
        # لیبل مدرن
        style.configure(
            "TLabel",
            background="#181c24",
            foreground="#fff",
            font=("Segoe UI", 11),
            padding=6
        )
        # استایل combobox
        style.configure("TCombobox", fieldbackground="#23272f", background="#23272f", foreground="#ff3333", borderwidth=0, padding=8, font=("Segoe UI", 11))
        style.map("TCombobox", fieldbackground=[("readonly", "#23272f")], background=[("readonly", "#23272f")], foreground=[("readonly", "#ff3333")])
        # استایل entry
        style.configure("TEntry", font=("Segoe UI", 11), padding=8, fieldbackground="#23272f", foreground="#fff", borderwidth=0)
        # استایل notification bar
        self.notification_bar = tk.Label(
            self.window,
            text="",
            bg="#ffcc00",
            fg="#000",
            font=("Segoe UI", 11, "bold"),
            anchor="center",
            relief="flat",
            padx=8,
            pady=4,
            bd=0,
            highlightthickness=2,
            highlightbackground="#ff8800"
        )
        self.notification_bar.pack(fill=tk.X, side=tk.TOP, padx=0, pady=0)
        self.notification_bar.pack_forget()

        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=18, pady=18)

        # تب چت
        self.chat_frame = ttk.Frame(self.notebook, style="TFrame")
        self.notebook.add(self.chat_frame, text="💬 Chat Interface")
        self.setup_profile_selector()
        self.setup_chat_ui()

        # تب داشبورد عملکرد
        self.dashboard_frame = ttk.Frame(self.notebook, style="TFrame")
        self.notebook.add(self.dashboard_frame, text="📊 Performance Dashboard")
        self.dashboard = PerformanceDashboard(self.dashboard_frame)

        # نمونه‌های قابلیت‌های سیستم
        self.world_builder = WorldBuilder()
        self.emotion_stack = EmotionStack()
        self.central_core = T13CentralCoreV4(profile_name="focus_mode")

        self.current_theme = "dark"

    def setup_profile_selector(self):
        # فریم اصلی انتخاب پروفایل
        outer_frame = ttk.Frame(self.chat_frame)
        outer_frame.grid(row=0, column=2, padx=10, pady=10, sticky="ne")

        # فریم اسکرول‌پذیر افقی برای دکمه‌ها و ابزارها
        canvas = tk.Canvas(outer_frame, height=60, bg="#181c24", highlightthickness=0)
        scrollbar = ttk.Scrollbar(outer_frame, orient="horizontal", command=canvas.xview)
        scrollable_frame = ttk.Frame(canvas)
        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(xscrollcommand=scrollbar.set)
        canvas.pack(side="top", fill="x", expand=True)
        scrollbar.pack(side="bottom", fill="x")

        # لیبل و ابزارهای انتخاب پروفایل
        ttk.Label(scrollable_frame, text="انتخاب پروفایل:").pack(side="left", padx=(0, 4))
        self.profile_var = tk.StringVar()
        self.profile_search_var = tk.StringVar()
        profiles = list_profiles()
        search_entry = ttk.Entry(scrollable_frame, textvariable=self.profile_search_var, width=12, style="TEntry")
        search_entry.pack(side="left", padx=(0, 5))
        search_entry.insert(0, "جستجو...")

        def on_profile_search(*args):
            q = self.profile_search_var.get().strip().lower()
            all_profiles = list_profiles()
            filtered = [p for p in all_profiles if q in p.lower()]
            self.profile_combo["values"] = filtered

        self.profile_search_var.trace_add("write", lambda *a: on_profile_search())
        self.profile_combo = ttk.Combobox(
            scrollable_frame, textvariable=self.profile_var, values=profiles, width=18, style="TCombobox"
        )
        self.profile_combo.pack(side="left", padx=5)

        # دکمه‌های پروفایل با ظاهر گرد و فاصله مناسب
        btn_style = {
            "style": "Rounded.TButton",
            "width": 14,
            "padding": 6
        }
        for text, cmd in [
            ("بارگذاری پروفایل", self.load_selected_profile),
            ("🔄 بروزرسانی لیست", self.refresh_profiles),
            ("➕ پروفایل جدید", self.create_new_profile),
            ("🗑️ حذف پروفایل", self.delete_selected_profile),
            ("ℹ️ خلاصه پروفایل", self.show_profile_info),
            ("⬇️ خروجی پروفایل", self.export_profile_gui),
            ("⬆️ ورود پروفایل", self.import_profile_gui),
        ]:
            ttk.Button(scrollable_frame, text=text, command=cmd, **btn_style).pack(side="left", padx=3)

        # انتخاب سبک پاسخ
        ttk.Label(scrollable_frame, text="سبک پاسخ:").pack(side="left", padx=(10, 0))
        self.style_var = tk.StringVar(value="default")
        self.style_combo = ttk.Combobox(
            scrollable_frame,
            textvariable=self.style_var,
            values=["default", "formal", "friendly", "motivational"],
            width=12,
            style="TCombobox"
        )
        self.style_combo.pack(side="left", padx=5)
        self.style_combo.bind("<<ComboboxSelected>>", self.change_response_style)
        # انتخاب مدل و زبان
        ttk.Label(scrollable_frame, text="مدل:").pack(side="left", padx=(10, 0))
        self.model_var = tk.StringVar(value="auto")
        self.model_combo = ttk.Combobox(
            scrollable_frame,
            textvariable=self.model_var,
            values=["auto", "gpt2", "HooshvareLab/gpt2-fa"],
            width=18,
            style="TCombobox"
        )
        self.model_combo.pack(side="left", padx=5)
        self.model_combo.bind("<<ComboboxSelected>>", self.change_model_lang)
        ttk.Label(scrollable_frame, text="زبان:").pack(side="left", padx=(10, 0))
        self.lang_var = tk.StringVar(value="fa")
        self.lang_combo = ttk.Combobox(
            scrollable_frame, textvariable=self.lang_var, values=["fa", "en"], width=8, style="TCombobox"
        )
        self.lang_combo.pack(side="left", padx=5)
        self.lang_combo.bind("<<ComboboxSelected>>", self.change_model_lang)
        # دکمه‌های نسخه پشتیبان و سایر ابزارها
        for text, cmd in [
            ("🗂️ نسخه‌های پشتیبان", self.show_backups_gui),
            ("❓ راهنما", self.show_help_popup),
            ("🌓 تغییر تم", self.toggle_theme),
            ("📢 ارسال بازخورد/گزارش خطا", self.show_feedback_popup),
        ]:
            ttk.Button(scrollable_frame, text=text, command=cmd, **btn_style).pack(side="left", padx=3)

    def change_response_style(self, event=None):
        style = self.style_var.get()
        self.central_core.ai.interaction.set_style(style)
        self.update_chat(f"سبک پاسخ به '{style}' تغییر یافت.")

    def show_profile_info(self):
        name = self.profile_var.get()
        if not name:
            messagebox.showinfo("خلاصه پروفایل", "لطفاً یک پروفایل انتخاب کنید.")
            return
        data, msg = load_profile(name)
        if data:
            info = "\n".join([f"{k}: {v}" for k, v in data.items()])
            messagebox.showinfo(f"خلاصه پروفایل '{name}'", info)
        else:
            messagebox.showinfo("خلاصه پروفایل", f"❌ خطا: {msg}")

    def refresh_profiles(self):
        profiles = list_profiles()
        self.profile_combo["values"] = profiles
        self.update_chat("🔄 لیست پروفایل‌ها بروزرسانی شد.")

    def load_selected_profile(self):
        name = self.profile_var.get()
        if not name:
            messagebox.showwarning("انتخاب پروفایل", "لطفاً یک پروفایل انتخاب کنید.")
            return
        data, msg = load_profile(name)
        if data:
            self.central_core = T13CentralCoreV4(profile_name=name)
            style = self.style_var.get() if hasattr(self, "style_var") else "default"
            self.central_core.ai.interaction.set_style(style)
            # اعمال مدل و زبان از پروفایل
            if hasattr(self.central_core.ai.interaction, "deep_model"):
                model = data.get("model", "auto")
                lang = data.get("lang", "fa")
                self.model_var.set(model)
                self.lang_var.set(lang)
                self.central_core.ai.interaction.deep_model = getattr(
                    __import__("deep_learning_model"), "DeepConversationalModel"
                )(model_name=model, lang=lang)
                self.status_bar.config(text=f"وضعیت سیستم: مدل={model} | زبان={lang}")
                # اگر مدل فارسی نصب نبود، هشدار GUI بده
                if model == "HooshvareLab/gpt2-fa" and hasattr(
                                    self.central_core.ai.interaction.deep_model, "error"
                                ) and (
                                        "not found" in self.central_core.ai.interaction.deep_model.error
                                        or "404" in self.central_core.ai.interaction.deep_model.error
                                    ):
                    messagebox.showwarning(
                        "مدل فارسی نصب نیست",
                        "مدل GPT2 فارسی نصب نیست. لطفاً دستور نصب را اجرا کنید.",
                    )
            self.update_chat(f"✅ پروفایل '{name}' با موفقیت بارگذاری شد.")
        else:
            self.update_chat(f"❌ خطا در بارگذاری پروفایل: {msg}")

    def create_new_profile(self):
        def save():
            name = entry.get().strip()
            if not name:
                messagebox.showwarning("نام پروفایل", "نام پروفایل نمی‌تواند خالی باشد.")
                return
            model = model_var.get()
            lang = lang_var.get()
            default_data = {
                "created": True,
                "desc": "پروفایل جدید",
                "model": model,
                "lang": lang,
            }
            msg = save_profile(name, default_data)
            self.refresh_profiles()
            self.update_chat(f"{msg}")
            win.destroy()

        win = tk.Toplevel(self.window)
        win.title("ساخت پروفایل جدید")
        ttk.Label(win, text="نام پروفایل:").pack(padx=10, pady=10)
        entry = ttk.Entry(win, width=25)
        entry.pack(padx=10, pady=5)
        ttk.Label(win, text="مدل عمیق:").pack(padx=10, pady=(10, 0))
        model_var = tk.StringVar(value="auto")
        model_combo = ttk.Combobox(
            win,
            textvariable=model_var,
            values=["auto", "gpt2", "HooshvareLab/gpt2-fa"],
            width=25,
            style="TCombobox"
        )
        model_combo.pack(padx=10, pady=5)
        ttk.Label(win, text="زبان پیش‌فرض:").pack(padx=10, pady=(10, 0))
        lang_var = tk.StringVar(value="fa")
        lang_combo = ttk.Combobox(
            win, textvariable=lang_var, values=["fa", "en"], width=25, style="TCombobox"
        )
        lang_combo.pack(padx=10, pady=5)
        ttk.Button(win, text="ذخیره", command=save).pack(pady=10)

    def delete_selected_profile(self):
        name = self.profile_var.get()
        if not name:
            messagebox.showwarning("حذف پروفایل", "لطفاً یک پروفایل انتخاب کنید.")
            return
        if answer := messagebox.askyesno(
            "تأیید حذف", f"آیا مطمئن هستید که می‌خواهید پروفایل '{name}' حذف شود؟"
        ):
            path = os.path.join("profiles", f"{name}.json")
            try:
                os.remove(path)
                self.refresh_profiles()
                self.update_chat(f"🗑️ پروفایل '{name}' حذف شد.")
            except Exception as e:
                self.update_chat(f"❌ خطا در حذف پروفایل: {e}")

    def show_backups_gui(self):
        backup_files = sorted(glob.glob("backup/*.json"), reverse=True)
        win = tk.Toplevel(self.window)
        win.title("نسخه‌های پشتیبان")
        ttk.Label(win, text="لیست نسخه‌های پشتیبان:").pack(padx=10, pady=10)
        search_var = tk.StringVar()
        search_entry = ttk.Entry(win, textvariable=search_var, width=30)
        search_entry.pack(padx=10, pady=(0, 5))
        listbox = tk.Listbox(win, width=60, height=15)
        for f in backup_files:
            listbox.insert(tk.END, f)
        listbox.pack(padx=10, pady=5)

        def on_search(*args):
            q = search_var.get().strip().lower()
            listbox.delete(0, tk.END)
            for f in backup_files:
                if q in f.lower():
                    listbox.insert(tk.END, f)

        search_var.trace_add("write", lambda *a: on_search())

        def restore():
            sel = listbox.curselection()
            if not sel:
                messagebox.showwarning(
                    "انتخاب نسخه پشتیبان", "لطفاً یک نسخه را انتخاب کنید."
                )
                return
            path = listbox.get(sel[0])
            import shutil

            shutil.copy(path, "data/version.json")
            self.update_chat(f"نسخه پشتیبان {path} بازگردانی شد.")
            win.destroy()

        ttk.Button(win, text="بازگردانی نسخه انتخابی", command=restore).pack(pady=10)

    def setup_chat_ui(self):
        self.chat_display = scrolledtext.ScrolledText(
            self.chat_frame,
            wrap=tk.WORD,
            state="disabled",
            height=25,
            width=90,
            bg="#000000",
            fg="#00FF00",
            font=("Consolas", 11, "bold"),
            borderwidth=3,
            relief="groove",
        )
        self.chat_display.grid(row=0, column=0, columnspan=2, padx=20, pady=20)
        self.chat_display.tag_configure("right", justify="right")

        self.user_input = ttk.Entry(self.chat_frame, width=70)
        self.user_input.grid(row=1, column=0, padx=20, pady=10, sticky="we")
        self.user_input.bind("<Return>", lambda event: self.send_message())

        self.send_button = ttk.Button(
            self.chat_frame, text="ارسال", command=self.send_message
        )
        self.send_button.grid(row=1, column=1, padx=20, pady=10)

        self.create_action_buttons()

        self.status_bar = ttk.Label(
            self.chat_frame,
            text="وضعیت سیستم: آماده",
            anchor="w",
            font=("Segoe UI", 9, "italic"),
        )
        self.status_bar.grid(
            row=3, column=0, columnspan=2, sticky="we", padx=20, pady=5
        )

        # فراخوانی تابع optimize_and_sync هر 60 ثانیه
        self.window.after(60000, self.optimize_and_sync)

    def optimize_and_sync(self):
        """Perform optimization and sync periodically"""
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
        # فریم جدا برای دکمه‌های اکشن پایین چت
        button_frame = ttk.Frame(self.chat_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky="we")
        # اسکرول افقی برای دکمه‌های اکشن
        canvas = tk.Canvas(button_frame, height=54, bg="#181c24", highlightthickness=0)
        scrollbar = ttk.Scrollbar(button_frame, orient="horizontal", command=canvas.xview)
        scrollable_frame = ttk.Frame(canvas)
        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(xscrollcommand=scrollbar.set)
        canvas.pack(side="top", fill="x", expand=True)
        scrollbar.pack(side="bottom", fill="x")
        # دکمه‌های اکشن با ظاهر گرد و فاصله مناسب
        btn_style = {
            "style": "Rounded.TButton",
            "width": 18,
            "padding": 8
        }
        for text, command in [
            ("📊 تحلیل احساسات", self.run_emotion_analysis),
            ("🧠 حافظه", self.run_memory),
            ("🧭 تصمیم‌گیری", self.run_decision),
            ("🎭 رفتار", self.run_behavior),
            ("🧬 ارتقا", self.run_upgrade),
            ("🩺 سلامت سیستم", self.run_health),
            ("💾 ذخیره مکالمه", self.save_conversation),
            ("📂 بارگذاری مکالمه", self.load_conversation),
            ("🌍 دنیاسازی", self.run_create_world),
            ("🧠 آخرین احساسات", self.run_emotion_stack),
        ]:
            ttk.Button(scrollable_frame, text=text, command=command, **btn_style).pack(side="left", padx=5)

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

    def show_notification(self, message, level="info", duration=4000):
        """
        نمایش پیام نوتیفیکیشن در بالای پنجره GUI
        level: info, warning, error
        duration: زمان نمایش (ms)
        """
        colors = {
            "info": ("#ffcc00", "#000"),
            "warning": ("#ff8800", "#fff"),
            "error": ("#ff3333", "#fff"),
        }
        bg, fg = colors.get(level, ("#ffcc00", "#000"))
        self.notification_bar.config(text=message, bg=bg, fg=fg)
        self.notification_bar.pack(fill=tk.X, side=tk.TOP)
        self.window.after(duration, lambda: self.notification_bar.pack_forget())

    def update_chat(self, message):
        def reverse_word_order(text):
            words = text.split()
            return " ".join(words[::-1])

        reversed_message = reverse_word_order(message)
        self.chat_display.config(state="normal")
        self.chat_display.insert(tk.END, "\u200f" + reversed_message + "\n", "right")
        self.chat_display.config(state="disabled")
        self.chat_display.see(tk.END)
        # اگر پیام راهنمای نصب مدل فارسی بود، یک هشدار GUI هم نمایش بده
        if "مدل GPT2 فارسی نصب نیست" in message:
            self.show_notification(
                "مدل GPT2 فارسی نصب نیست. لطفاً دستور نصب را اجرا کنید.", level="warning"
            )
        if "خطا" in message or "⚠️" in message:
            self.show_notification(message, level="error")

    def run_health(self):
        self.update_chat("🩺 وضعیت سیستم در حال بررسی است...")
        health = get_system_health()
        self.update_chat(
            f"🧠 CPU: {health['cpu']}% | 💾 RAM: {health['ram']}% | ⏱️ Latency: {health['latency']} ms"
        )
        if alerts := health.get("alert", []):
            self.show_notification(" | ".join(alerts), level="warning")

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

    def save_conversation(self):
        if file_path := filedialog.asksaveasfilename(
            defaultextension=".txt", filetypes=[("Text Files", "*.txt")]
        ):
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(self.chat_display.get("1.0", tk.END))
            messagebox.showinfo("ذخیره مکالمه", "مکالمه با موفقیت ذخیره شد.")

    def load_conversation(self):
        if file_path := filedialog.askopenfilename(
            filetypes=[("Text Files", "*.txt")]
        ):
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

    def change_model_lang(self, event=None):
        model = self.model_var.get()
        lang = self.lang_var.get()
        if hasattr(self.central_core.ai.interaction, "deep_model"):
            self.central_core.ai.interaction.deep_model = getattr(
                __import__("deep_learning_model"), "DeepConversationalModel"
            )(model_name=model, lang=lang)
        self.status_bar.config(text=f"وضعیت سیستم: مدل={model} | زبان={lang}")
        self.update_chat(f"مدل عمیق به '{model}' و زبان به '{lang}' تغییر یافت.")

    def export_profile_gui(self):
        name = self.profile_var.get()
        if not name:
            messagebox.showwarning("انتخاب پروفایل", "لطفاً یک پروفایل انتخاب کنید.")
            return
        export_path = filedialog.asksaveasfilename(
            defaultextension=".json", filetypes=[("JSON Files", "*.json")]
        )
        if not export_path:
            return
        ok, msg = export_profile(name, export_path)
        self.update_chat(msg)

    def import_profile_gui(self):
        import_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if not import_path:
            return
        ok, msg = import_profile(import_path)
        self.refresh_profiles()
        self.update_chat(msg)

    def show_help_popup(self):
        help_text = (
            "راهنمای سریع رابط گرافیکی T13.3\n"
            "\n"
            "- انتخاب و جستجوی پروفایل: از combobox و باکس جستجو استفاده کنید.\n"
            "- ساخت/حذف/خلاصه/خروجی/ورود پروفایل با دکمه‌های مربوطه.\n"
            "- انتخاب مدل و زبان: combobox مدل و زبان را تغییر دهید.\n"
            "- نسخه‌های پشتیبان: دکمه 🗂️ لیست و جستجو و بازگردانی سریع.\n"
            "- نوتیفیکیشن: هشدارها در نوار بالای پنجره نمایش داده می‌شود.\n"
            "- جستجو و فیلتر: با تایپ در باکس جستجو، لیست‌ها فیلتر می‌شوند.\n"
            "- عملیات سریع: دکمه‌های پایین برای تحلیل احساسات، حافظه، تصمیم‌گیری و ...\n"
            "- حالت تاریک و مدرن فعال است.\n"
            "\nبرای توضیحات بیشتر به README.md مراجعه کنید."
        )
        messagebox.showinfo("راهنمای کاربری T13.3", help_text)

    def toggle_theme(self):
        style = ttk.Style(self.window)
        if self.current_theme == "dark":
            self.window.configure(bg="#f5f5f5")
            self.chat_frame.configure(style="TFrame")
            style.configure("TLabel", background="#f5f5f5", foreground="#222")
            style.configure("TButton", background="#e0e0e0", foreground="#222")
            self.chat_display.config(bg="#ffffff", fg="#222")
            self.notification_bar.config(bg="#ffe066", fg="#222")
            self.current_theme = "light"
        else:
            self.window.configure(bg="#181c24")
            self.chat_frame.configure(style="TFrame")
            style.configure("TLabel", background="#181c24", foreground="#fff")
            style.configure("TButton", background="#23272f", foreground="#ff3333")
            self.chat_display.config(bg="#181c24", fg="#00FF00")
            self.notification_bar.config(bg="#ffcc00", fg="#000")
            self.current_theme = "dark"

    def show_feedback_popup(self):
        win = tk.Toplevel(self.window)
        win.title("ارسال بازخورد یا گزارش خطا")
        ttk.Label(win, text="متن بازخورد یا خطا:").pack(padx=10, pady=10)
        text = tk.Text(win, width=60, height=8)
        text.pack(padx=10, pady=5)

        def submit():
            content = text.get("1.0", tk.END).strip()
            if not content:
                messagebox.showwarning("خطا", "متن بازخورد نمی‌تواند خالی باشد.")
                return
            import datetime

            with open("data/feedback.log", "a", encoding="utf-8") as f:
                f.write(f"[{datetime.datetime.now().isoformat()}] {content}\n---\n")
            self.show_notification("بازخورد شما ثبت شد. متشکریم!", level="info")
            win.destroy()

        ttk.Button(win, text="ارسال", command=submit).pack(pady=10)

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    gui = T13GUI()
    gui.run()
