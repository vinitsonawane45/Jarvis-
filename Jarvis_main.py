import pyttsx3
import speech_recognition 
import requests
import datetime
import os
import pyautogui
import random
from plyer import notification
from pygame import mixer
import webbrowser
import speedtest
import sys
import tkinter as tk
from tkinter import scrolledtext





for i in range(3):
    a = input("Enter Password to open Jarvis :- ")
    pw_file = open("password.txt","r")
    pw = pw_file.read()
    pw_file.close()
    if (a==pw):
        print("WELCOME SIR ! PLZ SPEAK [WAKE UP] TO LOAD ME UP")
        break
    elif (i==2 and a!=pw):
        exit()

    elif (a!=pw):
        print("Try Again")





    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[0].id)
    rate = engine.setProperty("rate",170)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    r = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        print("Listening.....")
        r.pause_threshold = 1
        r.energy_threshold = 400
        audio = r.listen(source,0,4)

    try:
        print("Understanding..")
        query  = r.recognize_google(audio,language='en-in')
        print(f"You Said: {query}\n")
    except Exception as e:
        print("Say that again")
        return "None"
    return query



# def alarm(query):
#     timehere = open("Alarmtext.txt","a")
#     timehere.write(query)
#     timehere.close()
#     os.startfile("alarm.py")


