import tkinter as tk
from tkinter import scrolledtext
import sys, threading
from t13_core import T13Engine
from t13_core_persona import T13Persona
from profile_manager import save_profile, load_profile, list_profiles
from t13_central import T13CentralCore
from digital_selfcare import get_system_health

ai = T13Engine(user_name="Erfan")
persona = T13Persona(ai)
central = T13CentralCore(profile_name="focus_mode")
options = ["Continue Project", "Take a Break", "Postpone"]

# --- Redirect stdout to output box ---
class RedirectText:
    def __init__(self, widget): self.widget = widget
    def write(self, string):
        self.widget.insert(tk.END, string)
        self.widget.see(tk.END)
    def flush(self): pass

def run_with_output(fn):
    output.delete(1.0, tk.END)
    sys.stdout = RedirectText(output)
    try:
        print("\n" + "-"*70)
        fn()
    except Exception as e:
        print(f"⚠️ Error: {e}")
    finally:
        sys.stdout = sys.__stdout__
        update_status_bar()

# --- Emotion input ---
def get_user_feelings():
    return {
        "joy": int(entry_joy.get() or 5),
        "stress": int(entry_stress.get() or 5),
        "hope": int(entry_hope.get() or 5),
        "fear": int(entry_fear.get() or 5),
        "energy": int(entry_energy.get() or 5)
    }

# --- GUI actions ---
def run_custom_all(): run_with_output(lambda: ai.run_all(get_user_feelings(), options))
def run_memory(): run_with_output(ai.run_memory)
def run_emotion(): run_with_output(lambda: ai.run_emotion(get_user_feelings()))
def run_decision(): run_with_output(lambda: ai.run_decision(options))
def run_behavior(): run_with_output(ai.run_behavior)
def run_upgrade(): run_with_output(ai.run_upgrade)
def run_health(): run_with_output(ai.run_health)
def run_trend(): run_with_output(ai.run_trend_analysis)
def run_multiverse(): run_with_output(ai.run_multiverse)

def show_personality():
    feelings = get_user_feelings()
    ai.emotion_score = feelings
    persona.set_mood(feelings)
    mode = persona.execute_behavior()
    msg = persona.adapt_response()
    run_with_output(lambda: print(f"🧠 Mood: {persona.mood}\n🎭 Behavior: {mode}\n💬 Response: {msg}"))

def run_central(): threading.Thread(target=lambda: run_with_output(central.run_all)).start()
def clear_output(): output.delete(1.0, tk.END)

def save_current_profile():
    feelings = get_user_feelings()
    name = profile_name.get().strip()
    if name:
        msg = save_profile(name, feelings)
        run_with_output(lambda: print(msg))
        refresh_profile_menu()
    else:
        run_with_output(lambda: print("⚠️ Enter profile name."))

def load_and_run_profile():
    name = profile_name.get().strip()
    if name:
        feelings, msg = load_profile(name)
        run_with_output(lambda: print(msg))
        if feelings: run_with_output(lambda: ai.run_all(feelings, options))
    else:
        run_with_output(lambda: print("⚠️ Enter profile name."))

def refresh_profile_menu():
    profiles = list_profiles()
    menu = profile_dropdown["menu"]
    menu.delete(0, "end")
    for p in profiles:
        menu.add_command(label=p, command=lambda v=p: profile_name.delete(0, tk.END) or profile_name.insert(0, v))

def update_status_bar():
    health = get_system_health()
    status = f"🧠 CPU: {health['cpu']}% | 💾 RAM: {health['ram']}% | ⏱️ Latency: {round(health['latency'], 2)} ms"
    status_bar.config(text=status)

# --- GUI Layout ---
root = tk.Tk()
root.title("T13.3 – Full AI Interface")
root.geometry("950x700")
root.configure(bg="#1e1e1e")

tk.Label(root, text="💠 T13.3 Full Central Interface", font=("Segoe UI", 18, "bold"),
         fg="#00FFD1", bg="#1e1e1e").pack(pady=8)

# Emotion inputs
form = tk.Frame(root, bg="#1e1e1e")
form.pack()
for i, lbl in enumerate(["Joy", "Stress", "Hope", "Fear", "Energy"]):
    tk.Label(form, text=lbl, fg="white", bg="#1e1e1e").grid(row=0, column=i, padx=5)
entry_joy = tk.Entry(form, width=5); entry_joy.grid(row=1, column=0)
entry_stress = tk.Entry(form, width=5); entry_stress.grid(row=1, column=1)
entry_hope = tk.Entry(form, width=5); entry_hope.grid(row=1, column=2)
entry_fear = tk.Entry(form, width=5); entry_fear.grid(row=1, column=3)
entry_energy = tk.Entry(form, width=5); entry_energy.grid(row=1, column=4)

tk.Button(root, text="🚀 Run with My Emotions", command=run_custom_all,
          bg="#007acc", fg="white", font=("Segoe UI", 11)).pack(pady=5)

# Profile
profile = tk.Frame(root, bg="#1e1e1e")
profile.pack(pady=5)
tk.Label(profile, text="Profile:", bg="#1e1e1e", fg="white").grid(row=0, column=0)
profile_name = tk.Entry(profile, width=25); profile_name.grid(row=0, column=1)
profile_dropdown = tk.OptionMenu(profile, profile_name, "")
profile_dropdown.config(width=15)
profile_dropdown.grid(row=0, column=2)
tk.Button(profile, text="💾 Save", command=save_current_profile, bg="#444", fg="white").grid(row=0, column=3)
tk.Button(profile, text="📂 Load & Run", command=load_and_run_profile, bg="#555", fg="white").grid(row=0, column=4)
refresh_profile_menu()

# Buttons
buttons = tk.Frame(root, bg="#1e1e1e")
buttons.pack(pady=5)
actions = [
    ("🧠 Personality", show_personality),
    ("🧬 Memory", run_memory),
    ("📊 Emotions", run_emotion),
    ("🧭 Decision", run_decision),
    ("🎭 Behavior", run_behavior),
    ("🔁 Upgrade", run_upgrade),
    ("🩺 Health", run_health),
    ("📈 Trend", run_trend),
    ("🎇 Creativity", run_multiverse),
    ("🎯 Run T13CentralCore", run_central),
    ("🧹 Clear Output", clear_output)
]
for txt, fn in actions:
    tk.Button(buttons, text=txt, command=fn, width=25, bg="#333", fg="white", font=("Arial", 10)).pack(pady=2)

# Output area
output = scrolledtext.ScrolledText(root, font=("Consolas", 11), bg="#000", fg="#0f0", insertbackground="white")
output.pack(expand=True, fill="both", padx=10, pady=10)

# Status bar
status_bar = tk.Label(root, text="", anchor="w", font=("Segoe UI", 10), bg="#1e1e1e", fg="#aaaaaa", pady=4)
status_bar.pack(fill="x", side="bottom")
update_status_bar()

root.mainloop()
