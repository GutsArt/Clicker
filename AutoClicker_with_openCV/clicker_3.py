import pyautogui
import time

image_paths = [
    'SCREENS/screen1.png',
    'SCREENS/screen2.png',
    'SCREENS/screen3.png',
    'SCREENS/screen4.png',
    'SCREENS/screen5.png',
    'SCREENS/screen6.png'
]
def main(image_paths):
    i = 0
    # Применение функции ко всем изображениям
    for index, path in enumerate(image_paths):
        find_and_click_image(path, i)  # Обычный клик для остальных
        i += 10
        pyautogui.sleep(1)  # Задержка между кликами
    click_Hamser(image_paths[5])

    print("Скрипт завершен.")

def find_and_click_image(image_path, time, confidence=0.7):
    try:
        button = pyautogui.locateOnScreen(image_path, time, confidence=confidence, region=(1740, 760, 180, 320))
        if button:
            pyautogui.click(button, button='right')
            print(f"Клик выполнен для {image_path}.")
        else:
            print(f"Изображение {image_path} не найдено на экране.")
    except pyautogui.PyAutoGUIException as e:
        print(f"Ошибка при обработке {image_path}: ", e)


def click_Hamser(image_path, clicks=500, delay=0.25, confidence=0.75, region=(1740, 760, 180, 320)):
    try:
        button = pyautogui.locateOnScreen(image_path, confidence=confidence, region=region)
        if button:
            while True:
                for _ in range(clicks):
                    pyautogui.click(button, button='SECONDARY')
                    pyautogui.sleep(delay)

                current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                print("Current Time:", current_time)
                pyautogui.sleep(10 * 60)
        else:
            print(f"Изображение {image_path} не найдено на экране.")
    except pyautogui.PyAutoGUIException as e:
        print(f"Ошибка при обработке {image_path}: ", e)


if __name__ == "__main__":
    main(image_paths)