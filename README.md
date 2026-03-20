# 🤖 J.A.R.V.I.S — Python Voice Assistant

A Python-based personal AI voice assistant inspired by Iron Man's **J.A.R.V.I.S.** (Just A Rather Very Intelligent System). Jarvis listens to your voice commands and performs a wide range of tasks — from searching the web to setting alarms, sending WhatsApp messages, and more.

> **v2.0 Update** — Now features a fully linked **Iron Man HUD-style web UI** powered by Flask + Socket.IO. All commands, voice input, and responses are handled in real time between the browser and Python backend.

---

## 🌟 Features

| Feature | Description |
|---|---|
| 🎙️ Voice Recognition | Listens and responds to voice commands via Python `SpeechRecognition` |
| 🖥️ Web UI | Iron Man HUD-style interface linked live to the Python backend |
| 🔍 Web Search | Searches Google, YouTube, Wikipedia instantly |
| 📰 News Reader | Reads out the latest news headlines |
| 🔔 Alarm | Set alarms with custom messages |
| 📖 Dictionary | Look up definitions of words |
| 🌐 Translator | Translate text between languages |
| 💬 WhatsApp Messaging | Send WhatsApp messages via voice |
| 🧮 Calculator | WolframAlpha-powered calculations |
| 🎵 Music Player | Play and skip songs |
| ⌨️ Keyboard Shortcuts | Control your PC with keyboard automation |
| 🎮 Games | Play mini text-based games |
| 🧘 Focus Mode | Enable focus mode and track focus sessions |
| 📊 Focus Graph | Visualize your focus session history |
| 👋 Greeting | Greets you based on time of day |
| 🔐 Password Manager | Change and store passwords securely |
| 📝 Task & Notes | Remember tasks, notes, and schedules |
| 🖥️ App Launcher | Open and close applications by voice |
| 📸 Screenshot | Capture your screen instantly |
| 🌡️ Weather | Fetch live temperature for Maharashtra |
| 🏏 IPL Score | Get live cricket scores from Cricbuzz |

---

## 📁 Project Structure

```
Jarvis/
│
├── jarvismain.py           # ⭐ Main backend — Flask + SocketIO server
├── jarvis_ui.html          # ⭐ Web UI — Iron Man HUD (open in browser)
│
├── GreetMe.py              # Time-based greeting module
├── SearchNow.py            # Google / YouTube / Wikipedia search
├── NewsRead.py             # Fetches and reads news
├── alarm.py                # Alarm functionality
├── Alarmtext.txt           # Stores alarm data
├── Dictapp.py              # Dictionary lookup & app open/close
├── Translator.py           # Language translation
├── Whatsapp.py             # WhatsApp message sender
├── Calculatenumbers.py     # Calculator / WolframAlpha module
├── play_next_song.py       # Music playback control
├── keyboard.py             # Keyboard automation (volume etc.)
├── game.py                 # Mini games
├── FocusMode.py            # Focus / productivity mode
├── FocusGraph.py           # Focus session graph visualization
├── INTRO.py                # Intro animation / startup sequence
├── intents.json            # NLP intents configuration
├── Installer.py            # Auto-installs dependencies
├── requirements.txt        # Python dependencies
│
├── password.txt            # ⚠️ Local password storage (do NOT commit)
├── Remember.txt            # Notes / reminders storage
├── tasks.txt               # Task list storage
├── focus.txt               # Focus session log
└── notification.mp3        # Notification sound
```

---

## ⚙️ Installation

### Prerequisites

- Python 3.8 or higher
- A working microphone
- Internet connection
- Google Chrome (recommended for the UI)

### 1. Clone the Repository

```bash
git clone https://github.com/vinitsonawane45/Jarvis-.git
cd Jarvis-
```

### 2. Install Dependencies

Run the auto-installer:

```bash
python Installer.py
```

Or install manually:

```bash
pip install -r requirements.txt
```

### 3. Install New UI Dependencies

The web UI requires two additional packages:

```bash
pip install flask flask-socketio
```

If `pyaudio` fails to install:

```bash
pip install pipwin
pipwin install pyaudio
```

---

## 🚀 How to Run (v2.0 with Web UI)

### Step 1 — Start the backend server

```bash
python jarvismain.py
```

You will see:

```
=======================================================
  J.A.R.V.I.S  — Server starting...
  ▶  Open in browser:  http://localhost:5000
  Default password:    1234
=======================================================
```

### Step 2 — Open the UI

Open **Google Chrome** and navigate to:

```
http://localhost:5000
```

### Step 3 — Authenticate

Enter the password (`1234` by default) in the login screen.  
To change it, say or type: `change password`

### Step 4 — Wake Jarvis

Say or type:

```
wake up
```

Jarvis will greet you and become fully active. All commands now work via voice (MIC button) or by typing in the terminal panel.

> **Keep the Command Prompt window open** while using Jarvis — closing it stops the server.  
> To stop, press `Ctrl + C` in the terminal.

