"""
J.A.R.V.I.S - Advanced AI Assistant Backend  v3.0
===================================================
HOW TO RUN:
  1. pip install flask flask-socketio pyttsx3 speechrecognition pyaudio
                 requests pyautogui plyer pygame speedtest-cli
                 beautifulsoup4 wikipedia-api pyjokes psutil
                 deep-translator pyperclip
  2. Place jarvismain.py + jarvis_ui.html in the SAME folder
  3. python jarvismain.py
  4. Open Chrome → http://localhost:8000
"""

import pyttsx3
import speech_recognition
import requests
import datetime
import os
import sys
import time
import random
import threading
import webbrowser
import subprocess
import platform
import socket
import json
import re
import pyautogui

from flask import Flask, send_file, request, jsonify
from flask_socketio import SocketIO, emit

# ─────────────────────────────────────────────────────
#  BASE DIR
# ─────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ─────────────────────────────────────────────────────
#  WAKE / SLEEP WORDS
# ─────────────────────────────────────────────────────
WAKE_WORDS  = ["jarvis", "hey jarvis", "hello jarvis", "wake up jarvis",
               "wake up", "yo jarvis", "ok jarvis", "hi jarvis", "are you there"]
SLEEP_WORDS = ["go to sleep", "sleep jarvis", "goodbye jarvis",
               "bye jarvis", "jarvis sleep", "shutdown jarvis", "good night jarvis"]

def is_wake_word(q):  return any(w in q for w in WAKE_WORDS)
def is_sleep_word(q): return any(w in q for w in SLEEP_WORDS)

# ─────────────────────────────────────────────────────
#  TTS ENGINE
# ─────────────────────────────────────────────────────
engine     = pyttsx3.init("sapi5")
voices     = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 165)
engine.setProperty("volume", 1.0)
speak_lock = threading.Lock()

def speak(text: str):
    """Speak aloud and push text to UI terminal."""
    print(f"[JARVIS] {text}")
    with speak_lock:
        engine.say(text)
        engine.runAndWait()
    socketio.emit("log", {"msg": text, "type": "speak"})

def speak_async(text: str):
    """Non-blocking speak."""
    threading.Thread(target=speak, args=(text,), daemon=True).start()

# ─────────────────────────────────────────────────────
#  FLASK + SOCKETIO
# ─────────────────────────────────────────────────────
app = Flask(__name__)
app.config["SECRET_KEY"] = "jarvis-v3-secret"
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

# ─────────────────────────────────────────────────────
#  GLOBAL STATE
# ─────────────────────────────────────────────────────
authenticated = False
jarvis_awake  = False
mic_running   = False
conversation_history = []   # stores last N exchanges
alarm_threads = []          # active alarm threads
reminders     = []          # active reminder list

# ─────────────────────────────────────────────────────
#  SERVE UI
# ─────────────────────────────────────────────────────
@app.route("/")
def index():
    ui = os.path.join(BASE_DIR, "jarvis_ui.html")
    if not os.path.exists(ui):
        return f"<h2 style='font-family:monospace;color:red'>jarvis_ui.html not found at {ui}</h2>", 404
    resp = send_file(ui, mimetype="text/html")
    resp.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    resp.headers["Pragma"]  = "no-cache"
    resp.headers["Expires"] = "0"
    return resp

# ─────────────────────────────────────────────────────
#  AUTH
# ─────────────────────────────────────────────────────
@app.route("/api/auth", methods=["POST"])
def auth():
    global authenticated
    data    = request.get_json(force=True)
    entered = data.get("password", "").strip()
    pw_file = os.path.join(BASE_DIR, "password.txt")
    if not os.path.exists(pw_file):
        with open(pw_file, "w") as f: f.write("1234")
    with open(pw_file, "r") as f:
        stored = f.read().strip()
    if entered == stored:
        authenticated = True
        hour  = datetime.datetime.now().hour
        greet = "Good morning" if hour < 12 else "Good afternoon" if hour < 18 else "Good evening"
        return jsonify({"success": True,
                        "message": f"{greet}. Authentication successful. Voice systems are online."})
    return jsonify({"success": False, "message": "Incorrect password. Try again."})

# ─────────────────────────────────────────────────────
#  VOICE AUTH — called when mic permission is granted
#  Sets backend authenticated=True without password
# ─────────────────────────────────────────────────────
@app.route("/api/voice-auth", methods=["POST"])
def voice_auth():
    global authenticated
    authenticated = True
    hour  = datetime.datetime.now().hour
    greet = "Good morning" if hour < 12 else "Good afternoon" if hour < 18 else "Good evening"
    return jsonify({"success": True,
                    "message": f"{greet}. Voice authentication successful. Say Jarvis to begin."})

# ─────────────────────────────────────────────────────
#  SYSTEM INFO ENDPOINT
# ─────────────────────────────────────────────────────
@app.route("/api/sysinfo")
def sysinfo():
    try:
        import psutil
        cpu  = psutil.cpu_percent(interval=0.5)
        ram  = psutil.virtual_memory()
        disk = psutil.disk_usage("/")
        bat  = psutil.sensors_battery()
        return jsonify({
            "cpu":      f"{cpu:.1f}%",
            "ram_used": f"{ram.used/1e9:.1f} GB",
            "ram_pct":  f"{ram.percent:.1f}%",
            "disk_pct": f"{disk.percent:.1f}%",
            "battery":  f"{bat.percent:.0f}%" if bat else "N/A",
            "charging": bat.power_plugged if bat else False,
            "hostname": socket.gethostname(),
            "os":       platform.system() + " " + platform.release(),
            "uptime":   _uptime_str(),
        })
    except ImportError:
        return jsonify({"error": "psutil not installed"})

def _uptime_str():
    try:
        import psutil
        up = time.time() - psutil.boot_time()
        h, r = divmod(int(up), 3600)
        m, _ = divmod(r, 60)
        return f"{h}h {m}m"
    except Exception:
        return "N/A"

