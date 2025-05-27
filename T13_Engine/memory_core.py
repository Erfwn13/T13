# memory_core.py

import json
import os

from database_utils import get_all_memory, get_memory, set_memory
from encryption_utils import decrypt_json, encrypt_json

MEMORY_FILE = "data/memory.json.enc"  # تغییر نام فایل به نسخه رمزنگاری‌شده


def load_memory():
    return get_all_memory()


def save_memory(data):
    for key, value in data.items():
        set_memory(key, value)


def get_fact(key):
    return get_memory(f"facts:{key}")


def set_fact(key, value):
    set_memory(f"facts:{key}", value)


# filepath: T13/T13_Engine/memory_core.py
class MemoryManager:
    def __init__(self):
        self.memory = {}

    def add_fact(self, key, value):
        self.memory[key] = value

    def get_fact(self, key):
        return self.memory.get(key, "اطلاعاتی یافت نشد.")

    def clean_memory(self):
        # حذف داده‌های قدیمی که شامل "old" هستند (مثال)
        keys_to_remove = [
            key for key, value in self.memory.items() if "old" in str(value)
        ]
        for key in keys_to_remove:
            del self.memory[key]
