from flask import Flask, render_template, request, jsonify
import os
import time
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

# ==========================
# MEMORY (simple dictionary)
# ==========================
MEMORY = {
    "name": None,
    "favorite_game": None,
    "favorite_movie": None,
}

# ==========================
# BASIC PREDEFINED ANSWERS
# ==========================
PREDEFINED = {
    "game recommendations": "RDR2, Ghost of Tsushima, GTA V, Hitman WOA, Forza Horizon, Assassin’s Creed, Ace Combat 7.",
    "greatest football players": "Ronaldo, Messi, Ramos, Neymar, Mbappe.",
    "powerhouse of the cell": "Mitochondria.",
    "best movies": "Transformers, John Wick, Terminator, Fast & Furious, Fight Club, Red Notice, Avengers.",
    "famous comic characters": "Batman, Superman, Spiderman, Iron Man, Deadpool, Black Widow, Hulk."
}

# ================================
# DATE INTELLIGENCE
# ================================
def date_ai(text):
    text = text.lower()
    now = datetime.now()

    if "today" in text:
        return f"Today is {now.strftime('%d %B %Y')} ({now.strftime('%A')})."

    if "tomorrow" in text:
        tm = now + timedelta(days=1)
        return f"Tomorrow is {tm.strftime('%d %B %Y')} ({tm.strftime('%A')})."

    if "day after" in text:
        da = now + timedelta(days=2)
        return f"The day after tomorrow is {da.strftime('%d %B %Y')} ({da.strftime('%A')})."

    if "yesterday" in text:
        ys = now - timedelta(days=1)
        return f"Yesterday was {ys.strftime('%d %B %Y')} ({ys.strftime('%A')})."

    return None

# ================================
# WORLD KNOWLEDGE AI
# ================================
def world_ai(text):
    text = text.lower()

    if "world" in text or "earth" in text:
        return (
            "The world is around 4.5 billion years old. Humans appeared about 300,000 years ago. "
            "The Earth has 195 countries and supports life due to water and atmosphere."
        )

    if "india" in text:
        return (
            "India is one of the world's oldest civilizations. Birthplace of zero, yoga, ayurveda, and the largest democracy."
        )

    if "sun" in text:
        return "The Sun is a 4.6-billion-year-old star made of hydrogen and helium."

    if "moon" in text:
        return "The Moon formed 4.5 billion years ago and controls tides on Earth."

    return None

# ================================
# GEMINI AI FALLBACK
# ================================
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")

def call_gemini(prompt):
    if not GEMINI_KEY:
        return "AI mode not configured yet."

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_KEY}"

    payload = {
        "contents": [{
            "parts": [{"text": f"You are PabloBot. Use simple, formal, respectful language.\nUser: {prompt}"}]
        }]
    }

    res = requests.post(url, json=payload)
    j = res.json()

    try:
        return j["candidates"][0]["content"]["parts"][0]["text"]
    except:
        return "I am unable to think clearly right now. Try again."

# ================================
# FINAL REPLY LOGIC
# ================================
def generate_reply(message):
    msg = message.lower()

    # ---------------- Predefined ----------------
    for key, value in PREDEFINED.items():
        if key in msg:
            return value

    # --------------- Memory name save -----------
    if "my name is" in msg:
        MEMORY["name"] = message.split("is")[-1].strip()
        return f"Nice to meet you, {MEMORY['name']}."

    if "what is my name" in msg:
        return MEMORY["name"] if MEMORY["name"] else "I do not know your name yet."

    # --------------- Date AI --------------------
    d = date_ai(msg)
    if d:
        return d

    # --------------- World AI -------------------
    w = world_ai(msg)
    if w:
        return w

    # --------------- Calculator trigger ---------
    if "calculator" in msg or "transform into a calculator" in msg:
        return "__open_calculator__"

    # --------------- Gemini fallback ------------
    return call_gemini(message)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    message = data.get("message", "")
    reply = generate_reply(message)
    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(debug=True)
