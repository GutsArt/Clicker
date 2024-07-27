import time
import threading
from pynput.mouse import Controller, Button
from pynput.keyboard import Listener, Key, KeyCode

toggle_key = KeyCode(char='p')
exit_key = Key.esc

clicking = False
exit_flag = False
mouse = Controller()


def clicker():
    while True:
        if exit_flag:
            break
        if clicking:
            mouse.click(Button.left, 1)
        time.sleep(0.1)


def toggle_event(key):
    if key == toggle_key:
        global clicking
        clicking = not clicking
        print('Clicking:', clicking)
    elif key == exit_key:
        exit_flag = True
        print('Exiting...')
        return False


def main():
    clicking_thread = threading.Thread(target=clicker)
    clicking_thread.start()

    with Listener(on_release=toggle_event) as listener:
        listener.join()

if __name__ == '__main__':
    main()
