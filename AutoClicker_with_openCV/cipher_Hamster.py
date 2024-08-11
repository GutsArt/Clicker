import pyautogui
import time
import requests
from bs4 import BeautifulSoup
from config import *

img_Cipher = r"SCREENS\screenCipher.png"
img_Cipher_Red = r"SCREENS\screenCipherRed.png"
img_Cipher_Coin = r"SCREENS\screenCipherGetCoins.png"

img_Blue = r"SCREENS\ScreenBlue.png"


def get_iform_cipher_Hamster():
    from datetime import datetime
    now = datetime.now()
    day = now.day
    month = now.strftime("%B").lower()
    link = f"https://sumorb.com/crypto/hamster-kombat-daily-cipher-and-combo-code-for-{day}-{month}-2024/"
    print(link)
    response = requests.get(link)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        # Parse the page to extract the cipher and combo code
        # This is a placeholder, you need to replace it with the actual HTML structure

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


def open_icon_cipher_Hamster(region=region, confidence=0.95, interval=1):
    try:
        if (button := pyautogui.locateOnScreen(img_Cipher, confidence=confidence, region=region)):
            pyautogui.rightClick(button)
            time.sleep(interval)
            return True

    except pyautogui.PyAutoGUIException as e:
        print(f"Ошибка при обработке {img_Cipher}: {e}")


def clicks_chipher_Hamster(cipher_code, img_Cipher_Red, img_Blue, region=region, confidence=0.95, interval=0.1):
    try:
        if (button := pyautogui.locateOnScreen(img_Cipher_Red, confidence=confidence, region=region)):
            button_center = pyautogui.center(button)
            for code in cipher_code:
                symbols = code.split(", ")
                for symbol in symbols:
                    match symbol:
                        case "dot":
                            pyautogui.rightClick(button_center)
                        case "dash":
                            # Придержать нажатие
                            pyautogui.mouseDown(button_center)
                            time.sleep(1)  # Удерживать нажатие 1 секунду
                            pyautogui.mouseUp()
                    time.sleep(interval)
                time.sleep(interval * 2)
            return True
    except pyautogui.PyAutoGUIException as e:
        print(f"Ошибка при кликах по коду {cipher_code}: {e}")


def get_coin(img_Cipher_Coin, region=region, confidence=0.75):
    try:
        if (button := pyautogui.locateOnScreen(img_Cipher_Coin, confidence=confidence)):
            pyautogui.click(button)
            print("+1 000 000")
            return True
    except pyautogui.PyAutoGUIException as e:
        print(f"Ошибка при получении coins: {e}")


def main_cipher_Hamster():
    if (cipher_code := get_iform_cipher_Hamster()):
        print(cipher_code)
        if open_icon_cipher_Hamster():
            if (clicks_chipher_Hamster(cipher_code, img_Cipher_Red, img_Blue)):
                if (get_coin(img_Cipher_Coin)):
                    print('\033[32m Success with Hamster cipher \033[0m')

                    open_icon_cipher_Hamster()
                    return True
            else:
                if open_icon_cipher_Hamster():
                    if (clicks_chipher_Hamster(cipher_code, img_Cipher_Red, img_Blue)):
                        if (get_coin(img_Cipher_Coin)):
                            print('\033[32m Success with Hamster cipher \033[0m')

                            open_icon_cipher_Hamster()
                            return True


if __name__ == "__main__":
    main_cipher_Hamster()
    # pyautogui.alert("Cipher Hamster has been started!")
