# import subprocess
# import os

# def open_application(app):
#     try:
#         # Windows: Use start to open applications (e.g., chrome, notepad)
#         if os.name == 'nt':  # Windows
#             subprocess.run(["start", app], shell=True)
#         elif os.name == 'posix':  # macOS/Linux
#             subprocess.run(["open", app], check=True)  # For macOS
#             # subprocess.run(["xdg-open", app], check=True)  # For Linux
#         print(f"Opening {app}")
#     except Exception as e:
#         print(f"Error opening {app}: {e}")

# def close_application(app):
#     try:
#         # Windows: Use taskkill to close applications (e.g., chrome.exe, notepad.exe)
#         if os.name == 'nt':  # Windows
#             subprocess.run(["taskkill", "/im", f"{app}.exe", "/f"], check=True)
#         elif os.name == 'posix':  # macOS/Linux
#             subprocess.run(["killall", app], check=True)  # For macOS
#             # subprocess.run(["pkill", app], check=True)  # For Linux
#         print(f"Closing {app}")
#     except Exception as e:
#         print(f"Error closing {app}: {e}")

# def main():
#     print("Hello, I'm your assistant. Type 'open <app>' to open an application, 'close <app>' to close it.")
#     while True:
#         command = input("Command: ").lower().strip()
        
#         if command.startswith("open"):
#             app = command.replace("open", "").strip()
#             open_application(app)
#         elif command.startswith("close"):
#             app = command.replace("close", "").strip()
#             close_application(app)
#         elif command == "exit":
#             print("Goodbye!")
#             break
#         else:
#             print("Sorry, I don't understand that command.")

# if __name__ == "__main__":
#     main()



import subprocess
import os
import speech_recognition as sr
import pyttsx3

# # Initialize the speech engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def open_application(app):
    try:
        # For Windows: Use start to open applications (e.g., chrome, notepad)
        if os.name == 'nt':  # Windows
            subprocess.run(["start", app], shell=True)
        elif os.name == 'posix':  # macOS/Linux
            subprocess.run(["open", app], check=True)  # For macOS
            # subprocess.run(["xdg-open", app], check=True)  # For Linux
        speak(f"Opening {app}")
    except Exception as e:
        speak(f"Error opening {app}: {e}")

def close_application(app):
    try:
        # For Windows: Use taskkill to close applications (e.g., chrome.exe, notepad.exe)
        if os.name == 'nt':  # Windows
            subprocess.run(["taskkill", "/im", f"{app}.exe", "/f"], check=True)
        elif os.name == 'posix':  # macOS/Linux
            subprocess.run(["killall", app], check=True)  # For macOS
            # subprocess.run(["pkill", app], check=True)  # For Linux
        speak(f"Closing {app}")
    except Exception as e:
        speak(f"Error closing {app}: {e}")

def listen_for_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for your command...")
        speak("Listening for your command...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            speak("Sorry, I didn't understand that.")
            return None
        except sr.RequestError:
            speak("Sorry, I'm having trouble connecting to the speech recognition service.")
            return None
        

# def main():
#     while True:
#         command = listen_for_command()

#         if command:
#             if "open" in command:
#                 app = command.replace("open", "").strip()
#                 open_application(app)
#             elif "close" in command:
#                 app = command.replace("close", "").strip()
#                 close_application(app)
#             elif "exit" in command:
#                 speak("Goodbye!")
#                 break
#             else:
#                 speak("Sorry, I didn't understand that command.")

# if __name__ == "__main__":
#     main()