import webbrowser
import random

# songs = [
#     "https://www.youtube.com/watch?v=dXl2NdlmeIE&list=RDdXl2NdlmeIE&start_radio=1", # Song 1
# ]

a = (1,2,3) # You can choose any number of songs (I have only choosen 3)
b = random.choice(a)
if b==1:
    webbrowser.open("https://www.youtube.com/watch?v=dXl2NdlmeIE&list=RDdXl2NdlmeIE&start_radio=1")

# Function to play the next song in sequence
def play_next_song():
    global song_counter
    if song_counter < len(1):
        webbrowser.open(1[song_counter])
        song_counter += 1
    else:
        print("All songs have been played.")