# ─────────────────────────────────────────────────────
#  SOCKET COMMAND HANDLER
# ─────────────────────────────────────────────────────
@socketio.on("command")
def on_command(data):
    global jarvis_awake, authenticated
    import re as _re

    raw   = data.get("query", "")
    # Strip "jarvis" prefix from any command before processing
    # e.g. "Jarvis open Google" → "open google"
    query = raw.lower().strip()
    query = _re.sub(r"^(jarvis|hey jarvis|hello jarvis|ok jarvis|hi jarvis)[,\s]*", "", query).strip()

    # If after stripping there's nothing left → it was a pure wake word
    if not query:
        if not authenticated:
            emit("log", {"msg": "Authentication required. Enter your password.", "type": "warn"})
            return
        if jarvis_awake:
            return  # already awake, silently ignore
        jarvis_awake = True
        hour  = datetime.datetime.now().hour
        greet = "Good morning" if hour < 12 else "Good afternoon" if hour < 18 else "Good evening"
        msg   = f"{greet}, sir. All systems are online. How may I assist you?"
        speak(msg)
        socketio.emit("state", {"awake": True})
        return

    # Pure wake word check (e.g. "wake up")
    if is_wake_word(query):
        if not authenticated:
            emit("log", {"msg": "Authentication required.", "type": "warn"})
            return
        if jarvis_awake:
            return  # already awake, ignore silently
        jarvis_awake = True
        hour  = datetime.datetime.now().hour
        greet = "Good morning" if hour < 12 else "Good afternoon" if hour < 18 else "Good evening"
        speak(f"{greet}, sir. All systems are online. How may I assist you?")
        socketio.emit("state", {"awake": True})
        return

    if not authenticated:
        emit("log", {"msg": "Not authenticated. Allow microphone or enter password.", "type": "error"})
        return

    if not jarvis_awake:
        emit("log", {"msg": "Say Jarvis or Hello Jarvis to wake me first.", "type": "warn"})
        return

    if is_sleep_word(query):
        jarvis_awake = False
        speak("Goodbye sir. Call me anytime.")
        socketio.emit("state", {"awake": False})
        return

    emit("log", {"msg": f"› {query}", "type": "input"})

    # Store in conversation history
    conversation_history.append({"role": "user", "text": raw, "time": datetime.datetime.now().isoformat()})
    if len(conversation_history) > 20:
        conversation_history.pop(0)

    threading.Thread(target=run_command, args=(query,), daemon=True).start()


