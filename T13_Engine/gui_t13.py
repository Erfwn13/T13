# gui_t13.py

import tkinter as tk
from tkinter import scrolledtext
import sys
from t13_central import T13CentralCore
from t13_core import T13Engine
from t13_core_persona import T13Persona
from profile_manager import save_profile, load_profile, list_profiles

# Initialize core AI objects
ai = T13Engine(user_name="Erfan")
persona = T13Persona(ai)
central = T13CentralCore(profile_name="focus_mode")
options = ["Continue Project", "Take a Break", "Postpone"]

# Redirect stdout into the GUI text box
class RedirectText:
    def __init__(self, widget):
        self.widget = widget
    def write(self, string):
        self.widget.insert(tk.END, string)
        self.widget.see(tk.END)
    def flush(self):
        pass

def run_with_output(fn):
    output.delete(1.0, tk.END)
    sys.stdout = RedirectText(output)
    try:
        fn()
    except Exception as e:
        print(f"⚠️ Error: {e}")
    finally:
        sys.stdout = sys.__stdout__

# Helpers for emotion input
def get_user_feelings():
    return {
        "joy": int(entry_joy.get() or 5),
        "stress": int(entry_stress.get() or 5),
        "hope": int(entry_hope.get() or 5),
        "fear": int(entry_fear.get() or 5),
        "energy": int(entry_energy.get() or 5)
    }

# Button callbacks
def run_custom_all():
    feelings = get_user_feelings()
    run_with_output(lambda: ai.run_all(feelings, options))

def save_current_profile():
    feelings = get_user_feelings()
    name = entry_profile.get().strip()
    if name:
        msg = save_profile(name, feelings)
        run_with_output(lambda: print(msg))
        refresh_profile_list()
    else:
        run_with_output(lambda: print("⚠️ Enter a profile name first."))

def load_and_run_profile():
    name = entry_profile.get().strip()
    if not name:
        return run_with_output(lambda: print("⚠️ Enter a profile name to load."))
    feelings, msg = load_profile(name)
    run_with_output(lambda: print(msg))
    if feelings:
        run_with_output(lambda: ai.run_all(feelings, options))

def show_personality():
    feelings = get_user_feelings()
    ai.emotion_score = feelings
    persona.set_mood(feelings)
    mode = persona.execute_behavior()
    resp = persona.adapt_response()
    run_with_output(lambda: print(
        f"🧠 T13 Mood: {persona.mood}\n"
        f"🎭 Suggested Behavior: {mode}\n"
        f"💬 Response: {resp}"
    ))

def run_central():
    run_with_output(lambda: central.run_all())

def refresh_profile_list():
    profiles = list_profiles()
    menu = profile_menu["menu"]
    menu.delete(0, "end")
    for p in profiles:
        menu.add_command(label=p, command=lambda v=p: entry_profile.delete(0, tk.END) or entry_profile.insert(0, v))

# Build GUI
root = tk.Tk()
root.title("T13.3 Central GUI")
root.geometry("800x650")
root.configure(bg="#1e1e1e")

tk.Label(root, text="💠 T13.3 AI Central Interface", font=("Arial", 18, "bold"), fg="#00ffd1", bg="#1e1e1e").pack(pady=8)

# Emotion input frame
frm_emotions = tk.Frame(root, bg="#1e1e1e")
frm_emotions.pack(pady=5)
for idx, label in enumerate(["Joy","Stress","Hope","Fear","Energy"]):
    tk.Label(frm_emotions, text=label, fg="white", bg="#1e1e1e").grid(row=0, column=idx, padx=5)
entry_joy = tk.Entry(frm_emotions, width=5); entry_joy.grid(row=1,column=0)
entry_stress = tk.Entry(frm_emotions, width=5); entry_stress.grid(row=1,column=1)
entry_hope = tk.Entry(frm_emotions, width=5); entry_hope.grid(row=1,column=2)
entry_fear = tk.Entry(frm_emotions, width=5); entry_fear.grid(row=1,column=3)
entry_energy = tk.Entry(frm_emotions, width=5); entry_energy.grid(row=1,column=4)
tk.Button(root, text="🚀 Run with My Emotions", command=run_custom_all, bg="#007acc", fg="white").pack(pady=5)

# Profile management
frm_profile = tk.Frame(root, bg="#1e1e1e")
frm_profile.pack(pady=5)
tk.Label(frm_profile, text="Profile:", fg="white", bg="#1e1e1e").grid(row=0,column=0)
entry_profile = tk.Entry(frm_profile, width=20); entry_profile.grid(row=0,column=1, padx=5)
profile_menu = tk.OptionMenu(frm_profile, entry_profile, "")  # will be populated
profile_menu.config(width=15)
profile_menu.grid(row=0, column=2)
tk.Button(frm_profile, text="💾 Save", command=save_current_profile, bg="#444", fg="white").grid(row=0,column=3, padx=5)
tk.Button(frm_profile, text="📂 Load & Run", command=load_and_run_profile, bg="#555", fg="white").grid(row=0,column=4)
refresh_profile_list()

# Control buttons
frm_buttons = tk.Frame(root, bg="#1e1e1e")
frm_buttons.pack(pady=5)
buttons = [
    ("🧠 Personality", show_personality),
    ("🎯 Run Central Core", run_central)
]
for txt, cmd in buttons:
    tk.Button(frm_buttons, text=txt, command=cmd, width=20, bg="#333", fg="white").pack(side="left", padx=5)

# Output area
output = scrolledtext.ScrolledText(root, bg="#252526", fg="#d4d4d4", font=("Consolas", 11))
output.pack(fill="both", expand=True, padx=10, pady=10)

root.mainloop()
