import keyboard
import pyautogui
import time
import threading
import random
from pynput.keyboard import Listener
from config import *

image_paths = [
    'SCREENS/screen1.png',
    'SCREENS/screen2.png',
    'SCREENS/screen3.png',
    'SCREENS/screen4.png',
    'SCREENS/screen5.png',
    'SCREENS/screen6.png',
    'SCREENS/Error.png',
]


def find_and_click_image(image_path, confidence=0.7):
    try:
        if (button := pyautogui.locateOnScreen(image_path, confidence=confidence, region=(1740, 760, 180, 320))):
            pyautogui.click(button, button='right')
            print(f"Клик выполнен для {image_path}.")
            pyautogui.sleep(15)
        else:
            print(f"Изображение {image_path} не найдено на экране.")
    except pyautogui.PyAutoGUIException as e:
        print(f"Ошибка при обработке {image_path}: {e}")


def scroll_Hamster(image_path, scroll_times=20, confidence=0.7):
    try:
        if (button := pyautogui.locateOnScreen(image_path, confidence=confidence, region=(1740, 760, 180, 320))):
            pyautogui.moveTo(button)
            for _ in range(scroll_times):
                pyautogui.press('down')
                pyautogui.sleep(0.1)
            print(f"Клик down выполнен для {image_path}.")
            # pyautogui.scroll(scroll_amount)
            # print(f"Прокрутка выполнена для {image_path}.")
        else:
            print(f"Изображение {image_path} не найдено на экране.")
    except pyautogui.PyAutoGUIException as e:
        print(f"Ошибка при обработке {image_path}: {e}")


def click_Hamser(image_path, clicks=5, all_clicks=500, delay=0.25, confidence=0.75, region=(1740, 760, 180, 320)):
    i = 0
    while (i < all_clicks) and (CLICKING):
        try:
            if (button := pyautogui.locateOnScreen(image_path, confidence=confidence, region=region)):
                # Получаем координаты центра найденной области
                x, y = pyautogui.center(button)

                # Добавляем случайное смещение
                x += random.randint(-50, 50)
                y += random.randint(-50, 50)

                pyautogui.click(x=x, y=y, clicks=clicks, interval=delay, button='right')
                time.sleep(delay)
                i += clicks
            else:
                print(f"Изображение {image_path} не найдено на экране.")
                time.sleep(15)
                break
        except pyautogui.PyAutoGUIException as e:
            print(f"Ошибка при обработке {image_path}: {e}")
            break
    if i == 500:
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(f"Current Time: {current_time} +7014")
        pyautogui.sleep(10 * 60)


def on_press(key):
    global CLICKING, exit_flag
    if key == toggle_key:
        CLICKING = not CLICKING
        print("Скрипт запущен." if CLICKING else "Скрипт остановлен.")
    # elif key == exit_key:
    #     exit_flag = True
    #     print("Выход из скрипта.")
    #     return False  # Остановить слушатель
    # if keyboard.is_pressed("Esc"):
    #     exit_flag = True
    #     print("Прерывание работы скрипта.")
    elif keyboard.read_key() == "esc":
        exit_flag = True
        print("Прерывание работы скрипта.")
        return False


def main(image_paths):
    global CLICKING, exit_flag
    while not exit_flag:
        if CLICKING:
            for path in (image_paths[:4] + [image_paths[6]]):
                find_and_click_image(path)
                time.sleep(1)
            scroll_Hamster(image_paths[4])
            click_Hamser(image_paths[5])
            time.sleep(1 * 60)
        else:
            print("else:")
            time.sleep(10)
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
