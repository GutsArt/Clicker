import cv2
import pytesseract
import pyautogui
from matplotlib import pyplot as plt
import numpy as np
import re
import json

from config import *

# Укажите путь к Tesseract OCR, если он не находится в системном пути
pytesseract.pytesseract.tesseract_cmd = 'tesseract'


def find_image(img_path, region=region, confidence=0.9):
    try:
        if (button := pyautogui.locateOnScreen(img_path, region=region, confidence=confidence)):
            pyautogui.click(button, button='right')
            print(f"Клик выполнен для {img_path}.")
            pyautogui.sleep(sleep_time)
            return True
        else:
            print(f"Изображение {img_path} не найдено на экране.")
    except pyautogui.PyAutoGUIException as e:
        print(f"Ошибка при обработке {img_path}: {e}")


def get_price(region):
    try:
        screenshot = pyautogui.screenshot(region=region)
        img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        # Проверяем, удалось ли загрузить изображение

        # Увеличиваем качество изображения в 4 раза
        scale_factor = 2
        width = int(img.shape[1] * scale_factor)
        height = int(img.shape[0] * scale_factor)
        dim = (width, height)
        img = cv2.resize(img, dim, interpolation=cv2.INTER_CUBIC)

        # Преобразуем изображение в RGB
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Определяем диапазон желтого цвета в RGB
        # lower_yellow = np.array([200, 150, 0])
        # upper_yellow = np.array([255, 255, 200])
        lower_yellow = np.array([175, 150, 0])
        upper_yellow = np.array([255, 255, 195])

        # Создаем маску для желтого цвета
        mask = cv2.inRange(img_rgb, lower_yellow, upper_yellow)

        # Инвертируем маску, чтобы оставить все, кроме желтого
        mask_inv = cv2.bitwise_not(mask)

        # Применяем инвертированную маску к оригинальному изображению
        img_no_yellow = cv2.bitwise_and(img_rgb, img_rgb, mask=mask_inv)

        # Увеличиваем качество изображения в 4 раза
        scale_factor = 2
        width = int(img_no_yellow.shape[1] * scale_factor)
        height = int(img_no_yellow.shape[0] * scale_factor)
        dim = (width, height)
        img_no_yellow_high_res = cv2.resize(img_no_yellow, dim, interpolation=cv2.INTER_CUBIC)

        # Преобразуем изображение в оттенки серого
        gray_img = cv2.cvtColor(img_no_yellow_high_res, cv2.COLOR_RGB2GRAY)

        # Применяем фильтр для уменьшения шума
        img_filtered = cv2.bilateralFilter(gray_img, 11, 15, 15)

        # Применяем пороговое значение (бинаризация)
        _, thresh = cv2.threshold(img_filtered, 160, 255, cv2.THRESH_BINARY_INV)

        # Используем Tesseract для распознавания текста
        config = '--psm 6 -c tessedit_char_whitelist=0123456789+'
        text = pytesseract.image_to_string(thresh, config=config)

        # # Отображаем исходное изображение и результат
        # plt.subplot(1, 3, 1)
        # plt.title("Origin")
        # plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        #
        # plt.subplot(1, 3, 2)
        # plt.title("Изображение без желтого цвета")
        # plt.imshow(cv2.cvtColor(img_no_yellow, cv2.COLOR_BGR2RGB))
        #
        # plt.subplot(1, 3, 3)
        # plt.title("Фильтрованное изображение")
        # plt.imshow(cv2.cvtColor(thresh, cv2.COLOR_BGR2RGB))
        #
        # # Показ изображений
        # plt.show()

        # Вывод распознанного текста
        print("Распознанный текст:")
        print(text)

        return text.strip()
    except Exception as e:
        print(f"Ошибка: {str(e)}")
        return None


def extract_numbers(text):
    # Находим все числа в тексте
    numbers = re.findall(r'\d+', text)

    # Проверяем, есть ли знак +
    plus_number = None
    remaining_number = None

    # Ищем число после знака +
    if '+' in text:
        plus_number_match = re.search(r'\+(\d+)', text)
        if plus_number_match:
            plus_number = plus_number_match.group(1)

    # Если есть найденные числа, берем последнее число
    if numbers:
        remaining_number = numbers[-1]

    return plus_number, remaining_number


def create_json(json_filename, img_path, plus_number, price_number):
    try:
        with open(json_filename, 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    # Обновляем данные или создаем новую запись
    if "PR&Team" not in data:
        data["PR&Team"] = {}

    data["PR&Team"][img_path] = {
        "profit": f"+{plus_number}" if plus_number else None,
        "price": f"{price_number}" if price_number else None,
        "efficiency": f"{int(plus_number) / int(price_number):.5f}" if price_number != 0 else None
    }

    with open(json_filename, 'w') as file:
        json.dump(data, file, indent=2)


sleep_time = 2


def process_image(img_path, max_attempts=3):
    attempts = 0
    while attempts < max_attempts:
        result = find_image(img_path)
        if result:
            print(f"Изображение найдено в позиции: {result}")
            # Определяем область для поиска цены
            x1, y1 = 1780, 900
            x2, y2 = 1855, 1000
            region_money = (x1, y1, x2 - x1, y2 - y1)
            plus_number, price_number = extract_numbers(get_price(region_money))

            create_json("PS&Team.json", img_path, plus_number, price_number)

            pyautogui.sleep(sleep_time)
            find_image("BACK.png")
            pyautogui.sleep(sleep_time)
            break  # Выходим из цикла, если изображение найдено
        else:
            print(f"Изображение не найдено, попытка {attempts + 1}/{max_attempts}. Прокручиваем вниз...")
            for _ in range(10):
                pyautogui.press('down')
                pyautogui.sleep(0.1)
            pyautogui.sleep(sleep_time)
            attempts += 1

    if attempts == max_attempts:
        print(f"Не удалось найти изображение {img_path} после {max_attempts} попыток.")


def main():
    find_image("PS&Team.png")
    for img_path in imgs:
        process_image(img_path)


if __name__ == "__main__":
    main()
