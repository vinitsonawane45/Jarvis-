# import pyttsx3
# import speech_recognition 
# import requests
# import datetime
# import os
# import pyautogui
# import random
# from plyer import notification
# from pygame import mixer
# import webbrowser
# import speedtest
# import sys
# import tkinter as tk
# from tkinter import scrolledtext





# for i in range(3):
#     a = input("Enter Password to open Jarvis :- ")
#     pw_file = open("password.txt","r")
#     pw = pw_file.read()
#     pw_file.close()
#     if (a==pw):
#         print("WELCOME SIR ! PLZ SPEAK [WAKE UP] TO LOAD ME UP")
#         break
#     elif (i==2 and a!=pw):
#         exit()

#     elif (a!=pw):
#         print("Try Again")





#     engine = pyttsx3.init("sapi5")
#     voices = engine.getProperty("voices")
#     engine.setProperty("voice", voices[0].id)
#     rate = engine.setProperty("rate",170)

# def speak(audio):
#     engine.say(audio)
#     engine.runAndWait()

# def takeCommand():
#     r = speech_recognition.Recognizer()
#     with speech_recognition.Microphone() as source:
#         print("Listening.....")
#         r.pause_threshold = 1
#         r.energy_threshold = 400
#         audio = r.listen(source,0,4)

#     try:
#         print("Understanding..")
#         query  = r.recognize_google(audio,language='en-in')
#         print(f"You Said: {query}\n")
#     except Exception as e:
#         print("Say that again")
#         return "None"
#     return query



# # def alarm(query):
# #     timehere = open("Alarmtext.txt","a")
# #     timehere.write(query)
# #     timehere.close()
# #     os.startfile("alarm.py")


# if __name__ == "__main__":
#     while True:
#         query = takeCommand().lower()
#         if "wake up" in query:
#             from GreetMe import greetMe
#             greetMe()

#             while True:
#                 query = takeCommand().lower()
#                 if "go to sleep" in query:
#                     speak("Ok sir , You can me call anytime")
#                     break 

#                  ########### JAERVIS THE TARILOGY 2.0################
#                 elif "change password" in query:
#                     speak("What's the new password")
#                     new_pw = input("Enter the new password\n")
#                     new_password = open("password.txt","w")
#                     new_password.write(new_pw)
#                     new_password.close()
#                     speak("Done sir")
#                     speak(f"Your new password is{new_pw}")

#                 elif "schedule my day" in query:
#                     tasks = [] #Empty list 
#                     speak("Do you want to clear old tasks (Plz speak YES or NO)")
#                     query = takeCommand().lower()
#                     if "yes" in query:
#                             file = open("tasks.txt","w")
#                             file.write(f"")
#                             file.close()
#                             no_tasks = int(input("Enter the no. of tasks :- "))
#                             i = 0
#                             for i in range(no_tasks):
#                                 tasks.append(input("Enter the task :- "))
#                                 file = open("tasks.txt","a")
#                                 file.write(f"{i}. {tasks[i]}\n")
#                                 file.close()
#                     elif "no" in query:
#                                 i = 0
#                                 no_tasks = int(input("Enter the no. of tasks :- "))
#                     for i in range(no_tasks):
#                         tasks.append(input("Enter the task :- "))
#                         file = open("tasks.txt","a")
#                         file.write(f"{i}. {tasks[i]}\n")
#                         file.close()

#                 elif "show my schedule" in query:
#                         file = open("tasks.txt","r")
#                         content = file.read()
#                         file.close()
#                         mixer.init()
#                         mixer.music.load("notification.mp3")
#                         mixer.music.play()
#                         notification.notify(
#                         title = "My schedule :-",
#                         message = content,
#                         timeout = 15
#                             )

#                 elif "open" in query:   #EASY METHOD
#                     query = query.replace("open","")
#                     query = query.replace("jarvis","")
#                     pyautogui.press("super")
#                     pyautogui.typewrite(query)
#                     pyautogui.sleep(2)
#                     pyautogui.press("enter") 
                    



               


