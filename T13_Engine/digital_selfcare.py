# digital_selfcare.py

import gc
import logging
import os
import time
from datetime import datetime
from typing import Dict, List, Union, Any

import psutil

# کش برای ذخیره آخرین نتایج
_last_check_time = 0
_cached_health = None
_CACHE_DURATION = 1  # مدت زمان اعتبار کش به ثانیه


def get_system_health() -> Dict[str, Any]:
    """
    دریافت وضعیت سلامت سیستم شامل CPU، RAM، Latency و هشدارها.
    از کش استفاده می‌کند تا از فراخوانی بیش از حد جلوگیری شود.
    
    Returns:
        Dict[str, Any]: وضعیت سلامت و هشدارهای احتمالی
    """
    global _last_check_time, _cached_health
    
    current_time = time.time()
    if _cached_health and (current_time - _last_check_time) < _CACHE_DURATION:
        return _cached_health

    try:
        # محاسبه CPU با میانگین‌گیری
        cpu = psutil.cpu_percent(interval=0.1)
        
        # محاسبه RAM
        memory = psutil.virtual_memory()
        ram = memory.percent
        
        # محاسبه latency با تست عملیات I/O
        start = time.perf_counter()
        gc.collect()  # یک عملیات سیستمی ساده
        end = time.perf_counter()
        latency = (end - start) * 1000  # تبدیل به میلی‌ثانیه

        status = {
            "cpu": round(cpu, 1),
            "ram": round(ram, 1),
            "latency": round(latency, 2),
            "timestamp": datetime.now().isoformat(),
            "memory_available": f"{memory.available / (1024**3):.1f}GB",
            "memory_total": f"{memory.total / (1024**3):.1f}GB",
            "disk_percent": 0,
            "alert": []
        }

        # بررسی هشدارها
        if cpu > 85:
            status["alert"].append("مصرف CPU بالا")
        if ram > 90:
            status["alert"].append("حافظه در آستانه پر شدن است")
        if latency > 300:
            status["alert"].append("تاخیر بالا در عملیات سیستمی")
        
        # اضافه کردن اطلاعات دیسک
        try:
            disk = psutil.disk_usage('/')
            status["disk_percent"] = disk.percent
            if disk.percent > 90:
                status["alert"].append("فضای دیسک رو به اتمام است")
        except:
            pass

        # ثبت لاگ با ایجاد مسیر در صورت نیاز
        try:
            log_dir = os.path.join("data")
            if not os.path.exists(log_dir):
                os.makedirs(log_dir, exist_ok=True)
            
            log_path = os.path.join(log_dir, "selfcare_health.log")
            logging.basicConfig(
                filename=log_path,
                level=logging.INFO,
                format="%(asctime)s %(message)s",
                encoding="utf-8",
                force=True
            )
            
            log_msg = (f"Health Check - CPU: {status['cpu']}%, RAM: {status['ram']}%, "
                    f"Latency: {status['latency']:.1f}ms, Disk: {status['disk_percent']}%, "
                    f"Alerts: {', '.join(status['alert']) if status['alert'] else 'None'}")
            logging.info(log_msg)
        except Exception as e:
            print(f"Warning: Could not write to log file: {e}")

        # به‌روزرسانی کش
        _cached_health = status
        _last_check_time = current_time
        
        return status

    except Exception as e:
        # در صورت بروز خطا، یک وضعیت پیش‌فرض برگردان
        return {
            "cpu": 0,
            "ram": 0,
            "latency": 0,
            "timestamp": datetime.now().isoformat(),
            "memory_available": "N/A",
            "memory_total": "N/A",
            "disk_percent": 0,
            "alert": [f"خطا در دریافت وضعیت سیستم: {str(e)}"]
        }


def optimize_performance() -> None:
    """
    بهینه‌سازی منابع سیستم با جمع‌آوری garbage و آزادسازی حافظه.
    """
    gc.collect()
    if hasattr(psutil, "Process"):
        try:
            process = psutil.Process()
            process.memory_info()
        except psutil.NoSuchProcess:
            pass


def print_health_report(status: Dict[str, Any]) -> None:
    """
    چاپ گزارش سلامت سیستم به صورت متنی.
    
    Args:
        status (Dict[str, Any]): وضعیت سلامت سیستم
    """
    print("\n=== وضعیت سلامت سیستم ===")
    print(f"CPU Usage: {status['cpu']}%")
    print(f"RAM Usage: {status['ram']}%")
    print(f"Available Memory: {status['memory_available']}")
    print(f"Total Memory: {status['memory_total']}")
    print(f"Disk Usage: {status['disk_percent']}%")
    print(f"System Latency: {status['latency']:.1f}ms")
    
    alerts = status.get("alert", [])
    if alerts:
        print("\nSystem Alerts:")
        for alert in alerts:
            print(f"- {alert}")
    else:
        print("\nAll Systems Normal")