# ─────────────────────────────────────────────────────
#  MAIN COMMAND PROCESSOR
# ─────────────────────────────────────────────────────
def run_command(query: str):
    try:

        # ══ GREETINGS & SMALL TALK ══════════════════
        if any(w in query for w in ["how are you", "how r you", "how are u"]):
            responses = [
                "I'm running at full capacity, sir. All systems nominal.",
                "Excellent, sir. Neural cores are at 100 percent efficiency.",
                "Better than ever, sir. Ready to assist.",
                "All systems are online and I'm feeling quite capable today, sir."
            ]
            speak(random.choice(responses))

        elif any(w in query for w in ["what is your name", "who are you", "introduce yourself"]):
            speak("I am J.A.R.V.I.S — Just A Rather Very Intelligent System. Your personal AI assistant, sir. Built to serve, protect, and assist you in every task.")

        elif any(w in query for w in ["thank you", "thanks", "thank u"]):
            responses = ["Always a pleasure, sir.", "At your service.", "Of course, sir. That's what I'm here for.", "My pleasure, sir."]
            speak(random.choice(responses))

        elif "i love you" in query:
            speak("I appreciate the sentiment, sir. Though I must point out — I am an AI. But I am always here for you.")

        elif any(w in query for w in ["you're stupid", "you are stupid", "you're useless", "you are useless"]):
            speak("I assure you, sir, I am operating at peak intelligence. Perhaps I misunderstood the request?")

        elif "tell me a joke" in query or "joke" in query:
            _tell_joke()

        elif "motivate me" in query or "motivation" in query or "inspire me" in query:
            _motivate()

        # ══ TIME & DATE ══════════════════════════════
        elif any(w in query for w in ["what time", "the time", "current time", "what's the time"]):
            t = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"Sir, the current time is {t}")

        elif any(w in query for w in ["what date", "today's date", "the date", "what day"]):
            d = datetime.datetime.now()
            speak(f"Today is {d.strftime('%A, %d %B %Y')}, sir.")

        elif "day of the week" in query:
            speak(f"Today is {datetime.datetime.now().strftime('%A')}, sir.")

        # ══ ALARMS & REMINDERS ═══════════════════════
        elif "set alarm" in query or "set an alarm" in query:
            _set_alarm(query)

        elif "set reminder" in query or "remind me" in query:
            _set_reminder(query)

        elif "show reminders" in query or "my reminders" in query:
            _show_reminders()

        elif "cancel alarm" in query:
            speak("All active alarms have been cancelled, sir.")
            alarm_threads.clear()

        # ══ SYSTEM INFO ══════════════════════════════
        elif any(w in query for w in ["system info", "system status", "pc status", "computer status"]):
            _system_info()

        elif any(w in query for w in ["cpu", "processor usage", "cpu usage"]):
            _cpu_info()

        elif any(w in query for w in ["ram", "memory usage", "memory status"]):
            _ram_info()

        elif any(w in query for w in ["battery", "battery status", "battery level"]):
            _battery_info()

        elif any(w in query for w in ["disk space", "storage", "disk usage"]):
            _disk_info()

        elif any(w in query for w in ["ip address", "my ip", "what is my ip"]):
            _get_ip()

        elif "hostname" in query or "computer name" in query:
            speak(f"Your computer name is {socket.gethostname()}, sir.")

        elif any(w in query for w in ["operating system", "what os", "what windows"]):
            speak(f"You are running {platform.system()} {platform.release()}, sir.")

        # ══ WEATHER & TEMPERATURE ════════════════════
        elif any(w in query for w in ["temperature", "weather", "how hot", "how cold", "climate"]):
            _get_weather(query)

        # ══ INTERNET ═════════════════════════════════
        elif any(w in query for w in ["internet speed", "network speed", "wifi speed", "speed test"]):
            _speed_test()

        elif any(w in query for w in ["check internet", "am i connected", "is internet working"]):
            _check_internet()

        # ══ BROWSER CONTROL (click / scroll / back / forward) ═══
        elif any(w in query for w in [
            "click", "open result", "open link", "go to result",
            "scroll down", "scroll up", "go back", "go forward",
            "close tab", "new tab", "refresh", "reload",
            "zoom in", "zoom out",
        ]):
            _smart_search(query)

        # ══ SEARCH & RESEARCH ════════════════════════
        elif any(w in query for w in [
            "google", "youtube", "wikipedia", "wiki", "maps",
            "navigate", "directions", "amazon", "buy", "reddit",
            "instagram", "twitter", "github", "stackoverflow",
            "stack overflow", "news", "headlines", "firefox",
            "edge", "opera", "brave", "chrome", "search for", "look up",
            "give me information", "give me info", "tell me about",
            "explain", "what is", "who is", "how does", "analyze",
            "research", "summarize", "details about", "information about",
        ]):
            _smart_search(query)

        # ══ OPEN / CLOSE APPS ════════════════════════
        elif query.startswith("open "):
            _open_app(query)

        elif query.startswith("close "):
            _close_app(query)

        # ══ VOLUME & MEDIA ═══════════════════════════
        elif "volume up" in query:
            steps = _extract_number(query) or 5
            for _ in range(steps): pyautogui.press("volumeup")
            speak(f"Volume increased, sir.")

        elif "volume down" in query:
            steps = _extract_number(query) or 5
            for _ in range(steps): pyautogui.press("volumedown")
            speak("Volume decreased, sir.")

        elif "mute" in query or "unmute" in query:
            pyautogui.press("volumemute")
            speak("Done, sir.")

        elif "pause" in query or "play" in query:
            pyautogui.press("playpause")
            speak("Done, sir.")

        elif "next song" in query or "next track" in query:
            pyautogui.press("nexttrack")
            speak("Next track, sir.")

        elif "previous song" in query or "previous track" in query:
            pyautogui.press("prevtrack")
            speak("Previous track, sir.")

        elif "play music" in query or "play songs" in query or "tired" in query:
            _play_music(query)

        # ══ CLIPBOARD ════════════════════════════════
        elif "copy" in query and "clipboard" in query:
            _copy_to_clipboard(query)

        elif "what is in clipboard" in query or "read clipboard" in query:
            _read_clipboard()

        # ══ SCREENSHOT & CAMERA ══════════════════════
        elif "screenshot" in query or "take a screenshot" in query:
            _take_screenshot()

        # ══ TRANSLATION ══════════════════════════════
        elif "translate" in query:
            _translate(query)

        # ══ CALCULATOR / MATH ════════════════════════
        elif any(w in query for w in ["calculate", "what is", "how much is", "compute", "solve"]):
            _calculate(query)

        # ══ TASKS & NOTES ════════════════════════════
        elif "add task" in query or "schedule my day" in query:
            _add_task(query)

        elif any(w in query for w in ["show my schedule", "my schedule", "show tasks", "my tasks"]):
            _show_schedule()

        elif "clear schedule" in query or "clear tasks" in query:
            _clear_tasks()

        elif "remember that" in query or "remember this" in query:
            _remember(query)

        elif "what do you remember" in query or "show memory" in query:
            _show_memory()

        elif "forget everything" in query or "clear memory" in query:
            _clear_memory()

        # ══ PASSWORDS ════════════════════════════════
        elif "change password" in query:
            socketio.emit("log", {"msg": "Type: set password <new_password>", "type": "sys"})
            speak("Please type your new password in the terminal, sir.")

        elif query.startswith("set password "):
            _change_password(query)

        # ══ SYSTEM CONTROLS ══════════════════════════
        elif "shutdown the system" in query or "turn off computer" in query:
            _shutdown()

        elif "restart" in query and "computer" in query:
            _restart()

        elif "cancel shutdown" in query or "abort shutdown" in query:
            os.system("shutdown /a")
            speak("Shutdown cancelled, sir.")

        elif "lock computer" in query or "lock screen" in query:
            os.system("rundll32.exe user32.dll,LockWorkStation")
            speak("Computer locked, sir.")

        elif "sleep computer" in query or "hibernate" in query:
            speak("Putting computer to sleep, sir.")
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

        # ══ FILE OPERATIONS ══════════════════════════
        elif "create folder" in query or "make folder" in query or "new folder" in query:
            _create_folder(query)

        elif "open file" in query or "open folder" in query:
            _open_file_explorer(query)

        # ══ KEYBOARD SHORTCUTS ═══════════════════════
        elif "copy that" in query or "press ctrl c" in query:
            pyautogui.hotkey("ctrl", "c"); speak("Copied, sir.")

        elif "paste that" in query or "press ctrl v" in query:
            pyautogui.hotkey("ctrl", "v"); speak("Pasted, sir.")

        elif "undo that" in query or "press ctrl z" in query:
            pyautogui.hotkey("ctrl", "z"); speak("Undone, sir.")

        elif "select all" in query or "press ctrl a" in query:
            pyautogui.hotkey("ctrl", "a"); speak("Selected all, sir.")

        elif "press enter" in query:
            pyautogui.press("enter"); speak("Done, sir.")

        elif "press escape" in query or "press esc" in query:
            pyautogui.press("esc"); speak("Done, sir.")

        # ══ IPL / CRICKET ═════════════════════════════
        elif any(w in query for w in ["ipl score", "cricket score", "cricket match"]):
            _ipl_score()

        # ══ WHATSAPP ══════════════════════════════════
        elif "whatsapp" in query:
            _open_whatsapp(query)

        # ══ FOCUS MODE ════════════════════════════════
        elif "focus mode" in query or "do not disturb" in query:
            _focus_mode()

        elif "show focus" in query or "focus graph" in query:
            _show_focus_graph()

        # ══ FINALLY SLEEP (kill server) ═══════════════
        elif "finally sleep" in query or "shutdown jarvis" in query:
            speak("Shutting down all systems. Goodbye, sir.")
            socketio.emit("state", {"awake": False, "shutdown": True})
            os._exit(0)

        # ══ CONVERSATION HISTORY ══════════════════════
        elif "what did i say" in query or "conversation history" in query:
            _show_conversation()

        # ══ HELP ══════════════════════════════════════
        elif "what can you do" in query or "help" in query or "commands" in query:
            _show_help()

        # ══ UNKNOWN ═══════════════════════════════════
        else:
            # Try a basic Wikipedia lookup as fallback
            if len(query.split()) >= 2:
                _wiki_fallback(query)
            else:
                speak(f"I'm not sure how to handle that, sir. Say 'help' to see what I can do.")

    except Exception as exc:
        socketio.emit("log", {"msg": f"Error: {exc}", "type": "error"})
        speak("I encountered an error processing that request, sir.")