#                 elif "internet speed" in query:
#                     wifi  = speedtest.Speedtest()
#                     upload_net = wifi.upload()/1048576         #Megabyte = 1024*1024 Bytes
#                     download_net = wifi.download()/1048576
#                     print("Wifi Upload Speed is", upload_net)
#                     print("Wifi download speed is ",download_net)
#                     speak(f"Wifi download speed is {download_net}")
#                     speak(f"Wifi Upload speed is {upload_net}")

#                 elif "Ipl Score" in query:
#                     from plyer import notification  #pip install plyer
#                     import requests #pip install requests
#                     from bs4 import BeautifulSoup #pip install bs4
#                     url = "https://www.cricbuzz.com/"
#                     page = requests.get(url)
#                     soup = BeautifulSoup(page.text,"html.parser")
#                     team1 = soup.find_all(class_ = "cb-ovr-flo cb-hmscg-tm-nm")[0].get_text()
#                     team2 = soup.find_all(class_ = "cb-ovr-flo cb-hmscg-tm-nm")[1].get_text()
#                     team1_score = soup.find_all(class_ = "cb-ovr-flo")[8].get_text()
#                     team2_score = soup.find_all(class_ = "cb-ovr-flo")[10].get_text()

#                     a = print(f"{team1} : {team1_score}")
#                     b = print(f"{team2} : {team2_score}")

#                     notification.notify(
#                         title = "IPL SCORE :- ",
#                         message = f"{team1} : {team1_score}\n {team2} : {team2_score}",
#                         timeout = 15
#                     )
#                 elif "play a game" in query:
#                     from game import game_play
#                     game_play()

#                 elif "screenshot" in query:
#                      import pyautogui #pip install pyautogui
#                      im = pyautogui.screenshot()
#                      im.save("ss.jpg")
#                 elif "click my photo" in query:
#                     pyautogui.press("super")
#                     pyautogui.typewrite("camera")
#                     pyautogui.press("enter")
#                     pyautogui.sleep(2)
#                     speak("SMILE")
#                     pyautogui.press("enter")
                
#                 elif "focus mode" in query:
#                     a = int(input("Are you sure that you want to enter focus mode :- [1 for YES / 2 for NO "))
#                     if (a==1):
#                         speak("Entering the focus mode....")
#                         os.startfile("D:\\Coding\\Youtube\\Jarvis\\FocusMode.py")
#                         exit()
#                     else:
#                         pass
                
#                 elif "show my focus" in query:
#                     from FocusGraph import focus_graph
#                     focus_graph()

#                 elif "translate" in query:
#                     from Translator import translategl
#                     query = query.replace("jarvis","")
#                     query = query.replace("translate","")
#                     translategl(query)

                


                 

#                  ###################################################
    


            
#                 # elif "tired" in query:
#                 #     speak("Playing your favourite songs, sir")
#                 #     a = (1,2,3) # You can choose any number of songs (I have only choosen 3)
#                 #     b = random.choice(a)
#                 #     if b==1:
#                 #         webbrowser.open("https://open.spotify.com/playlist/6qy2c4so678KpMN7tAzhfgkm") 

#                 elif "tired" in query:
#                     speak("Playing your favourite songs, sir")
#                     from play_next_song import play_next_song
                    
#                 elif "pause" in query:
#                     pyautogui.press("k")
#                     speak("video paused")
#                 elif "play" in query:
#                     pyautogui.press("k")
#                     speak("video played")
#                 elif "mute" in query:
#                     pyautogui.press("m")
#                     speak("video muted")
#                 elif "next video" in query:
#                     from play_next_song import play_next_song

#                 elif "volume up" in query:
#                     from keyboard import volumeup
#                     speak("Turning volume up,sir")
#                     volumeup()
#                 elif "volume down" in query:
#                     from keyboard import volumedown
#                     speak("Turning volume down, sir")
#                     volumedown()


#                 elif "open" in query:
#                     from Dictapp import openappweb
#                     openappweb(query)

