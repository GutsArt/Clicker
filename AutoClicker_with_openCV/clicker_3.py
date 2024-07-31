import pyautogui

path1 = 'SCREENS/screen1.png'
path2 = 'SCREENS/screen2.png'

try:
    button = pyautogui.locateOnScreen(path1, confidence = 0.5)
    if button is not None:
        pyautogui.doubleClick(button)
        print("Двойной клик выполнен.")
    else:
        print("Изображение не найдено на экране.")
except pyautogui.PyAutoGUIException as e:
    print("Ошибка: ", e)

pyautogui.sleep(1)

try:
    button = pyautogui.locateOnScreen(path2, confidence = 0.8)
    if button is not None:
        # pyautogui.moveTo(button)
        pyautogui.click(button)
        print("Клик выполнен.")
except pyautogui.PyAutoGUIException as e:
    print("Ошибка: ", e)