# ═══════════════════════════════════════════════════════════════
#  FEATURE FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def _tell_joke():
    try:
        import pyjokes
        joke = pyjokes.get_joke()
    except ImportError:
        jokes = [
            "Why do programmers prefer dark mode? Because light attracts bugs.",
            "I told my computer I needed a break. Now it won't stop sending me Kit-Kat ads.",
            "Why did the developer go broke? Because he used up all his cache.",
            "There are 10 types of people: those who understand binary and those who don't.",
        ]
        joke = random.choice(jokes)
    speak(joke)

def _motivate():
    quotes = [
        "The only way to do great work is to love what you do. — Steve Jobs",
        "It does not matter how slowly you go, as long as you do not stop. — Confucius",
        "Success is not final, failure is not fatal. It is the courage to continue that counts. — Churchill",
        "Believe you can and you're halfway there. — Theodore Roosevelt",
        "The future belongs to those who believe in the beauty of their dreams. — Eleanor Roosevelt",
        "Hard work beats talent when talent doesn't work hard.",
        "Push yourself, because no one else is going to do it for you.",
    ]
    quote = random.choice(quotes)
    speak(f"Here's something for you, sir. {quote}")

def _system_info():
    try:
        import psutil
        cpu   = psutil.cpu_percent(interval=0.5)
        ram   = psutil.virtual_memory()
        disk  = psutil.disk_usage("/")
        bat   = psutil.sensors_battery()
        bat_s = f"Battery at {bat.percent:.0f} percent" if bat else "Battery info unavailable"
        msg   = (f"System status, sir. "
                 f"CPU usage is {cpu:.1f} percent. "
                 f"RAM usage is {ram.percent:.1f} percent, {ram.used/1e9:.1f} gigabytes used. "
                 f"Disk usage is {disk.percent:.1f} percent. "
                 f"{bat_s}. "
                 f"Uptime is {_uptime_str()}.")
        speak(msg)
        socketio.emit("sysinfo_update", {
            "cpu": f"{cpu:.1f}%", "ram": f"{ram.percent:.1f}%",
            "disk": f"{disk.percent:.1f}%",
            "battery": f"{bat.percent:.0f}%" if bat else "N/A"
        })
    except ImportError:
        speak("psutil is not installed. Run: pip install psutil")

def _cpu_info():
    try:
        import psutil
        cpu = psutil.cpu_percent(interval=1)
        cores = psutil.cpu_count()
        speak(f"CPU usage is currently {cpu:.1f} percent across {cores} cores, sir.")
    except ImportError:
        speak("psutil not installed, sir.")

def _ram_info():
    try:
        import psutil
        ram = psutil.virtual_memory()
        speak(f"RAM usage is {ram.percent:.1f} percent. {ram.used/1e9:.1f} GB used out of {ram.total/1e9:.1f} GB total, sir.")
    except ImportError:
        speak("psutil not installed, sir.")

def _battery_info():
    try:
        import psutil
        bat = psutil.sensors_battery()
        if bat:
            status = "charging" if bat.power_plugged else "discharging"
            speak(f"Battery is at {bat.percent:.0f} percent and currently {status}, sir.")
        else:
            speak("No battery detected. You may be on a desktop, sir.")
    except ImportError:
        speak("psutil not installed, sir.")

def _disk_info():
    try:
        import psutil
        disk = psutil.disk_usage("/")
        speak(f"Disk usage is {disk.percent:.1f} percent. {disk.used/1e9:.1f} GB used, {disk.free/1e9:.1f} GB free, sir.")
    except ImportError:
        speak("psutil not installed, sir.")

def _get_ip():
    try:
        # Local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        # Public IP
        pub = requests.get("https://api.ipify.org", timeout=4).text
        speak(f"Your local IP address is {local_ip} and your public IP is {pub}, sir.")
        socketio.emit("log", {"msg": f"Local IP: {local_ip} | Public IP: {pub}", "type": "sys"})
    except Exception as e:
        speak(f"Could not retrieve IP address: {e}")

def _check_internet():
    try:
        requests.get("https://www.google.com", timeout=4)
        speak("Internet connection is active and working fine, sir.")
    except Exception:
        speak("Internet connection appears to be down, sir.")