#                 elif "close" in query:
#                     from Dictapp import closeappweb
#                     closeappweb(query)

        
            

#                 elif "google" in query:
#                     from SearchNow import searchGoogle
#                     searchGoogle(query)

#                 elif "youtube" in query:
#                     from SearchNow import searchYoutube
#                     searchYoutube(query)

#                 elif "wikipedia" in query:
#                     from SearchNow import searchWikipedia
#                     searchWikipedia(query)

#                 elif "news" in query:
#                     from NewsRead import latestnews
#                     latestnews()

#                 elif "calculate" in query:
#                     from Calculatenumbers import WolfRamAlpha
#                     from Calculatenumbers import Calc
#                     query = query.replace("calculate","")
#                     query = query.replace("jarvis","")
#                     Calc(query)

#                 elif "Open whatsapp" in query:
#                     from Whatsapp import sendMessage
#                     sendMessage()

#                 elif "shutdown the system" in query:
#                     speak("Are You sure you want to shutdown")
#                     shutdown = input("Do you wish to shutdown your computer? (yes/no)")
#                     if shutdown == "yes":
#                         os.system("shutdown /s /t 1")

#                     elif shutdown == "no":
#                         break

                

#                 elif "temperature" in query:
#                     search = "temperature in Maharashtra"
#                     url = f"https://www.google.com/search?q={search}"
#                     r  = requests.get(url)
#                     data = BeautifulSoup(r.text,"html.parser")
#                     temp = data.find("div", class_ = "BNeawe").text
#                     speak(f"current{search} is {temp}")

#                 elif "weather" in query:
#                     search = "temperature in Maharashtra"
#                     url = f"https://www.google.com/search?q={search}"
#                     r  = requests.get(url)
#                     data = BeautifulSoup(r.text,"html.parser")
#                     temp = data.find("div", class_ = "BNeawe").text
#                     speak(f"current{search} is {temp}")

#                 elif "set an alarm" in query:
#                     print("input time example:- 10 and 10 and 10")
#                     speak("Set the time")
#                     a = input("Please tell the time :- ")
#                     alarm(a)
#                     speak("Done,sir")


#                 elif "the time" in query:
#                     strTime = datetime.datetime.now().strftime("%H:%M")    
#                     speak(f"Sir, the time is {strTime}")

#                 elif "finally sleep" in query:
#                     speak("Going to sleep,sir")
#                     exit()
                
#                 elif "remember that" in query:
#                     rememberMessage = query.replace("remember that","")
#                     rememberMessage = query.replace("jarvis","")
#                     speak("You told me to remember that"+rememberMessage)
#                     remember = open("Remember.txt","a")
#                     remember.write(rememberMessage)
#                     remember.close()
#                 elif "what do you remember" in query:
#                     remember = open("Remember.txt","r")
#                     speak("You told me to remember that" + remember.read())

    
# # =================================================================================================



"""
J.A.R.V.I.S - Backend Server (Flask + SocketIO)
================================================
HOW TO RUN:
  1. Install dependencies:
       pip install flask flask-socketio pyttsx3 speechrecognition pyaudio
                   requests pyautogui plyer pygame speedtest-cli beautifulsoup4
  2. Put jarvismain.py and jarvis_ui.html in the SAME folder.
  3. Run:  python jarvismain.py
  4. Open browser:  http://localhost:5000
"""

import pyttsx3
import speech_recognition
import requests
import datetime
import os
import pyautogui
import threading
import webbrowser
import sys

from flask import Flask, send_from_directory, request, jsonify, send_file
from flask_socketio import SocketIO, emit

# ──────────────────────────────────────────────────────────────
#  Base directory — always the folder where jarvismain.py lives
# ──────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ──────────────────────────────────────────────────────────────
#  TTS Engine
# ──────────────────────────────────────────────────────────────
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 170)
speak_lock = threading.Lock()

