import time
import threading
import random
import pyautogui
from pynput.keyboard import Listener

from config import *


def clicker():
    global exit_flag, x, y, sleep_time
    while True:
        if exit_flag:
            break
        if clicking:
            # Случайные координаты
            x = random.randint(1760, 1910)
            y = random.randint(895, 995)

            clicks = random.randint(1, 5)

            pyautogui.click(x, y, clicks)
        sleep_time = random.uniform(0.1, 0.5)
        time.sleep(sleep_time)


def toggle_event(key):
    global clicking, exit_flag
    if key == toggle_key:
        clicking = not clicking
        print('Clicking:', clicking)
    elif key == exit_key:
        exit_flag = True
        print('Exiting...')
        return False


def main():
    global exit_flag
    clicking_thread = threading.Thread(target=clicker)
    clicking_thread.daemon = True
    clicking_thread.start()

    with Listener(on_release=toggle_event) as listener:
        try:
            listener.join()
        except KeyboardInterrupt:
            exit_flag = True
            print('Interrupted!!! Exiting...')

    clicking_thread.join() # Ждем завершения потока перед выходом

if __name__ == '__main__':
    main()
