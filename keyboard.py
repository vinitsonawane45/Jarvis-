# from pynput.keyboard  import Key,Controller

# from time import sleep

# keyboard = Controller()

# def volumeup():
#     for i in range(5):
#         keyboard.press(Key.media_volume_up)
#         keyboard.release(Key.media_volume_up)
#         sleep(0.1)
# def volumedown():
#     for i in range(5):
#         keyboard.press(Key.media_volume_down)
#         keyboard.release(Key.media_volume_down)
#         sleep(0.1)


from pynput.keyboard import Key, Controller

from time import sleep

keyboard = Controller()

def volume_up():
    for i in range(5):
        # Press the volume up key
        keyboard.press(Key.media_volume_up)
        keyboard.release(Key.media_volume_up)
        sleep(0.1)

def volume_down():
    for i in range(5):
        # Press the volume down key
        keyboard.press(Key.media_volume_down)
        keyboard.release(Key.media_volume_down)
        sleep(0.1)


