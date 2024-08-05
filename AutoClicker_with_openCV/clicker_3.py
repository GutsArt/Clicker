import pyautogui
import time
import threading
from pynput.keyboard import Listener
from config import *

image_paths = [
    'SCREENS/screen1.png',
    'SCREENS/screen2.png',
    'SCREENS/screen3.png',
    'SCREENS/screen4.png',
    'SCREENS/screen5.png',
    'SCREENS/screen6.png'
]

def find_and_click_image(image_path, confidence=0.7):
    try:
        if (button := pyautogui.locateOnScreen(image_path, confidence=confidence, region=(1740, 760, 180, 320))):
            pyautogui.click(button, button='right')
            print(f"Клик выполнен для {image_path}.")
        else:
            print(f"Изображение {image_path} не найдено на экране.")
    except pyautogui.PyAutoGUIException as e:
        print(f"Ошибка при обработке {image_path}: {e}")

def click_Hamser(image_path, clicks=5, all_clicks=500, delay=0.25, confidence=0.75, region=(1740, 760, 180, 320)):
    i = 0
    while (i < all_clicks) and (clicking):
        try:
            if (button := pyautogui.locateOnScreen(image_path, confidence=confidence, region=region)):
                pyautogui.click(button, clicks=clicks, interval=delay, button='right')
                time.sleep(delay)
                current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                print("Current Time:", current_time)
                i += clicks
            else:
                print(f"Изображение {image_path} не найдено на экране.")
                time.sleep(15)
                # break
        except pyautogui.PyAutoGUIException as e:
            print(f"Ошибка при обработке {image_path}: {e}")






def on_press(key):
    global clicking, exit_flag
    if key == toggle_key:
        clicking = not clicking
        print("Скрипт запущен." if clicking else "Скрипт остановлен.")
    elif key == exit_key:
        exit_flag = True
        print("Выход из скрипта.")
        return False  # Остановить слушатель

def main(image_paths):
    global clicking, exit_flag
    while True:
        if exit_flag:
            break
        if clicking:
            for path in image_paths:
                find_and_click_image(path)
                time.sleep(1)
            click_Hamser(image_paths[5])
        else:
            time.sleep(10)
            print("else:")
            # break

def listen_for_keys():
    with Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    listener_thread = threading.Thread(target=listen_for_keys, daemon=True)
    listener_thread.start()

    try:
        main(image_paths)
    except KeyboardInterrupt:
        exit_flag = True
        print("Прерывание работы скрипта.")
    finally:
        listener_thread.join()
