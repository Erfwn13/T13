# memory_core.py

import json
import os
from encryption_utils import encrypt_json, decrypt_json
from database_utils import set_memory, get_memory, get_all_memory


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