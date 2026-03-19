# 🤖 Jarvis - Python Voice Assistant

A Python-based personal AI voice assistant inspired by Iron Man's J.A.R.V.I.S. (Just A Rather Very Intelligent System). Jarvis can listen to your voice commands and perform a wide range of tasks — from searching the web to setting alarms, sending WhatsApp messages, and more.

---

## 🌟 Features

| Feature | Description |
|---|---|
| 🎙️ Voice Recognition | Listens and responds to voice commands |
| 🔍 Web Search | Searches Google/Wikipedia instantly |
| 📰 News Reader | Reads out the latest news headlines |
| 🔔 Alarm | Set alarms with custom messages |
| 📖 Dictionary | Look up definitions of words |
| 🌐 Translator | Translate text between languages |
| 💬 WhatsApp Messaging | Send WhatsApp messages via voice |
| 🧮 Calculator | Perform arithmetic calculations |
| 🎵 Music Player | Play and skip songs |
| ⌨️ Keyboard Shortcuts | Control your PC with keyboard automation |
| 🎮 Games | Play mini text-based games |
| 🧘 Focus Mode | Enable focus mode and track focus sessions |
| 📊 Focus Graph | Visualize your focus session history |
| 👋 Greeting | Greets you based on time of day |
| 🔐 Password Manager | Store and retrieve passwords |
| 📝 Task & Notes | Remember tasks and notes |
| 🖥️ App Launcher | Open and close applications |

---

## 📁 Project Structure

```
Jarvis/
│
├── Jarvis_main.py          # Main entry point — orchestrates all modules
├── INTRO.py                # Intro animation / startup sequence
├── GreetMe.py              # Time-based greeting module
├── SearchNow.py            # Web/Wikipedia search
├── NewsRead.py             # Fetches and reads news
├── alarm.py                # Alarm functionality
├── Alarmtext.txt           # Stores alarm data
├── Dictapp.py              # Dictionary lookup
├── Translator.py           # Language translation
├── Whatsapp.py             # WhatsApp message sender
├── Calculatenumbers.py     # Calculator module
├── play_next_song.py       # Music playback control
├── keyboard.py             # Keyboard automation
├── game.py                 # Mini games
├── FocusMode.py            # Focus/productivity mode
├── FocusGraph.py           # Focus session graph visualization
├── open and closing.py     # App open/close handler
├── app.py                  # Application utilities
├── intents.json            # NLP intents configuration
├── Installer.py            # Auto-installs dependencies
├── requirements.txt        # Python dependencies
├── password.txt            # Local password storage
├── Remember.txt            # Notes/reminders storage
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

### 1. Clone the Repository

```bash
git clone https://github.com/vinitsonawane45/Jarvis-.git
cd Jarvis-
```

### 2. Install Dependencies

Run the auto-installer script:

```bash
python Installer.py
```

Or install manually:

```bash
pip install -r requirements.txt
```

### 3. Run Jarvis

```bash
python Jarvis_main.py
```

---

## 📦 Dependencies

Key libraries used in this project:

- `SpeechRecognition` — Voice input processing
- `pyttsx3` — Text-to-speech engine
- `pywhatkit` — WhatsApp messaging & YouTube
- `wikipedia` — Wikipedia search
- `newsapi-python` — News fetching
- `deep-translator` — Language translation
- `PyDictionary` — Word definitions
- `pyautogui` — Keyboard/mouse automation
- `matplotlib` — Focus session graph plotting
- `playsound` — Audio notification playback

---

## 🚀 Usage

Once running, Jarvis will greet you and wait for a wake command. Speak clearly into your microphone. Example commands:

```
"Jarvis, search Python programming"
"Jarvis, what's the news today?"
"Jarvis, set an alarm for 7 AM"
"Jarvis, translate hello to Spanish"
"Jarvis, send a WhatsApp message to Mom"
"Jarvis, what is the meaning of ephemeral"
"Jarvis, calculate 25 times 4"
"Jarvis, play music"
"Jarvis, enable focus mode"
"Jarvis, open Chrome"
"Jarvis, remember: dentist appointment on Friday"
```

---

## 🔧 Configuration

- **Alarm messages** are stored in `Alarmtext.txt`
- **Tasks and notes** are stored in `Remember.txt` and `tasks.txt`
- **Focus sessions** are logged in `focus.txt` and visualized via `FocusGraph.py`
- **Intents** for NLP command matching are defined in `intents.json`

---

## 🛡️ Notes & Warnings

> ⚠️ `password.txt` stores passwords in plain text locally. Do **not** share this file or commit it to a public repository. Consider adding it to `.gitignore`.

```gitignore
password.txt
Remember.txt
tasks.txt
focus.txt
__pycache__/
```

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

<p align="center">Made with ❤️ in Python</p>