---

## 🔗 How the UI and Python Are Linked

```
[jarvis_ui.html]  ←──── Socket.IO (WebSocket) ────→  [jarvismain.py]
   (Browser)                                           (Flask Server)
```

| UI Action | Python Backend Action |
|---|---|
| Enter password → Authenticate | Calls `/api/auth` → checks `password.txt` |
| Type command → Send | `socket.emit("command")` → `run_command()` executes it |
| Click MIC button | Starts Python `SpeechRecognition` mic listener |
| Jarvis speaks | `pyttsx3` speaks AND sends text to the UI terminal |
| Wake / Sleep state | Python emits `state` event → UI badge updates live |

---

## 🗣️ Voice Commands

```
"wake up"                        → Activate Jarvis
"go to sleep"                    → Suspend session
"the time"                       → Current time
"the date"                       → Today's date
"internet speed"                 → Run a speed test
"weather" / "temperature"        → Maharashtra live temperature
"ipl score"                      → Live cricket score
"open Chrome"                    → Launch an application
"google Python tutorials"        → Google search
"youtube lo-fi music"            → YouTube search
"wikipedia Albert Einstein"      → Wikipedia lookup
"screenshot"                     → Capture your screen
"add task buy groceries"         → Add a task
"show my schedule"               → View all tasks
"remember that meeting at 5pm"   → Store a note
"what do you remember"           → Read stored notes
"calculate 25 times 4"           → WolframAlpha calculation
"translate hello to Spanish"     → Translate text
"tired"                          → Play music
"news"                           → Latest headlines
"volume up" / "volume down"      → Volume control
"pause" / "play" / "mute"        → Media controls
"focus mode"                     → Enable focus mode
"open whatsapp"                  → Open WhatsApp Web
"shutdown the system"            → Shut down the PC
"change password"                → Change Jarvis password
"finally sleep"                  → Shut down Jarvis server
```

---

## 🐛 Bug Fixes in v2.0

- **Wake up not working** — `pyttsx3` engine was initialized inside the wrong indentation block (inside the `elif` for wrong password). It only initialized when the password was *incorrect*, so Jarvis crashed silently on correct login before ever reaching the `"wake up"` listener. Fixed by moving engine initialization to the top of the file.
- **Mic context error** — The microphone background thread was calling `on_command()` directly, which requires a Flask request context. Fixed by calling `run_command()` directly from the mic thread instead.
- **404 on UI load** — `send_from_directory(".")` used a relative path that broke when Python was run from a different directory. Fixed using `BASE_DIR = os.path.dirname(os.path.abspath(__file__))` so the path is always resolved relative to `jarvismain.py` itself.
- **File path errors** — `password.txt`, `tasks.txt`, `Remember.txt` now all use absolute `BASE_DIR` paths so they are always found regardless of working directory.

---

## 📦 Dependencies

```
flask
flask-socketio
SpeechRecognition
pyttsx3
pyaudio
requests
pyautogui
plyer
pygame
speedtest-cli
beautifulsoup4
pywhatkit
wikipedia
newsapi-python
deep-translator
PyDictionary
matplotlib
playsound
```

---

## 🔧 Configuration

| File | Purpose |
|---|---|
| `password.txt` | Jarvis login password (default: `1234`) |
| `Remember.txt` | Stores notes and reminders |
| `tasks.txt` | Stores your daily schedule |
| `focus.txt` | Logs focus session history |
| `Alarmtext.txt` | Stores alarm time data |
| `intents.json` | NLP command intent definitions |

---

## 🛡️ Security Notes

> ⚠️ `password.txt` stores your password in **plain text** locally. Do **not** share or commit this file to a public repository.

Add this to your `.gitignore`:

```gitignore
password.txt
Remember.txt
tasks.txt
focus.txt
__pycache__/
*.pyc
```

---

## ❓ Troubleshooting

| Problem | Fix |
|---|---|
| `ModuleNotFoundError: flask` | `pip install flask flask-socketio` |
| `pyaudio` install fails | `pip install pipwin` then `pipwin install pyaudio` |
| Browser shows 404 | Make sure `jarvis_ui.html` is in the **same folder** as `jarvismain.py` |
| Browser shows "Cannot connect" | Make sure `python jarvismain.py` is still running in CMD |
| Mic not working | Run Command Prompt as **Administrator** |
| "Wake up" not responding | Check microphone permissions in Windows Settings |
| `Working outside of request context` | Make sure you are using the latest `jarvismain.py` (v2.0 fix applied) |

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## 👨‍💻 Author

**Vinit Sonawane**
- GitHub: [@vinitsonawane45](https://github.com/vinitsonawane45)

---

## 📜 License

This project is open-source. Feel free to use, modify, and distribute it with attribution.

---

<p align="center">Made with ❤️ in Python &nbsp;·&nbsp; v2.0 — Now with Web UI</p>