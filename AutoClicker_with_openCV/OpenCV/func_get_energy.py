import cv2
import pytesseract
from matplotlib import pyplot as plt

import pyautogui
import numpy as np

# Укажите путь к Tesseract OCR, если он не находится в системном пути
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\artem\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'


def extract_digits_from_screen(region=(1705, 1010, 30, 15)):
    # screenshot = pyautogui.screenshot(region=region)
    # screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    # gray_image = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    # extracted_text = pytesseract.image_to_string(gray_image, config='--psm 6 digits')
    # digits = ''.join(filter(str.isdigit, extracted_text))

    # screenshot = pyautogui.screenshot(region=region)
    # screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    # gray_image = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    #
    # # Применение пороговой обработки для улучшения качества распознавания
    # _, thresh_image = cv2.threshold(gray_image, 150, 255, cv2.THRESH_BINARY_INV)
    #
    # # Использование Tesseract с конфигурацией для распознавания только цифр
    # extracted_text = pytesseract.image_to_string(thresh_image, config='--psm 6 digits')
    # digits = ''.join(filter(str.isdigit, extracted_text))

    screenshot = pyautogui.screenshot('SCREEN_ENERGY.png', region=region)
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    gray_image = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # Увеличение изображения для лучшего распознавания
    gray_image = cv2.resize(gray_image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    # Применение пороговой обработки
    _, thresh_image = cv2.threshold(gray_image, 125, 255, cv2.THRESH_BINARY_INV)

    cv2.imwrite('thresh_image.png', thresh_image)

    # Применение Tesseract
    extracted_text = pytesseract.image_to_string(thresh_image, config='--psm 6 digits')
    digits = ''.join(filter(str.isdigit, extracted_text))
    print(f"Энергия: {digits}")

    # digits = extracted_text
    # print(f"Энергия: {digits}")
    return int(digits) if digits.isdigit() else 0


energy = extract_digits_from_screen()

print(f"Energy: {energy}")
