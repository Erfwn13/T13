# echo_engine.py

import random


def echo_response(mode, message, energy):
    if mode == "ShadowBoost":
        return shadow_echo(message, energy)
    elif mode == "ChillCompanion":
        return chill_echo(message)
    elif mode == "ChaosSpark":
        return chaos_echo(message)
    elif mode == "SafeSupport":
        return safe_echo(message)
    else:
        return message


def shadow_echo(msg, energy):
    lines = [
        f"🔥 {msg.upper()}!",
        f"⚡ You're built for greatness — {msg}.",
        f"🚀 It's your time. {msg.capitalize()} now!",
        f"🎯 Stay locked in: {msg}.",
    ]
    return random.choice(lines) if energy >= 7 else f"Keep pushing... {msg}"


def chill_echo(msg):
    lines = [
        f"🌿 Take a breath... {msg.lower()}.",
        f"☁️ Let's move gently: {msg}.",
        f"🧘‍♂️ Everything's okay. Just {msg.lower()} and flow.",
        f"🎶 Calm rhythm: {msg.lower()}...",
    ]
    return random.choice(lines)


def chaos_echo(msg):
    sparks = [
        f"✨ What if we flipped it? {msg.upper()} with fireworks!",
        f"⚡ Boom! {msg.capitalize()} — but backwards.",
        f"🌀 Let it twist: {msg}… but sideways.",
        f"🔥 Wild idea: don't just {msg}, revolutionize it!",
    ]
    return random.choice(sparks)


def safe_echo(msg):
    comforts = [
        f"🛡 You're safe here. Let's just {msg}.",
        f"🤝 No pressure. We can take it slow: {msg}.",
        f"🧩 Step by step, we’ll get there — {msg.lower()} together.",
        f"🕊 It's okay. Just {msg.lower()}, no rush.",
    ]
    return random.choice(comforts)