def speak(text: str):
    """Speak aloud + forward text to the UI terminal."""
    with speak_lock:
        engine.say(text)
        engine.runAndWait()
    socketio.emit("log", {"msg": text, "type": "speak"})

# ──────────────────────────────────────────────────────────────
#  Flask app
# ──────────────────────────────────────────────────────────────
app = Flask(__name__)
app.config["SECRET_KEY"] = "jarvis-ultra-secret"
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

# ── State ──────────────────────────────────────────────────────
authenticated = False
jarvis_awake   = False
mic_running    = False

# ──────────────────────────────────────────────────────────────
#  Serve the HTML UI from the same directory
# ──────────────────────────────────────────────────────────────
@app.route("/")
def index():
    ui_path = os.path.join(BASE_DIR, "jarvis_ui.html")
    if not os.path.exists(ui_path):
        return f"<h2>jarvis_ui.html not found at {ui_path}</h2>", 404
    return send_file(ui_path)

# ──────────────────────────────────────────────────────────────
#  REST: Password check
# ──────────────────────────────────────────────────────────────
@app.route("/api/auth", methods=["POST"])
def auth():
    global authenticated
    data     = request.get_json(force=True)
    entered  = data.get("password", "").strip()

    # Create default password file if it doesn't exist
    if not os.path.exists(os.path.join(BASE_DIR, "password.txt")):
        with open(os.path.join(BASE_DIR, "password.txt"), "w") as f:
            f.write("1234")

    with open(os.path.join(BASE_DIR, "password.txt"), "r") as f:
        stored = f.read().strip()

    if entered == stored:
        authenticated = True
        return jsonify({"success": True,  "message": "Access granted. Speak WAKE UP to begin."})
    return jsonify({"success": False, "message": "Incorrect password. Try again."})

# ──────────────────────────────────────────────────────────────
#  SocketIO: Command handler  (UI → Python)
#  UI emits:   socket.emit("command", { query: "wake up" })
#  We emit back: socket.emit("log", { msg: "...", type: "ok" })
#               socket.emit("state", { awake: true })
# ──────────────────────────────────────────────────────────────
@socketio.on("command")
def on_command(data):
    global jarvis_awake

    if not authenticated:
        emit("log", {"msg": "Not authenticated. Enter your password first.", "type": "error"})
        return

    raw   = data.get("query", "")
    query = raw.lower().strip()
    emit("log", {"msg": f"› {raw}", "type": "input"})

    # WAKE UP
    if "wake up" in query:
        jarvis_awake = True
        hour = datetime.datetime.now().hour
        greet = ("Good morning" if hour < 12 else
                 "Good afternoon" if hour < 18 else "Good evening")
        msg = f"{greet}, sir. All systems are online. How may I assist you?"
        speak(msg)
        socketio.emit("state", {"awake": True})
        return

    # Gate — must wake first
    if not jarvis_awake:
        emit("log", {"msg": 'Jarvis is in standby. Say "wake up" to activate.', "type": "warn"})
        return

    # GO TO SLEEP
    if "go to sleep" in query:
        jarvis_awake = False
        speak("Ok sir, call me anytime.")
        socketio.emit("state", {"awake": False})
        return

    # Run all other commands in a background thread
    threading.Thread(target=run_command, args=(query,), daemon=True).start()


