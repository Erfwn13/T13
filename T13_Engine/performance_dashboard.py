import random
import time
import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from digital_selfcare import get_system_health
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class PerformanceDashboard:
    def __init__(self, parent):
        """
        ایجاد یک داشبورد عملکرد که نمودار عملکرد را به‌صورت زنده نشان می‌دهد.
        """
        self.parent = parent
        self.frame = ttk.Frame(self.parent)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # ایجاد نمودار با استایل مدرن
        plt.style.use('dark_background')
        self.fig = Figure(figsize=(8, 4), dpi=100)
        self.fig.patch.set_facecolor('#2b2b2b')
        
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor('#1c1c1c')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # داده‌های نمودار
        self.x_data = []
        self.y_data = []
        self.start_time = time.time()
        self.update_interval = 1000  # میلی‌ثانیه
        self.is_running = True

        # تنظیم عنوان‌ها و استایل نمودار
        self._setup_chart_style()
        
        # ایجاد و تنظیم لیبل‌های وضعیت
        self._setup_status_labels()
        
        # شروع به‌روزرسانی خودکار
        self.start_auto_update()

    def _setup_chart_style(self):
        """تنظیم استایل اولیه نمودار"""
        self.ax.set_title("System Performance Monitor", color='white', pad=10, fontsize=12)
        self.ax.set_xlabel("Time (s)", color='white', labelpad=10)
        self.ax.set_ylabel("Performance Score", color='white', labelpad=10)
        self.ax.tick_params(colors='white')
        self.ax.grid(True, color='#404040', linestyle='--', alpha=0.3)

    def _setup_status_labels(self):
        """ایجاد و تنظیم لیبل‌های نمایش وضعیت سیستم"""
        # فریم وضعیت
        self.status_frame = ttk.Frame(self.frame)
        self.status_frame.pack(fill=tk.X, pady=5)
          # تنظیمات مشترک لیبل‌ها
        label_config = {
            "fg": "#00ff00",
            "bg": "#1c1c1c",
            "padx": 10,
            "pady": 5
        }
        
        # ایجاد لیبل‌های وضعیت با فونت عادی
        normal_label_config = {**label_config, "font": ("Segoe UI", 10)}
        bold_label_config = {**label_config, "font": ("Segoe UI", 10, "bold")}
        
        self.cpu_label = tk.Label(self.status_frame, text="CPU: 0%", **normal_label_config)
        self.cpu_label.pack(side=tk.LEFT, padx=5)

        self.ram_label = tk.Label(self.status_frame, text="RAM: 0%", **normal_label_config)
        self.ram_label.pack(side=tk.LEFT, padx=5)

        self.latency_label = tk.Label(self.status_frame, text="Latency: 0ms", **normal_label_config)
        self.latency_label.pack(side=tk.LEFT, padx=5)

        self.alert_label = tk.Label(
            self.frame,
            text="System Status: Normal",
            **bold_label_config
        )
        self.alert_label.pack(fill=tk.X, pady=5)

    def start_auto_update(self):
        """شروع به‌روزرسانی خودکار داشبورد"""
        if hasattr(self, 'parent') and self.parent.winfo_exists():
            self.update_dashboard()
            self.parent.after(self.update_interval, self.start_auto_update)

    def stop_auto_update(self):
        """توقف به‌روزرسانی خودکار"""
        self.is_running = False

    def update_dashboard(self):
        """به‌روزرسانی همزمان نمودار و وضعیت سیستم"""
        try:
            # دریافت داده‌های سیستم
            health = get_system_health()
            performance_score = (100 - health['cpu']) * 0.4 + (100 - health['ram']) * 0.4 + (100 - min(health['latency'], 100)) * 0.2
            performance_score = max(0, min(10, performance_score / 10))  # تبدیل به مقیاس 0-10
            
            # به‌روزرسانی همزمان
            self.update_chart(performance_score)
            self.update_health_status(health)
            
        except Exception as e:
            print(f"Error updating dashboard: {e}")
            self.alert_label.config(text=f"Error: {str(e)}", fg="#ff0000")

    def update_chart(self, performance_score):
        """
        به‌روزرسانی نمودار با یک مقدار عملکرد جدید
        """
        current_time = time.time() - self.start_time
        self.x_data.append(current_time)
        self.y_data.append(performance_score)

        # نگه داشتن فقط 60 نقطه آخر
        if len(self.x_data) > 60:
            self.x_data = self.x_data[-60:]
            self.y_data = self.y_data[-60:]

        self.ax.clear()
        self.ax.plot(self.x_data, self.y_data, marker="o", color="#00ff00", 
                    linewidth=2, markersize=4, alpha=0.8)
        
        self._setup_chart_style()
        self.ax.set_facecolor('#1c1c1c')
        self.ax.set_ylim(0, 10)
        
        self.fig.tight_layout()
        try:
            self.canvas.draw()
        except Exception:
            pass  # اگر کنوس از بین رفته باشد

    def update_health_status(self, health_status):
        """
        به‌روزرسانی نمایش وضعیت سلامت سیستم
        """
        try:
            # به‌روزرسانی لیبل‌های وضعیت
            cpu_usage = health_status['cpu']
            ram_usage = health_status['ram']
            latency = health_status['latency']
            
            # تنظیم رنگ بر اساس مقادیر
            cpu_color = "#00ff00" if cpu_usage < 70 else "#ffff00" if cpu_usage < 90 else "#ff0000"
            ram_color = "#00ff00" if ram_usage < 70 else "#ffff00" if ram_usage < 90 else "#ff0000"
            latency_color = "#00ff00" if latency < 100 else "#ffff00" if latency < 200 else "#ff0000"

            self.cpu_label.config(text=f"CPU: {cpu_usage:.1f}%", fg=cpu_color)
            self.ram_label.config(text=f"RAM: {ram_usage:.1f}%", fg=ram_color)
            self.latency_label.config(text=f"Latency: {latency:.1f}ms", fg=latency_color)

            # نمایش هشدارها
            alerts = health_status.get("alert", [])
            if alerts:
                alert_text = "⚠️ " + " | ".join(alerts)
                self.alert_label.config(text=alert_text, fg="#ff0000")
            else:
                self.alert_label.config(text="System Status: Normal", fg="#00ff00")

        except Exception as e:
            print(f"Error updating health status: {e}")

    def __del__(self):
        """تمیزکاری منابع هنگام حذف داشبورد"""
        self.stop_auto_update()
        plt.close(self.fig)


if __name__ == "__main__":
    # اجرای نمونه داشبورد عملکرد برای تست
    root = tk.Tk()
    root.title("T13 Performance Dashboard")
    root.configure(bg='#1c1c1c')
    root.minsize(800, 600)
    
    dashboard = PerformanceDashboard(root)
    root.mainloop()
