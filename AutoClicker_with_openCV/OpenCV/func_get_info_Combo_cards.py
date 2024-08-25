import cv2
import pytesseract
import pyautogui
from matplotlib import pyplot as plt
import numpy as np
import re
import json
from datetime import datetime
import threading
from pynput import keyboard

from config import *

# Укажите путь к Tesseract OCR, если он не находится в системном пути
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\artem\AppData\Local\Programs\Tesseract-OCR\tesseract'


def find_image(img_path, region=region, confidence=0.9):
    try:
        sleep(sleep_time)
        if (button := pyautogui.locateOnScreen(img_path, region=region, confidence=confidence)):
            pyautogui.click(button, button='right')
            print(f"Клик выполнен для {img_path}.")
            return True
        else:
            print(f"Изображение {img_path} не найдено на экране.")
    except pyautogui.PyAutoGUIException as e:
        print(f"Ошибка при обработке {img_path}: {e}")


def press_down(number_down):
    find_image("Hamster Kombat.png")
    for _ in range(number_down):
        pyautogui.press('down')
        sleep(0.1)


def press_up(number_up):
    find_image("Hamster Kombat.png")
    for _ in range(number_up):
        pyautogui.press('up')
        sleep(0.1)


def get_price(region):
    try:
        sleep(sleep_time)
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
        "efficiency": f"{(int(plus_number) * 100) / int(price_number):.5f}" if price_number != 0 else None
    }

    with open(json_filename, 'w') as file:
        json.dump(data, file, indent=2)


def sleep(time):
    pyautogui.sleep(time)


def process_image(img_path, max_attempts=10):
    attempts = 0
    while attempts < max_attempts:
        result = find_image(img_path)
        if result:
            print(f"Изображение найдено в позиции: {result}")
            # Определяем область для поиска цены
            x1, y1 = 1770, 900
            x2, y2 = 1860, 1000
            region_money = (x1, y1, x2 - x1, y2 - y1)
            price_text = get_price(region_money)
            # print(f"\033[91m{price_text}\033[0m")
            # print(f"Тип данных: {type(price_text)}")
            if len(price_text) < 2:
                print(f"Не удалось распознать цену для {img_path}. Пропускаем этот элемент.")
                sleep(sleep_time * 10)
                price_text = get_price(region_money)
                if len(price_text) < 2:
                    break
                find_image("BACK.png")

            plus_number, price_number = extract_numbers(price_text)

            if plus_number is None and price_number is None:
                print(f"Не удалось извлечь числа из текста: {price_text}. Пропускаем этот элемент.")
                find_image("BACK.png")
                break

            if not create_json("PR&Team.json", img_path, plus_number, price_number):
                find_image("BACK.png")
                break

            find_image("BACK.png")
            break  # Выходим из цикла, если изображение найдено
        else:
            print(f"Изображение не найдено, попытка {attempts + 1}/{max_attempts}. Прокручиваем вниз...")
            press_down(5)
            sleep(sleep_time)
            attempts += 1

    if attempts == max_attempts:
        find_image("PR&Team.png")
        print(f"Не удалось найти изображение {img_path} после {max_attempts} попыток.")
        sleep(sleep_time * 10)


# def find_best_efficiency(my_coins):
#     try:
#         # Преобразуем доступные монеты в целое число, если они не в формате числа
#         my_coins = int(my_coins)
#
#         with open("PR&Team.json", 'r') as file:
#             data = json.load(file)
#             best_efficiency = 0
#             best_image = None
#             best_price = None
#
#             for img_path, values in data["PR&Team"].items():
#                 try:
#                     efficiency = float(values["efficiency"])
#                     price = int(values["price"])  # Преобразуем цену в целое число
#
#                     if efficiency > best_efficiency and price <= my_coins:
#                         best_efficiency = efficiency
#                         best_image = img_path
#                         best_price = price
#                 except ValueError:
#                     print(f"Невозможно преобразовать цену в целое число для {img_path}: {values['price']}")
#                     continue  # Пропускаем итерацию, если цена не является числом
#
#             if best_image:
#                 remaining_coins = my_coins - best_price
#                 print(f"Лучшее изображение: {best_image} с эффективностью: {best_efficiency}")
#                 print(f"Цена: {best_price}, оставшиеся монеты: {remaining_coins}")
#                 return best_image, remaining_coins
#             else:
#                 print("Не найдено изображение с наилучшей эффективностью в пределах доступных монет.")
#                 return None, my_coins
#     except Exception as e:
#         print(f"Ошибка при поиске лучшей эффективности: {str(e)}")
#         return None, my_coins


