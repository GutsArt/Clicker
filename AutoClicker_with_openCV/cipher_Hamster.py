import pyautogui
import time
import requests
from bs4 import BeautifulSoup
from config import *

import re

img_Cipher = r"SCREENS\screenCipher.png"
img_Cipher_Red = r"SCREENS\screenCipherRed.png"
img_Cipher_Coin = r"SCREENS\screenCipherGetCoins.png"

img_Blue = r"SCREENS\ScreenBlue.png"


def get_iform_cipher_Hamster():
    from datetime import datetime
    now = datetime.now()
    day = now.day + 1
    month = now.strftime("%B").lower()
    link = f"https://sumorb.com/crypto/hamster-kombat-daily-cipher-and-combo-code-for-{day}-{month}-2024/"
    print(link)
    response = requests.get(link)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        if (ul_element := soup.find_all("ul", class_="wp-block-list")[1]):
            cipher_codes = []
            li_elements = ul_element.find_all("li")
            for li in li_elements:
                # Extract text within parentheses
                text = li.get_text()
                print(text)
                start = text.find("(")
                end = text.find(")")
                if start != -1 and end != -1:
                    cipher_code = text[start + 1:end]
                    cipher_codes.append(cipher_code)
            return cipher_codes
        else:
            print("Error: wp-block-list not find")
            return None
    else:
        print("Failed to retrieve the webpage.")
        return None


def manual_input():
    # Запрашиваем код шифра через графический интерфейс
    cipher_code = pyautogui.prompt(title="Hamster cipher", text="Please enter cipher code:")

    # Если пользователь не нажал "Cancel"
    if cipher_code is not None:
        # Используем полученный код
        pyautogui.alert(f"Cipher code entered: {cipher_code}")
        matches = re.findall(r'dash|dot|—|•|–|\.|_|-', cipher_code)

        # Соединим их в строку с пробелами
        result = ' '.join(matches)

        print(result)

        result = ["dash" if char in ['_', '—', '–', '-', 'dash'] else "dot" for char in matches]

        print(result)
        return result
    else:
        pyautogui.alert("No cipher code entered.")
        return None


def open_icon_cipher_Hamster(region=region, confidence=0.9, interval=1):
    try:
        if (button := pyautogui.locateOnScreen(img_Cipher, confidence=confidence, region=region)):
            pyautogui.rightClick(button)
            time.sleep(interval)
            return True

    except pyautogui.PyAutoGUIException as e:
        print(f"Ошибка при обработке {img_Cipher}: {e}")


def clicks_chipher_Hamster(cipher_code, img_Cipher_Red, img_Blue, region=region, confidence=0.95, interval=0.5):
    try:
        if (button := pyautogui.locateOnScreen(img_Cipher_Red, confidence=confidence, region=region)):
            # button_center = pyautogui.center(button)
            for code in cipher_code:
                symbols = code.split(", ")
                for symbol in symbols:
                    print(symbol)
                    match symbol:
                        case "dot":
                            time.sleep(interval // 2)  # Перерывать 0.25 секунду
                            pyautogui.rightClick(button)
                            time.sleep(interval // 2)  # Перерывать 0.25 секунду
                        case "dash":
                            time.sleep(interval // 2)  # Перерывать 0.25 секунду
                            # Придержать нажатие
                            pyautogui.mouseDown(button)
                            time.sleep(interval * 2)  # Удерживать нажатие 1 секунду
                            pyautogui.mouseUp()
                            time.sleep(interval // 2)  # Перерывать 0.25 секунду
                    # time.sleep(interval)
                time.sleep(interval * 2)
            return True
    except pyautogui.PyAutoGUIException as e:
        print(f"Ошибка при кликах по коду {cipher_code}: {e}")


def get_coin(img_Cipher_Coin, region=region, confidence=0.75):
    try:
        time.sleep(10)
        if (button := pyautogui.locateOnScreen(img_Cipher_Coin,region=region, confidence=confidence)):
            pyautogui.click(button)
            print("+1 000 000")
            return True
    except pyautogui.PyAutoGUIException as e:
        print(f"Ошибка при получении coins: {e}")


def main_cipher_Hamster():
    if (cipher_code := get_iform_cipher_Hamster() or manual_input()):
        print(cipher_code)
        if open_icon_cipher_Hamster():
            if (clicks_chipher_Hamster(cipher_code, img_Cipher_Red, img_Blue) or open_icon_cipher_Hamster() and clicks_chipher_Hamster(cipher_code, img_Cipher_Red, img_Blue)):
                if (get_coin(img_Cipher_Coin)):
                    print('\033[32m Success with Hamster cipher \033[0m')

                    open_icon_cipher_Hamster()
                    return True
            # else:
            #     if open_icon_cipher_Hamster():
            #         if (clicks_chipher_Hamster(cipher_code, img_Cipher_Red, img_Blue)):
            #             if (get_coin(img_Cipher_Coin)):
            #                 print('\033[32m Success with Hamster cipher \033[0m')
            #
            #                 open_icon_cipher_Hamster()
            #                 return True


if __name__ == "__main__":
    main_cipher_Hamster()
    # pyautogui.alert("Cipher Hamster has been started!")

    """link = f"https://sumorb.com/crypto/hamster-kombat-daily-cipher-and-combo-code-for-{day}-{month}-2024/"
    response = requests.get(link)

    if response.status_code == 200:
        # Обработка первой ссылки
        soup = BeautifulSoup(response.content, "html.parser")
        # Парсинг данных...
    elif response.status_code != 200:
        # Переход ко второй ссылке, если первая не сработала
        link1 = f"https://hindijankaripur.com/hamster-kombat-daily-cipher-{month}-{day}/"
        response = requests.get(link1)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            morse_codes = soup.find_all()  # Укажите нужные параметры для поиска
        else:
            print("Failed to retrieve the webpage from both links.")"""
