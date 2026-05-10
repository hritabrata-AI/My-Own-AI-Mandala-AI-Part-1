import os
import google.generativeai as genai
import sys
import time
import json

# --- 1. SETTINGS & API CONFIG ---
# Your verified API key
API_KEY = "AIzaSyCNo4GVfb8EORgvpmgdkRsvSqWi6ItR-2s"

try:
    genai.configure(api_key=API_KEY)
    # Using the 2026 standard model
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception as e:
    print(f"Setup Error: {e}")

WHITE_BG = "\033[48;5;15m"
BLACK_TEXT = "\033[38;5;0m"
RESET = "\033[0m"
DATA_FILE = "user_data.json"

# --- 2. DATA MANAGEMENT ---
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"name": "Hritabrata", "history": []}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def type_speed(text):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.01)
    print()

# --- 3. THE HYBRID BRAIN ---
def get_response(user_input, data):
    ui = user_input.lower().strip()

    # A. REFINED PERSONALITY RULES
    # Only triggers if you specifically ask about IT'S creator or mention your name
    if any(word in ui for word in ["who made you", "your creator", "hritabrata"]):
        return "You made me, Hritabrata! I am Mandala AI, powered by the latest Gemini 2.5 Transformer architecture."

    if "thank you" in ui:
        return "You're very welcome! I'm here to help."

    # B. CLOUD TRANSFORMER LOGIC
    try:
        system_instructions = (
            "You are Mandala AI, a helpful assistant created by Hritabrata Mondal. "
            "You are an expert in 9th-grade Math, Biology, and Coding. "
            "Provide clear, accurate, and encouraging answers."
        )
        full_prompt = f"{system_instructions}\n\nUser: {user_input}"
        
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        # Fallback to lite version if main model is busy
        try:
            alt_model = genai.GenerativeModel('gemini-2.5-flash-lite')
            return alt_model.generate_content(user_input).text
        except:
            return f"Technical Error: {e}\n(Tip: Check your internet or API status)"

# --- 4. MAIN LOOP ---
user_data = load_data()
os.system('clear')

# Visual Banner
print(f"{WHITE_BG}{BLACK_TEXT}")
print("   " + "━" * 36)
print("   MANDALA AI: TRANSFORMER EDITION  ".center(40))
print(f"   Developer: Hritabrata Mondal".center(40))
print("   " + "━" * 36 + RESET + "\n")

while True:
    try:
        user_q = input(f"{WHITE_BG}{BLACK_TEXT}   {user_data['name']}: {RESET} ")
        
        if user_q.lower() in ['exit', 'quit', 'bye']:
            type_speed("\n   Mandala AI: Goodbye, boss! Session saved.")
            break
        
        user_data["history"].append(user_q)
        save_data(user_data)
        
        answer = get_response(user_q, user_data)
        
        sys.stdout.write(f"{WHITE_BG}{BLACK_TEXT}\n   Mandala AI: ")
        type_speed(answer)
        print(f"   {'-'*34}\n{RESET}")
        
    except (EOFError, KeyboardInterrupt):
        break
