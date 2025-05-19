# digital_selfcare.py

import psutil
import time
from datetime import datetime

def get_system_health():
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent

    # اصلاح محاسبه latency با یک عملیات ساده قابل اندازه‌گیری
    start = time.time()
    for _ in range(10000): pass  # یک عملیات سبک برای تست تاخیر
    end = time.time()
    latency = round((end - start) * 1000, 2)  # به میلی‌ثانیه

    status = {
        "cpu": cpu,
        "ram": ram,
        "latency": latency,
        "timestamp": datetime.now().isoformat()
    }

    alert = []
    if cpu > 85:
        alert.append("⚠️ مصرف CPU بالا")
    if ram > 90:
        alert.append("⚠️ حافظه در آستانه پر شدن است")
    if latency > 300:
        alert.append("⚠️ تاخیر بالا – ممکن است مشکلی در پردازش باشد")

    status["alert"] = alert
    return status

def print_health_report(status):
    print("\n🩺 وضعیت سلامت سیستم:")
    print(f"🧠 CPU: {status['cpu']}%")
    print(f"💾 RAM: {status['ram']}%")
    print(f"⏱️ Latency: {status['latency']} ms")

    if status["alert"]:
        print("🚨 هشدارها:")
        for a in status["alert"]:
            print("➤", a)
    else:
        print("✅ سیستم در وضعیت بهینه است.")
