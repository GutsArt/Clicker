import keyboard
import mouse
import time

isClicking = False

def set_click():
    global isClicking
    if isClicking:
        isClicking = False
        print('Mouse click stopped')
    else:
        isClicking = True
        print('Mouse click started')


keyboard.add_hotkey('Ctrl + P', set_click)

while True:
    if isClicking:
        mouse.double_click(button = 'left')
        time.sleep(0.1)  # Wait for a short while before making the next click