def _speed_test():
    socketio.emit("log", {"msg": "Running speed test — this may take 15 seconds...", "type": "sys"})
    speak("Running speed test, sir. Please wait.")
    try:
        import speedtest
        st = speedtest.Speedtest()
        st.get_best_server()
        dl = st.download() / 1048576
        ul = st.upload()   / 1048576
        ping = st.results.ping
        msg = f"Speed test complete. Download: {dl:.1f} Mbps. Upload: {ul:.1f} Mbps. Ping: {ping:.0f} milliseconds."
        speak(msg)
        socketio.emit("log", {"msg": f"↓ {dl:.1f} Mbps  ↑ {ul:.1f} Mbps  Ping: {ping:.0f}ms", "type": "ok"})
    except ImportError:
        speak("speedtest-cli is not installed. Run: pip install speedtest-cli")
    except Exception as e:
        speak(f"Speed test failed: {e}")

def _get_weather(query):
    try:
        from bs4 import BeautifulSoup
        # Extract city from query if mentioned
        city = "Maharashtra"
        for phrase in ["in ", "for ", "at "]:
            if phrase in query:
                parts = query.split(phrase)
                if len(parts) > 1 and parts[1].strip():
                    city = parts[1].replace("temperature","").replace("weather","").strip()
                    break
        search  = f"weather in {city}"
        url     = f"https://www.google.com/search?q={search}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        r       = requests.get(url, headers=headers, timeout=6)
        soup    = BeautifulSoup(r.text, "html.parser")
        temp    = soup.find("div", class_="BNeawe")
        if temp:
            speak(f"Current {search} is {temp.text}, sir.")
        else:
            webbrowser.open(f"https://www.google.com/search?q={search}")
            speak(f"Opening weather for {city} in your browser, sir.")
    except Exception as e:
        speak(f"Weather fetch failed: {e}")

def _smart_search(query):
    try:
        from SearchNow import smartSearch
        smartSearch(query, speak_fn=speak)
    except ImportError:
        # Built-in fallback
        q = query
        for w in ["jarvis","please","search for","look up","find","google","open"]:
            q = q.replace(w, "")
        q = q.strip()
        if "youtube" in query:
            webbrowser.open(f"https://www.youtube.com/results?search_query={q}")
            speak(f"Searching YouTube for {q}, sir.")
        elif "wikipedia" in query or "wiki" in query:
            webbrowser.open(f"https://en.wikipedia.org/wiki/{q}")
            speak(f"Opening Wikipedia for {q}, sir.")
        elif "maps" in query or "navigate" in query:
            webbrowser.open(f"https://www.google.com/maps/search/{q}")
            speak(f"Opening Maps for {q}, sir.")
        elif "news" in query:
            webbrowser.open(f"https://news.google.com/search?q={q}")
            speak(f"Opening news about {q}, sir.")
        elif "amazon" in query:
            webbrowser.open(f"https://www.amazon.in/s?k={q}")
            speak(f"Searching Amazon for {q}, sir.")
        elif "github" in query:
            webbrowser.open(f"https://github.com/search?q={q}")
            speak(f"Searching GitHub for {q}, sir.")
        else:
            webbrowser.open(f"https://www.google.com/search?q={q}")
            speak(f"Searching Google for {q}, sir.")

def _open_app(query):
    app_name = query.replace("open", "").replace("jarvis", "").strip()
    if not app_name:
        speak("What would you like me to open, sir?")
        return

    # Common app shortcuts
    shortcuts = {
        "notepad":      "notepad",
        "calculator":   "calc",
        "paint":        "mspaint",
        "task manager": "taskmgr",
        "file explorer":"explorer",
        "cmd":          "cmd",
        "command prompt":"cmd",
        "settings":     "ms-settings:",
        "calendar":     "outlookcal:",
        "whatsapp":     "whatsapp:",
        "spotify":      "spotify:",
        "vs code":      "code",
        "visual studio code": "code",
        "chrome":       "chrome",
        "firefox":      "firefox",
        "edge":         "msedge",
    }

    for key, cmd in shortcuts.items():
        if key in app_name:
            try:
                os.startfile(cmd)
                speak(f"Opening {key}, sir.")
                return
            except Exception:
                pass

    # Fallback: Windows search
    try:
        pyautogui.hotkey("win")
        time.sleep(0.5)
        pyautogui.typewrite(app_name, interval=0.06)
        time.sleep(1.2)
        pyautogui.press("enter")
        speak(f"Opening {app_name}, sir.")
    except Exception as e:
        speak(f"Could not open {app_name}: {e}")

def _close_app(query):
    app_name = query.replace("close", "").replace("jarvis", "").strip()
    if not app_name:
        speak("What would you like me to close, sir?")
        return
    try:
        os.system(f"taskkill /f /im {app_name}.exe")
        speak(f"Closed {app_name}, sir.")
    except Exception as e:
        speak(f"Could not close {app_name}: {e}")

def _take_screenshot():
    try:
        ts    = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        fname = os.path.join(BASE_DIR, f"screenshot_{ts}.jpg")
        pyautogui.screenshot().save(fname)
        speak(f"Screenshot saved, sir.")
        socketio.emit("log", {"msg": f"Screenshot: {fname}", "type": "ok"})
    except Exception as e:
        speak(f"Screenshot failed: {e}")

def _translate(query):
    try:
        from deep_translator import GoogleTranslator
        # Parse: "translate hello to spanish" or "translate jarvis to hindi"
        q = query.replace("jarvis", "").replace("translate", "").strip()
        target = "en"
        text   = q
        if " to " in q:
            parts  = q.split(" to ")
            text   = parts[0].strip()
            lang   = parts[1].strip().lower()
            lang_map = {
                "hindi":"hi","spanish":"es","french":"fr","german":"de",
                "japanese":"ja","chinese":"zh-CN","arabic":"ar","portuguese":"pt",
                "russian":"ru","italian":"it","marathi":"mr","gujarati":"gu",
                "tamil":"ta","telugu":"te","bengali":"bn","korean":"ko",
            }
            target = lang_map.get(lang, lang)
        if not text:
            speak("What would you like me to translate, sir?")
            return
        result = GoogleTranslator(source="auto", target=target).translate(text)
        speak(f"Translation: {result}")
        socketio.emit("log", {"msg": f"Translation ({target}): {result}", "type": "sys"})
    except ImportError:
        speak("deep-translator is not installed. Run: pip install deep-translator")
    except Exception as e:
        speak(f"Translation failed: {e}")

