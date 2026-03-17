# import os 
# import pyautogui
# import webbrowser
# import pyttsx3
# from time import sleep

# engine = pyttsx3.init("sapi5")
# voices = engine.getProperty("voices")
# engine.setProperty("voice", voices[0].id)
# engine.setProperty("rate",200)

# def speak(audio):
#     engine.say(audio)
#     engine.runAndWait()

# dictapp = {"commandprompt":"cmd","paint":"paint","word":"winword","excel":"excel","chrome":"chrome","vscode":"code","powerpoint":"powerpoint","google":"google","google chrome":"chrome",
#            "fireFox":"firefox","Microsoft Edge":"Microsoft Edge"}

# def openappweb(query):
#     speak("Launching, sir")
#     if ".com" in query or ".co.in" in query or ".org" in query:
#         query = query.replace("open","")
#         query = query.replace("jarvis","")
#         query = query.replace("launch","")
#         query = query.replace(" ","")
#         webbrowser.open(f"https://www.{query}")
#     else:
#         keys = list(dictapp.keys())
#         for app in keys:
#             if app in query:
#                 os.system(f"start {dictapp[app]}")

# def closeappweb(query):
#     speak("Closing,sir")
#     if "one tab" in query or "1 tab" in query:
#         pyautogui.hotkey("ctrl","w")
#         speak("All tabs closed")
#     elif "2 tab" in query:
#         pyautogui.hotkey("ctrl","w")
#         sleep(0.5)
#         pyautogui.hotkey("ctrl","w")
#         speak("All tabs closed")
#     elif "3 tab" in query:
#         pyautogui.hotkey("ctrl","w")
#         sleep(0.5)
#         pyautogui.hotkey("ctrl","w")
#         sleep(0.5)
#         pyautogui.hotkey("ctrl","w")
#         speak("All tabs closed")
        
#     elif "4 tab" in query:
#         pyautogui.hotkey("ctrl","w")
#         sleep(0.5)
#         pyautogui.hotkey("ctrl","w")
#         sleep(0.5)
#         pyautogui.hotkey("ctrl","w")
#         sleep(0.5)
#         pyautogui.hotkey("ctrl","w")
#         speak("All tabs closed")
#     elif "5 tab" in query:
#         pyautogui.hotkey("ctrl","w")
#         sleep(0.5)
#         pyautogui.hotkey("ctrl","w")
#         sleep(0.5)
#         pyautogui.hotkey("ctrl","w")
#         sleep(0.5)
#         pyautogui.hotkey("ctrl","w")
#         sleep(0.5)
#         pyautogui.hotkey("ctrl","w")
#         speak("All tabs closed")

#     else:
#         keys = list(dictapp.keys())
#         for app in keys:
#             if app in query:
#                 os.system(f"taskkill /f /im {dictapp[app]}.exe")



import os
import pyautogui
import webbrowser
import pyttsx3
from time import sleep
import subprocess

engine = pyttsx3.init("sapi5")

voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 200)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

dictapp = {
    "commandprompt": "cmd", "paint": "paint", "word": "winword", "excel": "excel", 
    "chrome": "chrome", "vscode": "code", "powerpoint": "powerpoint", "google": "google", 
    "google chrome": "chrome", "firefox": "firefox", "Microsoft Edge": "Microsoft Edge"
}

def openappweb(query):
    speak("Launching, sir")
    query = query.lower().replace("open", "").replace("launch", "").replace("jarvis", "").replace(" ", "")
    
    if ".com" in query or ".co.in" in query or ".org" in query:
        webbrowser.open(f"https://www.{query}")
    else:
        for app, exe in dictapp.items():
            if app in query:
                subprocess.Popen([exe])

def closeappweb(query):
    speak("Closing, sir")
    # Check for closing a specific number of tabs, e.g., "close 1 tab", "close 2 tab", etc.
    tabs_to_close = {
        "one tab": 1, "2 tab": 2, "3 tab": 3, "4 tab": 4, "5 tab": 5
    }

    tabs = tabs_to_close.get(query.lower(), 0)  # Make the query case-insensitive
    if tabs > 0:
        for _ in range(tabs):
            pyautogui.hotkey("ctrl", "w")
            sleep(0.5)
        speak(f"{tabs} tabs closed")
    else:
        # Check for application name (e.g., "firefox", "chrome") to close the app
        for app, exe in dictapp.items():
            if app in query.lower():  # Case-insensitive check
                os.system(f"taskkill /f /im {exe}.exe")
                speak(f"Closing {app}")
                return  # Exit after closing the app

        # If no specific app found, try closing the active window or tab
        pyautogui.hotkey("ctrl", "w")
        sleep(0.5)
        speak("Tab closed")