def run_command(query: str):
    """Execute a Jarvis command in a worker thread."""
    try:

        # ── TIME ────────────────────────────────────
        if "the time" in query:
            t = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"Sir, the time is {t}")

        # ── DATE ────────────────────────────────────
        elif "the date" in query or "today's date" in query:
            d = datetime.datetime.now().strftime("%A, %d %B %Y")
            speak(f"Today is {d}, sir.")

        # ── CHANGE PASSWORD ──────────────────────────
        elif "change password" in query:
            socketio.emit("log", {
                "msg": "Type your new password as:  set password <new_password>",
                "type": "sys"
            })

        elif query.startswith("set password "):
            new_pw = query.replace("set password ", "").strip()
            with open(os.path.join(BASE_DIR, "password.txt"), "w") as f:
                f.write(new_pw)
            speak("Password changed successfully, sir.")

        # ── INTERNET SPEED ───────────────────────────
        elif "internet speed" in query:
            socketio.emit("log", {"msg": "Running speed test, please wait...", "type": "sys"})
            try:
                import speedtest
                wifi = speedtest.Speedtest()
                dl = wifi.download() / 1048576
                ul = wifi.upload()   / 1048576
                msg = f"Download: {dl:.2f} Mbps  |  Upload: {ul:.2f} Mbps"
                speak(msg)
            except Exception as e:
                speak(f"Speed test failed: {e}")

        # ── WEATHER / TEMPERATURE ────────────────────
        elif "temperature" in query or "weather" in query:
            try:
                from bs4 import BeautifulSoup
                search  = "temperature in Maharashtra"
                url     = f"https://www.google.com/search?q={search}"
                headers = {"User-Agent": "Mozilla/5.0"}
                r       = requests.get(url, headers=headers, timeout=6)
                soup    = BeautifulSoup(r.text, "html.parser")
                temp    = soup.find("div", class_="BNeawe")
                speak(f"Current temperature in Maharashtra is {temp.text}" if temp
                      else "Sorry sir, I couldn't fetch the temperature right now.")
            except Exception as e:
                speak(f"Weather fetch failed: {e}")

        # ── IPL SCORE ────────────────────────────────
        elif "ipl score" in query:
            try:
                from bs4 import BeautifulSoup
                socketio.emit("log", {"msg": "Fetching live IPL score...", "type": "sys"})
                page = requests.get("https://www.cricbuzz.com/", timeout=6)
                soup = BeautifulSoup(page.text, "html.parser")
                t1   = soup.find_all(class_="cb-ovr-flo cb-hmscg-tm-nm")[0].get_text()
                t2   = soup.find_all(class_="cb-ovr-flo cb-hmscg-tm-nm")[1].get_text()
                s1   = soup.find_all(class_="cb-ovr-flo")[8].get_text()
                s2   = soup.find_all(class_="cb-ovr-flo")[10].get_text()
                speak(f"{t1}: {s1}  vs  {t2}: {s2}")
            except Exception as e:
                speak(f"Could not fetch IPL score: {e}")

        # ── SCREENSHOT ───────────────────────────────
        elif "screenshot" in query:
            fname = f"screenshot_{datetime.datetime.now().strftime('%H%M%S')}.jpg"
            pyautogui.screenshot().save(fname)
            speak(f"Screenshot saved as {fname}, sir.")

        # ── OPEN APP ─────────────────────────────────
        elif query.startswith("open"):
            app_name = query.replace("open", "").replace("jarvis", "").strip()
            if app_name:
                pyautogui.press("super")
                pyautogui.typewrite(app_name, interval=0.05)
                pyautogui.sleep(2)
                pyautogui.press("enter")
                speak(f"Opening {app_name}, sir.")
            else:
                speak("What should I open, sir?")

        # ── GOOGLE ───────────────────────────────────
        elif "google" in query:
            q = query.replace("google", "").replace("jarvis", "").strip()
            webbrowser.open(f"https://www.google.com/search?q={q}")
            speak(f"Searching Google for {q}")

        # ── YOUTUBE ──────────────────────────────────
        elif "youtube" in query:
            q = query.replace("youtube", "").replace("jarvis", "").strip()
            webbrowser.open(f"https://www.youtube.com/results?search_query={q}")
            speak(f"Searching YouTube for {q}")

        # ── WIKIPEDIA ────────────────────────────────
        elif "wikipedia" in query:
            q = query.replace("wikipedia", "").replace("jarvis", "").strip()
            webbrowser.open(f"https://en.wikipedia.org/wiki/{q}")
            speak(f"Opening Wikipedia page for {q}")

        # ── ADD TASK ─────────────────────────────────
        elif "add task" in query or "schedule my day" in query:
            task = query.replace("add task", "").replace("schedule my day", "").replace("jarvis", "").strip()
            if task:
                ts = datetime.datetime.now().strftime("%H:%M")
                with open(os.path.join(BASE_DIR, "tasks.txt"), "a") as f:
                    f.write(f"[{ts}] {task}\n")
                speak(f"Task added: {task}")
            else:
                socketio.emit("log", {"msg": "To add a task type: add task <your task>", "type": "sys"})

        # ── SHOW SCHEDULE ────────────────────────────
        elif "show my schedule" in query or "my schedule" in query:
            try:
                with open(os.path.join(BASE_DIR, "tasks.txt"), "r") as f:
                    content = f.read().strip()
                if content:
                    socketio.emit("log", {"msg": "📋 YOUR SCHEDULE:\n" + content, "type": "sys"})
                    speak("Here is your schedule, sir.")
                else:
                    speak("Your schedule is empty, sir.")
            except FileNotFoundError:
                speak("No schedule found, sir.")

        # ── REMEMBER ─────────────────────────────────
        elif "remember that" in query:
            mem = query.replace("remember that", "").replace("jarvis", "").strip()
            with open(os.path.join(BASE_DIR, "Remember.txt"), "a") as f:
                f.write(mem + "\n")
            speak(f"Noted, sir. I will remember: {mem}")

        # ── WHAT DO YOU REMEMBER ─────────────────────
        elif "what do you remember" in query:
            try:
                with open(os.path.join(BASE_DIR, "Remember.txt"), "r") as f:
                    content = f.read().strip()
                if content:
                    socketio.emit("log", {"msg": "🧠 MEMORY:\n" + content, "type": "sys"})
                    speak("Here is what I remember, sir.")
                else:
                    speak("My memory is empty, sir.")
            except FileNotFoundError:
                speak("No memory found, sir.")

        # ── NEWS ─────────────────────────────────────
        elif "news" in query:
            try:
                from NewsRead import latestnews
                latestnews()
            except ImportError:
                webbrowser.open("https://news.google.com")
                speak("Opening Google News, sir.")

        # ── CALCULATE ────────────────────────────────
        elif "calculate" in query:
            q = query.replace("calculate", "").replace("jarvis", "").strip()
            webbrowser.open(f"https://www.wolframalpha.com/input?i={q}")
            speak(f"Searching WolframAlpha for {q}")

        # ── WHATSAPP ─────────────────────────────────
        elif "whatsapp" in query:
            try:
                from Whatsapp import sendMessage
                sendMessage()
            except ImportError:
                webbrowser.open("https://web.whatsapp.com")
                speak("Opening WhatsApp Web, sir.")

        # ── FOCUS MODE ───────────────────────────────
        elif "focus mode" in query:
            try:
                os.startfile("FocusMode.py")
                speak("Entering focus mode, sir.")
            except Exception:
                speak("Focus mode script not found, sir.")

        # ── MEDIA CONTROLS ───────────────────────────
        elif "pause" in query:
            pyautogui.press("k"); speak("Paused, sir.")
        elif "play" in query:
            pyautogui.press("k"); speak("Playing, sir.")
        elif "mute" in query:
            pyautogui.press("m"); speak("Muted, sir.")
        elif "volume up" in query:
            for _ in range(5): pyautogui.press("volumeup")
            speak("Volume up, sir.")
        elif "volume down" in query:
            for _ in range(5): pyautogui.press("volumedown")
            speak("Volume down, sir.")

        # ── SHUTDOWN ─────────────────────────────────
        elif "shutdown the system" in query:
            speak("Shutting down in 10 seconds, sir.")
            os.system("shutdown /s /t 10")

        elif "cancel shutdown" in query:
            os.system("shutdown /a")
            speak("Shutdown cancelled, sir.")

        # ── FINALLY SLEEP (kill server) ───────────────
        elif "finally sleep" in query:
            speak("Going to sleep. Goodbye, sir.")
            socketio.emit("state", {"awake": False, "shutdown": True})
            os._exit(0)

        # ── TRANSLATE ────────────────────────────────
        elif "translate" in query:
            try:
                from Translator import translategl
                q = query.replace("translate", "").replace("jarvis", "").strip()
                translategl(q)
            except ImportError:
                speak("Translator module not found, sir.")

        # ── TIRED / MUSIC ─────────────────────────────
        elif "tired" in query:
            try:
                from play_next_song import play_next_song
                speak("Playing your favourite songs, sir.")
                play_next_song()
            except ImportError:
                webbrowser.open("https://open.spotify.com")
                speak("Opening Spotify, sir.")

        # ── UNRECOGNIZED ──────────────────────────────
        else:
            socketio.emit("log", {
                "msg": f'Command not recognized: "{query}"',
                "type": "warn"
            })

    except Exception as exc:
        socketio.emit("log", {"msg": f"Error: {exc}", "type": "error"})