def find_best_efficiency(my_coins, top_n=10):
    try:
        # Преобразуем доступные монеты в целое число, если они не в формате числа
        my_coins = int(my_coins)

        with open("PR&Team.json", 'r') as file:
            data = json.load(file)
            efficiencies = []

            for img_path, values in data["PR&Team"].items():
                try:
                    efficiency = float(values["efficiency"])
                    price = int(values["price"])  # Преобразуем цену в целое число

                    if price <= my_coins:
                        efficiencies.append((img_path, efficiency, price))
                except ValueError:
                    print(f"Невозможно преобразовать цену в целое число для {img_path}")

            # Сортируем по эффективности в порядке убывания и берем топ N
            top_efficiencies = sorted(efficiencies, key=lambda x: x[1], reverse=True)[:top_n]

            for img_path, efficiency, price in top_efficiencies:
                print(f"Изображение: {img_path}, Эффективность: {efficiency}, Цена: {price}")

        print(top_efficiencies)

        return top_efficiencies
    except Exception as e:
        print(f"Ошибка: {str(e)}")
        return None


def smart_find(best_img, max_attempts=11, attempts=0):
    while attempts < max_attempts:
        if find_image(best_img):
            break
        press_down(5)
        attempts += 1
    if attempts == max_attempts:
        print("Изображение не найдено после 11 попыток")
        return None
    else:
        return True

def main():
    try:
        if not find_image("MINING.png"):
            print("Не удалось найти изображение MINING.png, завершение работы.")
        while CLICKING:
            if not find_image("PR&Team.png"):
                print("Не удалось найти изображение PR&Team.png, завершение работы.")
                break

            press_up(50)

            sleep(1)

            x, y = 1770, 895
            x1, y1 = 1875, 920
            my_coins = get_price((x, y, x1 - x, y1 - y))
            print(f"Текущий баланс монет: {my_coins}")
            if not my_coins:
                break

            if int(my_coins) <= 1_000_000:
                break

            if not find_image("PR&Team.png"):
                print("Не удалось найти изображение PR&Team.png, завершение работы.")
                break

            # for img_path in imgs:
            #     process_image(img_path)
            #
            # if not find_image("PR&Team.png"):
            #     print("Не удалось найти изображение PR&Team.png, завершение работы.")
            #     break

            sleep(sleep_time * 2)

            # best_img, remaining_money = find_best_efficiency(my_coins)
            best_images = find_best_efficiency(my_coins)
            for best_img, efficiency, price in best_images:
                if best_img:
                    find_image("PR&Team.png")

                    if not smart_find(best_img):
                        print(f"Не удалось найти изображение |{best_img}|, пробуем следующее.")
                        continue  # Переходим к следующему изображению

                    if not find_image("GET.png"):
                        print("Не удалось найти изображение GET.png, завершение работы.")
                        break

                    x1, y1 = 1770, 900
                    x2, y2 = 1860, 1000
                    region_money = (x1, y1, x2 - x1, y2 - y1)
                    price_text = get_price(region_money)
                    if len(price_text) < 2:
                        print(f"Не удалось распознать цену для {best_img}. Пропускаем этот элемент.")
                        sleep(sleep_time * 10)
                        price_text = get_price(region_money)
                        if len(price_text) < 2:
                            break
                        find_image("BACK.png")

                    plus_number, price_number = extract_numbers(price_text)

                    if plus_number is None and price_number is None:
                        print(f"Не удалось извлечь числа из текста: {price_text}. Пропускаем этот элемент.")
                        find_image("BACK.png")
                        break

                    if not create_json("PR&Team.json", best_img, plus_number, price_number):
                        find_image("BACK.png")
                        break

                    find_image("BACK.png")

                    remaining_money = my_coins - price
                    if remaining_money <= 1_000_000:
                        print("Достаточно денег для завершения работы.")
                        break
                    else:
                        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Money: {remaining_money}")
                        sleep(sleep_time * 60)

        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    except Exception as e:
        print(f"Ошибка при работе с изображениями: {str(e)}")
    finally:
        sleep(sleep_time * 60)
        main()


def on_press(key):
    global CLICKING, exit_flag
    if key == toggle_key:
        CLICKING = not CLICKING
        print(f"Автоклик {'включен' if CLICKING else 'выключен'}.")
        if CLICKING:
            threading.Thread(target=main).start()
    elif key == exit_key:
        exit_flag = True
        return False


def listen_keyboard():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()


if __name__ == "__main__":
    listen_keyboard()