if __name__ == "__main__":
    while True:
        query = takeCommand().lower()
        if "wake up" in query:
            from GreetMe import greetMe
            greetMe()

            while True:
                query = takeCommand().lower()
                if "go to sleep" in query:
                    speak("Ok sir , You can me call anytime")
                    break 

                 ########### JAERVIS THE TARILOGY 2.0################
                elif "change password" in query:
                    speak("What's the new password")
                    new_pw = input("Enter the new password\n")
                    new_password = open("password.txt","w")
                    new_password.write(new_pw)
                    new_password.close()
                    speak("Done sir")
                    speak(f"Your new password is{new_pw}")

                elif "schedule my day" in query:
                    tasks = [] #Empty list 
                    speak("Do you want to clear old tasks (Plz speak YES or NO)")
                    query = takeCommand().lower()
                    if "yes" in query:
                            file = open("tasks.txt","w")
                            file.write(f"")
                            file.close()
                            no_tasks = int(input("Enter the no. of tasks :- "))
                            i = 0
                            for i in range(no_tasks):
                                tasks.append(input("Enter the task :- "))
                                file = open("tasks.txt","a")
                                file.write(f"{i}. {tasks[i]}\n")
                                file.close()
                    elif "no" in query:
                                i = 0
                                no_tasks = int(input("Enter the no. of tasks :- "))
                    for i in range(no_tasks):
                        tasks.append(input("Enter the task :- "))
                        file = open("tasks.txt","a")
                        file.write(f"{i}. {tasks[i]}\n")
                        file.close()

                elif "show my schedule" in query:
                        file = open("tasks.txt","r")
                        content = file.read()
                        file.close()
                        mixer.init()
                        mixer.music.load("notification.mp3")
                        mixer.music.play()
                        notification.notify(
                        title = "My schedule :-",
                        message = content,
                        timeout = 15
                            )

                elif "open" in query:   #EASY METHOD
                    query = query.replace("open","")
                    query = query.replace("jarvis","")
                    pyautogui.press("super")
                    pyautogui.typewrite(query)
                    pyautogui.sleep(2)
                    pyautogui.press("enter") 
                    



               


                elif "internet speed" in query:
                    wifi  = speedtest.Speedtest()
                    upload_net = wifi.upload()/1048576         #Megabyte = 1024*1024 Bytes
                    download_net = wifi.download()/1048576
                    print("Wifi Upload Speed is", upload_net)
                    print("Wifi download speed is ",download_net)
                    speak(f"Wifi download speed is {download_net}")
                    speak(f"Wifi Upload speed is {upload_net}")

                elif "Ipl Score" in query:
                    from plyer import notification  #pip install plyer
                    import requests #pip install requests
                    from bs4 import BeautifulSoup #pip install bs4
                    url = "https://www.cricbuzz.com/"
                    page = requests.get(url)
                    soup = BeautifulSoup(page.text,"html.parser")
                    team1 = soup.find_all(class_ = "cb-ovr-flo cb-hmscg-tm-nm")[0].get_text()
                    team2 = soup.find_all(class_ = "cb-ovr-flo cb-hmscg-tm-nm")[1].get_text()
                    team1_score = soup.find_all(class_ = "cb-ovr-flo")[8].get_text()
                    team2_score = soup.find_all(class_ = "cb-ovr-flo")[10].get_text()

                    a = print(f"{team1} : {team1_score}")
                    b = print(f"{team2} : {team2_score}")

                    notification.notify(
                        title = "IPL SCORE :- ",
                        message = f"{team1} : {team1_score}\n {team2} : {team2_score}",
                        timeout = 15
                    )
                elif "play a game" in query:
                    from game import game_play
                    game_play()

                elif "screenshot" in query:
                     import pyautogui #pip install pyautogui
                     im = pyautogui.screenshot()
                     im.save("ss.jpg")
                elif "click my photo" in query:
                    pyautogui.press("super")
                    pyautogui.typewrite("camera")
                    pyautogui.press("enter")
                    pyautogui.sleep(2)
                    speak("SMILE")
                    pyautogui.press("enter")
                
                elif "focus mode" in query:
                    a = int(input("Are you sure that you want to enter focus mode :- [1 for YES / 2 for NO "))
                    if (a==1):
                        speak("Entering the focus mode....")
                        os.startfile("D:\\Coding\\Youtube\\Jarvis\\FocusMode.py")
                        exit()
                    else:
                        pass
                
                elif "show my focus" in query:
                    from FocusGraph import focus_graph
                    focus_graph()

                elif "translate" in query:
                    from Translator import translategl
                    query = query.replace("jarvis","")
                    query = query.replace("translate","")
                    translategl(query)

                


                 

                 ###################################################
    


            
                # elif "tired" in query:
                #     speak("Playing your favourite songs, sir")
                #     a = (1,2,3) # You can choose any number of songs (I have only choosen 3)
                #     b = random.choice(a)
                #     if b==1:
                #         webbrowser.open("https://open.spotify.com/playlist/6qy2c4so678KpMN7tAzhfgkm") 

                elif "tired" in query:
                    speak("Playing your favourite songs, sir")
                    from play_next_song import play_next_song
                    
                elif "pause" in query:
                    pyautogui.press("k")
                    speak("video paused")
                elif "play" in query:
                    pyautogui.press("k")
                    speak("video played")
                elif "mute" in query:
                    pyautogui.press("m")
                    speak("video muted")
                elif "next video" in query:
                    from play_next_song import play_next_song

                elif "volume up" in query:
                    from keyboard import volumeup
                    speak("Turning volume up,sir")
                    volumeup()
                elif "volume down" in query:
                    from keyboard import volumedown
                    speak("Turning volume down, sir")
                    volumedown()


                elif "open" in query:
                    from Dictapp import openappweb
                    openappweb(query)

                elif "close" in query:
                    from Dictapp import closeappweb
                    closeappweb(query)

        
            

                elif "google" in query:
                    from SearchNow import searchGoogle
                    searchGoogle(query)

                elif "youtube" in query:
                    from SearchNow import searchYoutube
                    searchYoutube(query)

                elif "wikipedia" in query:
                    from SearchNow import searchWikipedia
                    searchWikipedia(query)

                elif "news" in query:
                    from NewsRead import latestnews
                    latestnews()

                elif "calculate" in query:
                    from Calculatenumbers import WolfRamAlpha
                    from Calculatenumbers import Calc
                    query = query.replace("calculate","")
                    query = query.replace("jarvis","")
                    Calc(query)

                elif "Open whatsapp" in query:
                    from Whatsapp import sendMessage
                    sendMessage()

                elif "shutdown the system" in query:
                    speak("Are You sure you want to shutdown")
                    shutdown = input("Do you wish to shutdown your computer? (yes/no)")
                    if shutdown == "yes":
                        os.system("shutdown /s /t 1")

                    elif shutdown == "no":
                        break

                

                elif "temperature" in query:
                    search = "temperature in Maharashtra"
                    url = f"https://www.google.com/search?q={search}"
                    r  = requests.get(url)
                    data = BeautifulSoup(r.text,"html.parser")
                    temp = data.find("div", class_ = "BNeawe").text
                    speak(f"current{search} is {temp}")

                elif "weather" in query:
                    search = "temperature in Maharashtra"
                    url = f"https://www.google.com/search?q={search}"
                    r  = requests.get(url)
                    data = BeautifulSoup(r.text,"html.parser")
                    temp = data.find("div", class_ = "BNeawe").text
                    speak(f"current{search} is {temp}")

                elif "set an alarm" in query:
                    print("input time example:- 10 and 10 and 10")
                    speak("Set the time")
                    a = input("Please tell the time :- ")
                    alarm(a)
                    speak("Done,sir")


                elif "the time" in query:
                    strTime = datetime.datetime.now().strftime("%H:%M")    
                    speak(f"Sir, the time is {strTime}")

                elif "finally sleep" in query:
                    speak("Going to sleep,sir")
                    exit()
                
                elif "remember that" in query:
                    rememberMessage = query.replace("remember that","")
                    rememberMessage = query.replace("jarvis","")
                    speak("You told me to remember that"+rememberMessage)
                    remember = open("Remember.txt","a")
                    remember.write(rememberMessage)
                    remember.close()
                elif "what do you remember" in query:
                    remember = open("Remember.txt","r")
                    speak("You told me to remember that" + remember.read())

    
# =================================================================================================