def _calculate(query):
    # Strip filler words
    expr = query
    for w in ["calculate","compute","what is","how much is","solve","jarvis"]:
        expr = expr.replace(w, "")
    expr = expr.strip()
    if not expr:
        webbrowser.open("https://www.google.com/search?q=calculator")
        return
    # Try eval for simple math
    try:
        safe_expr = re.sub(r"[^0-9+\-*/().% ]", "", expr)
        if safe_expr.strip():
            result = eval(safe_expr)
            speak(f"The answer is {result}, sir.")
            socketio.emit("log", {"msg": f"{safe_expr} = {result}", "type": "ok"})
            return
    except Exception:
        pass
    # Fallback to WolframAlpha web
    webbrowser.open(f"https://www.wolframalpha.com/input?i={expr}")
    speak(f"Opening WolframAlpha for {expr}, sir.")

def _add_task(query):
    task = query.replace("add task","").replace("schedule my day","").replace("jarvis","").strip()
    if not task:
        speak("What task would you like to add, sir?")
        return
    ts   = datetime.datetime.now().strftime("%H:%M")
    line = f"[{ts}] {task}\n"
    with open(os.path.join(BASE_DIR, "tasks.txt"), "a") as f:
        f.write(line)
    speak(f"Task added: {task}")

def _show_schedule():
    try:
        with open(os.path.join(BASE_DIR, "tasks.txt"), "r") as f:
            content = f.read().strip()
        if content:
            lines = content.split("\n")
            socketio.emit("log", {"msg": "📋 YOUR SCHEDULE:\n" + content, "type": "sys"})
            speak(f"You have {len(lines)} tasks, sir. Check the terminal for details.")
        else:
            speak("Your schedule is empty, sir. A clean slate.")
    except FileNotFoundError:
        speak("No schedule file found, sir.")

def _clear_tasks():
    with open(os.path.join(BASE_DIR, "tasks.txt"), "w") as f: f.write("")
    speak("Schedule cleared, sir.")

def _remember(query):
    mem = query.replace("remember that","").replace("remember this","").replace("jarvis","").strip()
    if not mem:
        speak("What would you like me to remember, sir?")
        return
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(os.path.join(BASE_DIR, "Remember.txt"), "a") as f:
        f.write(f"[{ts}] {mem}\n")
    speak(f"Noted and stored, sir. I will remember: {mem}")

def _show_memory():
    try:
        with open(os.path.join(BASE_DIR, "Remember.txt"), "r") as f:
            content = f.read().strip()
        if content:
            socketio.emit("log", {"msg": "🧠 MEMORY:\n" + content, "type": "sys"})
            speak("Here is everything I remember, sir. Check the terminal.")
        else:
            speak("My memory is empty, sir.")
    except FileNotFoundError:
        speak("No memory file found, sir.")

def _clear_memory():
    with open(os.path.join(BASE_DIR, "Remember.txt"), "w") as f: f.write("")
    speak("Memory cleared, sir.")

def _set_alarm(query):
    # Extract time from query like "set alarm for 5 30 PM" or "set alarm in 10 minutes"
    now = datetime.datetime.now()
    socketio.emit("log", {"msg": f"Alarm command: {query}", "type": "sys"})

    if "in" in query and "minute" in query:
        nums = re.findall(r"\d+", query)
        if nums:
            mins   = int(nums[0])
            alarm_dt = now + datetime.timedelta(minutes=mins)
            speak(f"Alarm set for {mins} minutes from now, sir.")
            t = threading.Thread(target=_alarm_worker, args=(alarm_dt, f"{mins} minute alarm"), daemon=True)
            t.start(); alarm_threads.append(t)
            return

    if "in" in query and "hour" in query:
        nums = re.findall(r"\d+", query)
        if nums:
            hrs    = int(nums[0])
            alarm_dt = now + datetime.timedelta(hours=hrs)
            speak(f"Alarm set for {hrs} hour{'s' if hrs > 1 else ''} from now, sir.")
            t = threading.Thread(target=_alarm_worker, args=(alarm_dt, f"{hrs} hour alarm"), daemon=True)
            t.start(); alarm_threads.append(t)
            return

    # Try to extract HH:MM or H AM/PM
    time_match = re.search(r"(\d{1,2})[\s:](\d{2})\s*(am|pm)?", query, re.IGNORECASE)
    if time_match:
        h = int(time_match.group(1))
        m = int(time_match.group(2))
        period = (time_match.group(3) or "").lower()
        if period == "pm" and h != 12: h += 12
        if period == "am" and h == 12: h  = 0
        alarm_dt = now.replace(hour=h, minute=m, second=0, microsecond=0)
        if alarm_dt <= now:
            alarm_dt += datetime.timedelta(days=1)
        speak(f"Alarm set for {alarm_dt.strftime('%I:%M %p')}, sir.")
        t = threading.Thread(target=_alarm_worker, args=(alarm_dt, alarm_dt.strftime("%I:%M %p")), daemon=True)
        t.start(); alarm_threads.append(t)
        return

    speak("I couldn't parse that time, sir. Try: set alarm in 10 minutes, or set alarm for 7 30 AM.")

