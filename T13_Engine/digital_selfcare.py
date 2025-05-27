# digital_selfcare.py

import gc
import logging
import time
from datetime import datetime

import psutil


def get_system_health():
    """
    دریافت وضعیت سلامت سیستم شامل CPU، RAM، Latency و هشدارها.
    خروجی:
        dict: وضعیت سلامت و هشدارهای احتمالی
    """
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent

    # اصلاح محاسبه latency با یک عملیات ساده قابل اندازه‌گیری
    start = time.time()
    end = time.time()
    latency = round((end - start) * 1000, 2)  # به میلی‌ثانیه

    status = {
        "cpu": cpu,
        "ram": ram,
        "latency": latency,
        "timestamp": datetime.now().isoformat(),
    }

    alert = []
    if cpu > 85:
        alert.append("⚠️ مصرف CPU بالا")
    if ram > 90:
        alert.append("⚠️ حافظه در آستانه پر شدن است")
    if latency > 300:
        alert.append("⚠️ تاخیر بالا – ممکن است مشکلی در پردازش باشد")

    status["alert"] = alert
    # ثبت لاگ سلامت سیستم
    logging.basicConfig(
        filename="data/selfcare_health.log",
        level=logging.INFO,
        format="%(asctime)s %(message)s",
        encoding="utf-8",
    )
    log_msg = f"CPU: {cpu}%, RAM: {ram}%, Latency: {latency}ms, Alerts: {alert}"
    logging.info(log_msg)
    return status


def optimize_performance():
    """
    بهینه‌سازی منابع سیستم با جمع‌آوری garbage و آزادسازی حافظه.
    """
    gc.collect()
    print("✅ بهینه‌سازی منابع سیستم انجام شد.")


def print_health_report(status):
    """
    چاپ گزارش سلامت سیستم به صورت متنی.
    ورودی:
        status (dict): وضعیت سلامت سیستم
    """
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