# ──────────────────────────────────────────────────────────────
#  SocketIO: Microphone control (starts Python speech listener)
# ──────────────────────────────────────────────────────────────
@socketio.on("mic_control")
def on_mic(data):
    global mic_running
    action = data.get("action")
    if action == "start" and not mic_running:
        mic_running = True
        threading.Thread(target=mic_listener, daemon=True).start()
        emit("log", {"msg": "Microphone active — listening...", "type": "sys"})
    elif action == "stop":
        mic_running = False
        emit("log", {"msg": "Microphone stopped.", "type": "warn"})

def mic_listener():
    """
    Runs in a background thread.
    Must NOT call on_command() — that needs a Flask request context.
    Instead, call run_command() directly for all processing.
    """
    global mic_running, jarvis_awake
    r = speech_recognition.Recognizer()
    r.pause_threshold = 1
    r.energy_threshold = 400

    # Calibrate for ambient noise once
    try:
        with speech_recognition.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=1)
    except Exception:
        pass

    while mic_running:
        try:
            with speech_recognition.Microphone() as source:
                audio = r.listen(source, timeout=3, phrase_time_limit=6)

            query = r.recognize_google(audio, language="en-in")
            socketio.emit("log", {"msg": f"Heard: {query}", "type": "heard"})

            q = query.lower().strip()

            # Handle wake/sleep directly (no request context needed)
            if "wake up" in q:
                jarvis_awake = True
                hour = datetime.datetime.now().hour
                greet = ("Good morning" if hour < 12 else
                         "Good afternoon" if hour < 18 else "Good evening")
                msg = f"{greet}, sir. All systems are online."
                speak(msg)
                socketio.emit("state", {"awake": True})

            elif "go to sleep" in q:
                jarvis_awake = False
                speak("Ok sir, call me anytime.")
                socketio.emit("state", {"awake": False})

            elif not jarvis_awake:
                socketio.emit("log", {
                    "msg": "Jarvis is in standby. Say wake up to activate.",
                    "type": "warn"
                })

            else:
                # Run command in its own thread so mic stays alive
                threading.Thread(target=run_command, args=(q,), daemon=True).start()

        except speech_recognition.WaitTimeoutError:
            continue
        except speech_recognition.UnknownValueError:
            continue
        except Exception as e:
            socketio.emit("log", {"msg": f"Mic error: {e}", "type": "error"})
            break

    mic_running = False
    socketio.emit("log", {"msg": "Microphone stopped.", "type": "warn"})


# ──────────────────────────────────────────────────────────────
#  Main
# ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Create missing support files
    for fname, default in [("password.txt", "1234"), ("tasks.txt", ""), ("Remember.txt", "")]:
        if not os.path.exists(fname):
            with open(fname, "w") as f:
                f.write(default)

    print("\n" + "=" * 55)
    print("  J.A.R.V.I.S  — Server starting...")
    print("  ▶  Open in browser:  http://localhost:5000")
    print("  Default password:    1234")
    print("=" * 55 + "\n")

    socketio.run(app, host="0.0.0.0", port=5000, debug=False)