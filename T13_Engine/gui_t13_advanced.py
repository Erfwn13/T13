# gui_t13_advanced.py

import tkinter as tk
from tkinter import scrolledtext
import sys, threading
from t13_central import T13CentralCore
from memory_core import set_fact
from digital_selfcare import get_system_health

# GUI output redirection
class RedirectText:
    def __init__(self, widget):
        self.widget = widget
    def write(self, string):
        self.widget.insert(tk.END, string)
        self.widget.see(tk.END)
    def flush(self):
        pass

# Run T13Core in a thread
def run_t13_core():
    set_fact("creator", "Erfan")
    sys.stdout = RedirectText(output_box)

    try:
        print("\n" + "-"*70)
        print("🚀 Starting T13CentralCore Execution...\n")
        core = T13CentralCore(profile_name="focus_mode")
        core.run_all()
        print("\n✅ Execution Complete.\n")
    except Exception as e:
        print(f"⚠️ Error: {e}")
    finally:
        sys.stdout = sys.__stdout__
        update_status_bar()

def run_threaded():
    threading.Thread(target=run_t13_core).start()

# Clear output
def clear_output():
    output_box.delete(1.0, tk.END)

# Show system status
def update_status_bar():
    health = get_system_health()
    status = f"🧠 CPU: {health['cpu']}% | 💾 RAM: {health['ram']}% | ⏱️ Latency: {round(health['latency'], 2)} ms"
    status_bar.config(text=status)

# GUI Layout
window = tk.Tk()
window.title("🧠 T13.3 Central Interface - Pro Edition")
window.geometry("900x650")
window.config(bg="#1e1e1e")

# Header
header = tk.Label(window, text="T13.3 Central Interface", font=("Segoe UI", 20, "bold"), fg="cyan", bg="#1e1e1e")
header.pack(pady=10)

# Button panel
btn_frame = tk.Frame(window, bg="#1e1e1e")
btn_frame.pack(pady=5)

tk.Button(btn_frame, text="▶️ Run T13CentralCore", command=run_threaded,
          font=("Segoe UI", 12), bg="#007acc", fg="white", width=22).pack(side="left", padx=8)

tk.Button(btn_frame, text="🧹 Clear Output", command=clear_output,
          font=("Segoe UI", 12), bg="#333", fg="white", width=15).pack(side="left", padx=8)

# Output area
output_box = scrolledtext.ScrolledText(window, font=("Consolas", 11), bg="#252526", fg="#d4d4d4", wrap=tk.WORD)
output_box.pack(expand=True, fill="both", padx=20, pady=10)

# Status bar
status_bar = tk.Label(window, text="Initializing...", anchor="w", font=("Segoe UI", 10),
                      bg="#1e1e1e", fg="#aaaaaa", pady=5)
status_bar.pack(fill="x", side="bottom")

update_status_bar()
window.mainloop()
