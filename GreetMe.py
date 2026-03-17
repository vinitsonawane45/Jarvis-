import pyttsx3
import datetime

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate",200)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def greetMe():
    hour  = int(datetime.datetime.now().hour)
    if hour>=0 and hour<=12:
        speak("Good Morning,sir")
    elif hour >12 and hour<=18:
        speak("Good Afternoon ,sir")

    else:
        speak("Good Evening,sir")

    speak("Please tell me, How can I help you ?")

# import pyttsx3
# import datetime

# engine = pyttsx3.init("sapi5")
# voices = engine.getProperty("voices")

# # Check if there are available voices
# if len(voices) > 0:
#     engine.setProperty("voice", voices[0].id)  # You can change the index for different voices
# engine.setProperty("rate", 200)

# def speak(audio):
#     engine.say(audio)
#     engine.runAndWait()

# def greetMe():
#     hour = int(datetime.datetime.now().hour)
#     if hour >= 0 and hour < 12:
#         speak("Good Morning, sir.")
#     elif hour >= 12 and hour < 18:
#         speak("Good Afternoon, sir.")
#     else:
#         speak("Good Evening, sir.")
    
#     speak("Please tell me how I can help you.")

# # Call the greetMe function to test it
# greetMe()
