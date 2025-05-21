import sqlite3
import json

DB_FILE = "data/t13_database.db"

def init_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # ایجاد جدول حافظه
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)

    conn.commit()
    conn.close()
    print("✅ جدول حافظه ایجاد شد یا از قبل وجود داشت.")

def initialize_database():
    connection = sqlite3.connect("database.db")  # مسیر پایگاه داده خود را جایگزین کنید
    cursor = connection.cursor()
    
    # ایجاد جدول memory در صورت عدم وجود
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)
    
    # افزودن داده پیش‌فرض (اختیاری)
    cursor.execute("""
        INSERT OR IGNORE INTO memory (key, value) VALUES (?, ?)
    """, ("facts:creator", "Erfan"))
    
    connection.commit()
    connection.close()

# ذخیره یک مقدار در پایگاه داده
def set_memory(key, value):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO memory (key, value)
        VALUES (?, ?)
    """, (key, value))
    conn.commit()
    conn.close()

# بازیابی یک مقدار از پایگاه داده
def get_memory(key):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT value FROM memory WHERE key = ?
    """, (key,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

# بازیابی تمام داده‌ها
def get_all_memory():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT key, value FROM memory
    """)
    rows = cursor.fetchall()
    conn.close()
    return {key: value for key, value in rows}

def save_conversation(conversation_history):
    with open("conversation_history.json", "w", encoding="utf-8") as file:
        json.dump(conversation_history, file, ensure_ascii=False, indent=4)

def load_conversation():
    try:
        with open("conversation_history.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []