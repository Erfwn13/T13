import random
import time
import tkinter as tk
from tkinter import ttk

import matplotlib.pyplot as plt
from digital_selfcare import get_system_health
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class PerformanceDashboard:
    def __init__(self, parent):
        """
        ایجاد یک داشبورد عملکرد که نمودار عملکرد را به‌صورت زنده نشان می‌دهد.
        """
        self.parent = parent
        self.frame = ttk.Frame(self.parent)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.fig, self.ax = plt.subplots(figsize=(5, 3))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.x_data = []
        self.y_data = []
        self.start_time = time.time()

        self.ax.set_title("Performance Monitor")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Avg Emotion")

    def update_chart(self, avg_emotion):
        """
        به‌روزرسانی نمودار با یک مقدار میانگین احساسات جدید.
        """
        current_time = time.time() - self.start_time
        self.x_data.append(current_time)
        self.y_data.append(avg_emotion)

        self.ax.clear()
        self.ax.plot(self.x_data, self.y_data, marker="o", color="tab:blue")
        self.ax.set_title("Performance Monitor")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Avg Emotion")
        self.canvas.draw()

    def update_health_status(self, health_status):
        """
        نمایش وضعیت سلامت سیستم (CPU، RAM، Latency، هشدارها) در داشبورد
        """
        if hasattr(self, "health_label"):
            self.health_label.destroy()
        alerts = "\n".join(health_status.get("alert", []))
        text = (
            f"🧠 CPU: {health_status['cpu']}%\n"
            f"💾 RAM: {health_status['ram']}%\n"
            f"⏱️ Latency: {health_status['latency']} ms\n"
            f"{alerts or 'وضعیت بهینه'}"
        )
        self.health_label = tk.Label(
            self.frame,
            text=text,
            font=("Segoe UI", 10),
            fg="red" if alerts else "green",
            bg="black",
        )
        self.health_label.pack(side=tk.BOTTOM, fill=tk.X, pady=5)


if __name__ == "__main__":
    # اجرای نمونه داشبورد عملکرد برای تست
    root = tk.Tk()
    root.title("Performance Dashboard")
    dashboard = PerformanceDashboard(root)

    def simulate_data():
        # تولید داده تصادفی میانگین احساس برای شبیه‌سازی عملکرد سیستم
        avg_emotion = random.uniform(0, 10)
        dashboard.update_chart(avg_emotion)
        health = get_system_health()
        dashboard.update_health_status(health)
        root.after(1000, simulate_data)

    simulate_data()
    root.mainloop()
