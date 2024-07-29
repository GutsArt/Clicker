import pyautogui

from config import *
def on_press(key):
    if key == toggle_key:
        x, y = pyautogui.position()
        print(f'X: {x}, Y: {y}')
    elif key == exit_key:
        print('Exiting...')
        return False  # Останавливаем listener


def main():
    # Запускаем listener клавиатуры
    with Listener(on_press=on_press) as listener:
        listener.join()


if __name__ == '__main__':
    main()