def transform_path(file_path):
    # Разделяем путь по разделителю папок
    parts = file_path.split('\\')

    # Убираем имя файла и оставляем только путь до папки
    folder_name = parts[-2]
    print(folder_name)

    # Формируем новый путь, добавляя `.png` к имени папки
    new_path = '\\'.join(parts[:-2]) + '\\' + folder_name + '.png'

    return new_path


def transform_paths(paths):
    return [transform_path(path) for path in paths]


# Пример использования
best_img = ["SCREENS\\Specials\\Telegram Miniapp Launch.png",
            "SCREENS\\Legal\\Telegram Miniapp Launch.png",
            r"SCREENS\PR&Team\Partnership program.png",
            r"SCREENS\Markets\Fan tokens.png",
            r"SCREENS\Web3\DEX.png"]
transformed_img = transform_paths(best_img)
print(transformed_img)

"""
['SCREENS\\Specials.png']
Legal
['SCREENS\\Legal.png']
PR&Team
['SCREENS&Team\\PR&Team.png']
Markets
['SCREENS\\Markets.png']
Web3
['SCREENS\\Web3.png']
"""