# import pyttsx3
# import speech_recognition as sr
# import requests
# import datetime
# import os
# import pyautogui
# import speedtest
# import sys
# from plyer import notification
# from pygame import mixer
# import webbrowser
# from bs4 import BeautifulSoup
# import time
# from transformers import AutoModelForCausalLM, AutoTokenizer

# # Download the Mistral model and tokenizer
# model_name = "mistral-7b"  # Replace with the desired Mistral model name
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModelForCausalLM.from_pretrained(model_name)

# # Local Mistral query function
# def mistral_query_local(query):
#     inputs = tokenizer(query, return_tensors="pt")
#     outputs = model.generate(inputs['input_ids'], max_length=200)
#     response = tokenizer.decode(outputs[0], skip_special_tokens=True)
#     return response

# def speak(audio):
#     engine = pyttsx3.init("sapi5")
#     voices = engine.getProperty("voices")
#     engine.setProperty("voice", voices[0].id)
#     engine.setProperty("rate", 170)
#     engine.say(audio)
#     engine.runAndWait()

# def take_command():
#     r = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Listening...")
#         r.pause_threshold = 1
#         r.energy_threshold = 400
#         audio = r.listen(source, 0, 4)
#     try:
#         print("Recognizing...")
#         query = r.recognize_google(audio, language='en-in')
#         print(f"You said: {query}\n")
#     except Exception as e:
#         print("Could not understand. Say that again.")
#         return "None"
#     return query.lower()

# def authenticate():
#     for i in range(3):
#         user_input = input("Enter Password to open JARVIS: ")
#         with open("password.txt", "r") as pw_file:
#             stored_pw = pw_file.read().strip()
#         if user_input == stored_pw:
#             print("WELCOME SIR! Speak 'Wake up' to load me up.")
#             return True
#         elif i == 2:
#             print("Too many failed attempts. Exiting...")
#             sys.exit()
#         else:
#             print("Incorrect password, try again.")
#     return False

# def check_internet_speed():
#     wifi = speedtest.Speedtest()
#     download_speed = wifi.download() / 1048576  # Convert to MBps
#     upload_speed = wifi.upload() / 1048576
#     print(f"Download Speed: {download_speed:.2f} Mbps")
#     print(f"Upload Speed: {upload_speed:.2f} Mbps")
#     speak(f"Download speed is {download_speed:.2f} Mbps and upload speed is {upload_speed:.2f} Mbps")

# def get_ipl_score():
#     url = "https://www.cricbuzz.com/"
#     page = requests.get(url)
#     soup = BeautifulSoup(page.text, "html.parser")
#     try:
#         team1 = soup.find_all(class_="cb-ovr-flo cb-hmscg-tm-nm")[0].get_text()
#         team2 = soup.find_all(class_="cb-ovr-flo cb-hmscg-tm-nm")[1].get_text()
#         team1_score = soup.find_all(class_="cb-ovr-flo")[8].get_text()
#         team2_score = soup.find_all(class_="cb-ovr-flo")[10].get_text()
#         print(f"{team1}: {team1_score}\n{team2}: {team2_score}")
#         notification.notify(
#             title="IPL SCORE: ",
#             message=f"{team1}: {team1_score}\n{team2}: {team2_score}",
#             timeout=15
#         )
#     except Exception as e:
#         print("Could not fetch IPL score.")
#         speak("Sorry, I couldn't get the IPL score.")

# def check_temperature():
#     search = "temperature in Maharashtra"
#     url = f"https://www.google.com/search?q={search}"
#     r = requests.get(url)
#     soup = BeautifulSoup(r.text, "html.parser")
#     temp = soup.find("div", class_="BNeawe").text
#     print(f"Current temperature: {temp}")
#     speak(f"Current temperature in Maharashtra is {temp}")

# def main():
#     if authenticate():
#         while True:
#             query = take_command()
#             if "wake up" in query:
#                 speak("How can I assist you?")
#                 while True:
#                     query = take_command()
#                     if "go to sleep" in query:
#                         speak("Okay sir, call me anytime.")
#                         break
#                     elif "internet speed" in query:
#                         check_internet_speed()
#                     elif "ipl score" in query:
#                         get_ipl_score()
#                     elif "temperature" in query or "weather" in query:
#                         check_temperature()
#                     elif "shutdown the system" in query:
#                         speak("Are you sure you want to shut down?")
#                         confirm = input("Confirm shutdown (yes/no): ").lower()
#                         if confirm == "yes":
#                             os.system("shutdown /s /t 1")
#                         else:
#                             speak("Shutdown cancelled.")
#                     elif "what is the time" in query:
#                         current_time = datetime.datetime.now().strftime("%H:%M")
#                         speak(f"Sir, the time is {current_time}")
#                     elif "finally sleep" in query:
#                         speak("Going to sleep, sir.")
#                         sys.exit()
#                     else:
#                         # Use the locally loaded Mistral model for queries
#                         response = mistral_query_local(query)
#                         speak(response)

# if __name__ == "__main__":
#     main()