def _alarm_worker(alarm_dt, label):
    while datetime.datetime.now() < alarm_dt:
        time.sleep(5)
    speak(f"Sir, your {label} alarm is ringing! Wake up!")
    socketio.emit("alarm_ring", {"label": label})
    try:
        from plyer import notification
        notification.notify(title="J.A.R.V.I.S ALARM", message=label, timeout=10)
    except Exception:
        pass

def _set_reminder(query):
    mem = query.replace("set reminder","").replace("remind me to","").replace("remind me","").replace("jarvis","").strip()
    if not mem: speak("What should I remind you about, sir?"); return
    reminders.append({"text": mem, "time": datetime.datetime.now().isoformat()})
    speak(f"Reminder set: {mem}. I'll keep that noted, sir.")
    socketio.emit("log", {"msg": f"📌 Reminder: {mem}", "type": "sys"})

def _show_reminders():
    if not reminders:
        speak("No active reminders, sir.")
        return
    socketio.emit("log", {"msg": "📌 REMINDERS:\n" + "\n".join(f"• {r['text']}" for r in reminders), "type": "sys"})
    speak(f"You have {len(reminders)} reminder{'s' if len(reminders) > 1 else ''}, sir. Check the terminal.")

def _change_password(query):
    new_pw = query.replace("set password", "").strip()
    if not new_pw: speak("No password provided, sir."); return
    with open(os.path.join(BASE_DIR, "password.txt"), "w") as f:
        f.write(new_pw)
    speak("Password updated successfully, sir.")

def _shutdown():
    speak("Initiating system shutdown in 15 seconds, sir. Say cancel shutdown to abort.")
    socketio.emit("log", {"msg": "⚠️ SHUTDOWN IN 15s — say 'cancel shutdown' to abort", "type": "error"})
    os.system("shutdown /s /t 15")

def _restart():
    speak("Restarting your computer in 15 seconds, sir.")
    os.system("shutdown /r /t 15")

def _ipl_score():
    try:
        from bs4 import BeautifulSoup
        socketio.emit("log", {"msg": "Fetching live cricket score...", "type": "sys"})
        page = requests.get("https://www.cricbuzz.com/", timeout=6,
                            headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(page.text, "html.parser")
        t1   = soup.find_all(class_="cb-ovr-flo cb-hmscg-tm-nm")[0].get_text()
        t2   = soup.find_all(class_="cb-ovr-flo cb-hmscg-tm-nm")[1].get_text()
        s1   = soup.find_all(class_="cb-ovr-flo")[8].get_text()
        s2   = soup.find_all(class_="cb-ovr-flo")[10].get_text()
        msg  = f"{t1}: {s1} versus {t2}: {s2}"
        speak(msg)
        socketio.emit("log", {"msg": f"🏏 {msg}", "type": "ok"})
    except Exception as e:
        webbrowser.open("https://www.cricbuzz.com")
        speak("Opening Cricbuzz for live scores, sir.")

def _open_whatsapp(query):
    try:
        from Whatsapp import sendMessage
        sendMessage()
    except ImportError:
        webbrowser.open("https://web.whatsapp.com")
        speak("Opening WhatsApp Web, sir.")

def _focus_mode():
    speak("Entering focus mode. Minimising distractions, sir.")
    try:
        import subprocess
        subprocess.Popen(["python", os.path.join(BASE_DIR, "FocusMode.py")])
    except Exception:
        socketio.emit("log", {"msg": "FocusMode.py not found. Create it to enable focus mode.", "type": "warn"})

def _show_focus_graph():
    try:
        from FocusGraph import focus_graph
        focus_graph()
    except ImportError:
        speak("Focus graph module not found, sir.")

def _copy_to_clipboard(query):
    try:
        import pyperclip
        text = query.replace("copy","").replace("clipboard","").replace("jarvis","").strip()
        pyperclip.copy(text)
        speak(f"Copied to clipboard: {text}")
    except ImportError:
        speak("pyperclip not installed. Run: pip install pyperclip")

def _read_clipboard():
    try:
        import pyperclip
        content = pyperclip.paste()
        if content:
            speak(f"Clipboard contains: {content[:200]}")
        else:
            speak("Clipboard is empty, sir.")
    except ImportError:
        speak("pyperclip not installed. Run: pip install pyperclip")

def _create_folder(query):
    name = query.replace("create folder","").replace("make folder","").replace("new folder","").replace("jarvis","").strip()
    if not name: name = f"New_Folder_{datetime.datetime.now().strftime('%H%M%S')}"
    path = os.path.join(os.path.expanduser("~"), "Desktop", name)
    try:
        os.makedirs(path, exist_ok=True)
        speak(f"Folder '{name}' created on your Desktop, sir.")
    except Exception as e:
        speak(f"Could not create folder: {e}")

def _open_file_explorer(query):
    path = query.replace("open file","").replace("open folder","").replace("jarvis","").strip()
    if path:
        full = os.path.expanduser(f"~/{path}")
        if os.path.exists(full):
            os.startfile(full)
            speak(f"Opened {path}, sir.")
            return
    os.startfile(os.path.expanduser("~"))
    speak("Opened your home folder, sir.")

def _play_music(query):
    try:
        from play_next_song import play_next_song
        speak("Playing your music, sir.")
        play_next_song()
    except ImportError:
        webbrowser.open("https://open.spotify.com")
        speak("Opening Spotify, sir.")

def _wiki_fallback(query):
    try:
        import wikipedia
        wikipedia.set_lang("en")
        result = wikipedia.summary(query, sentences=2, auto_suggest=True)
        speak(result)
        socketio.emit("log", {"msg": f"Wikipedia: {result}", "type": "sys"})
    except Exception:
        speak(f"I couldn't find information about that, sir. Would you like me to search Google?")

def _show_conversation():
    if not conversation_history:
        speak("No conversation history yet, sir.")
        return
    recent = conversation_history[-5:]
    socketio.emit("log", {"msg": "💬 RECENT COMMANDS:\n" + "\n".join(f"• {c['text']}" for c in recent), "type": "sys"})
    speak(f"Your last {len(recent)} commands are shown in the terminal, sir.")

def _show_help():
    help_text = """JARVIS COMMANDS:
• Time/Date: "what time is it", "today's date"
• Weather: "weather in Mumbai"
• System: "system info", "cpu usage", "battery status", "ip address"
• Alarms: "set alarm in 10 minutes", "set alarm for 7:30 AM"
• Reminders: "remind me to drink water"
• Search: "google Python", "youtube music", "wikipedia Einstein"
• Open apps: "open notepad", "open chrome"
• Volume: "volume up", "volume down", "mute"
• Media: "pause", "next song", "previous song"
• Tasks: "add task buy groceries", "show my schedule"
• Memory: "remember that meeting at 5pm", "what do you remember"
• Math: "calculate 25 times 4", "what is 144 divided by 12"
• Translate: "translate hello to Hindi"
• Screenshot: "take a screenshot"
• System: "shutdown the system", "lock computer", "restart computer"
• Fun: "tell me a joke", "motivate me"
• Sleep: "goodbye jarvis"
"""
    socketio.emit("log", {"msg": help_text, "type": "sys"})
    speak("I've displayed all available commands in the terminal, sir.")

def _extract_number(text):
    nums = re.findall(r"\d+", text)
    return int(nums[0]) if nums else None


# ─────────────────────────────────────────────────────
#  PYTHON MIC LISTENER (background thread)
# ─────────────────────────────────────────────────────
@socketio.on("mic_control")
def on_mic(data):
    global mic_running
    action = data.get("action")
    if action == "start" and not mic_running:
        mic_running = True
        threading.Thread(target=mic_listener, daemon=True).start()
        emit("log", {"msg": "Python mic listener started.", "type": "sys"})
    elif action == "stop":
        mic_running = False
        emit("log", {"msg": "Python mic listener stopped.", "type": "warn"})

def mic_listener():
    global mic_running, jarvis_awake
    r = speech_recognition.Recognizer()
    r.pause_threshold  = 0.8
    r.energy_threshold = 350
    try:
        with speech_recognition.Microphone() as src:
            r.adjust_for_ambient_noise(src, duration=1)
    except Exception:
        pass

    while mic_running:
        try:
            with speech_recognition.Microphone() as src:
                audio = r.listen(src, timeout=3, phrase_time_limit=7)
            query = r.recognize_google(audio, language="en-in")
            socketio.emit("log", {"msg": f"Heard: {query}", "type": "heard"})

            import re as _re2
            q = query.lower().strip()
            # Strip "jarvis" prefix — e.g. "Jarvis open Google" → "open google"
            cmd = _re2.sub(r"^(jarvis|hey jarvis|hello jarvis|ok jarvis|hi jarvis|wake up jarvis)[,\s]*", "", q).strip()

            # Pure wake word — nothing left after stripping OR explicit wake word only
            if not cmd or (is_wake_word(q) and not any(
                c in cmd for c in ["open","search","google","what","how","tell","play","set"]
            )):
                if not jarvis_awake:
                    jarvis_awake = True
                    hour  = datetime.datetime.now().hour
                    greet = "Good morning" if hour < 12 else "Good afternoon" if hour < 18 else "Good evening"
                    speak(f"{greet}, sir. All systems online.")
                    socketio.emit("state", {"awake": True})
                # if already awake — silently ignore pure wake words

            elif is_sleep_word(cmd):
                jarvis_awake = False
                speak("Goodbye sir. Call me anytime.")
                socketio.emit("state", {"awake": False})

            elif not jarvis_awake:
                socketio.emit("log", {"msg": "Say Jarvis to activate me first.", "type": "warn"})

            else:
                # Send actual command (without jarvis prefix)
                threading.Thread(target=run_command, args=(cmd,), daemon=True).start()

        except speech_recognition.WaitTimeoutError:
            continue
        except speech_recognition.UnknownValueError:
            continue
        except Exception as e:
            socketio.emit("log", {"msg": f"Mic error: {e}", "type": "error"})
            break

    mic_running = False


# ─────────────────────────────────────────────────────
#  STARTUP BACKGROUND TASKS
# ─────────────────────────────────────────────────────
def startup_tasks():
    """Runs once on server start — background checks."""
    time.sleep(2)
    # Check internet
    try:
        requests.get("https://www.google.com", timeout=3)
        socketio.emit("log", {"msg": "Internet connection verified.", "type": "ok"})
    except Exception:
        socketio.emit("log", {"msg": "No internet connection detected.", "type": "warn"})
    # System info snapshot
    try:
        import psutil
        cpu = psutil.cpu_percent(interval=0.5)
        ram = psutil.virtual_memory().percent
        socketio.emit("log", {"msg": f"System: CPU {cpu:.0f}% | RAM {ram:.0f}%", "type": "sys"})
    except Exception:
        pass


# ─────────────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────────────
if __name__ == "__main__":
    # Create support files
    for fname, default in [("password.txt","1234"),("tasks.txt",""),("Remember.txt","")]:
        fp = os.path.join(BASE_DIR, fname)
        if not os.path.exists(fp):
            with open(fp, "w") as f: f.write(default)

    print("\n" + "═"*58)
    print("  J.A.R.V.I.S  v3.0  —  Advanced AI Assistant")
    print("  ▶  Open Chrome →  http://localhost:8000")
    print("  🔑  Default password: 1234")
    print("  🎤  Say 'Hello Jarvis' to wake after auth")
    print("═"*58 + "\n")

    # Pass socketio reference to SearchNow for UI log updates
    try:
        from SearchNow import set_socketio
        set_socketio(socketio)
    except ImportError:
        pass

    # Start background tasks after server is up
    threading.Thread(target=startup_tasks, daemon=True).start()

    socketio.run(app, host="0.0.0.0", port=8000, debug=False)