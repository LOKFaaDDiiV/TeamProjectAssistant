import re
import sys
import os
import shutil
from pathlib import Path


class SomeField:
    """Клас для загальних змінних"""
    root_str_path = None
    path = None
    known_formats = set()
    unknown_formats = set()


def main_function(some_path):
    """
    Створює потрібні папки. Якщо вони вже існують, то помилки не виникає.
    Викликає рекурсивну функцію для знаходження всіх нащадків.
    Повертає строку з відомими та невідомими форматами
    """
    for k in suffix.keys():
        try:
            os.mkdir(os.path.join(some_path, k))
        except FileExistsError:
            continue

    listdirs(some_path)
    return f"Known formats:\n" \
           f"<{', '.join(some_field.known_formats) if bool(some_field.known_formats) else 'No known formats'}>\n" \
           f"Unknown formats:\n" \
           f"<{', '.join(some_field.unknown_formats) if bool(some_field.unknown_formats) else 'No unknown formats'}>"


def listdirs(rootdir):
    """
    Рекурсивна функція.
    Якщо знаходить папку, то перебирає всіх її нащадків.
    До файлів застосовує функцію переміщення
    """
    for list_path in rootdir.iterdir():
        if list_path.is_dir():
            is_not_dir = False

            for k in suffix.keys():
                if list_path.name == k:
                    is_not_dir = True

            if is_not_dir:
                continue

            listdirs(Path(list_path))
        else:
            move_and_rename(list_path)

    if rootdir != some_field.path:
        os.rmdir(rootdir)


def normalize(name):
    """Нормалізує ім'я файлу"""
    name_obj = Path(name)
    cyrillic_symbols = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    translation = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t",
                   "u", "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
    cyrillic_codes = []
    for char in cyrillic_symbols:
        cyrillic_codes.append(ord(char))
    trans = dict(zip(cyrillic_codes, translation))
    trans.update({ord(chr(c).upper()): l.upper() for c, l in trans.items()})
    clean_name = re.sub(name_obj.suffix, '', name_obj.name)
    new_name = clean_name.translate(trans)
    return re.sub("[^a-zA-Z0-9]", "_", new_name)


def move_and_rename(string_path):
    """Переміщує та перейменовує файл (враховуючи можливість існування декількох файлів з однаковим іменем)"""
    string_path_obj = Path(string_path)
    is_known_formats = False
    for k, v in suffix.items():
        if v.find(string_path_obj.suffix) != -1:
            new_location = os.path.join(some_field.root_str_path, k)
            new_path = os.path.join(new_location, normalize(string_path_obj.name) + string_path_obj.suffix)

            if os.path.exists(new_path):
                num = 1
                while True:
                    new_path = os.path.join(new_location,
                                            normalize(string_path_obj.name) + f"-copy{num}" + string_path_obj.suffix)

                    if not os.path.exists(new_path):
                        break
                    num += 1

            shutil.move(str(string_path_obj), new_path)  # Переміщуємо файл

            if k == "archives":
                unpack_archive(new_path)

            some_field.known_formats.add(string_path_obj.suffix[1:])
            is_known_formats = True
            break

    if not is_known_formats:
        new_location = os.path.join(some_field.root_str_path, "other")
        new_path = os.path.join(new_location, normalize(string_path_obj.name) + string_path_obj.suffix)

        if os.path.exists(new_path):
            num = 1
            while True:
                new_path = os.path.join(new_location,
                                        normalize(string_path_obj.name) + f"-copy{num}" + string_path_obj.suffix)

                if not os.path.exists(new_path):
                    break
                num += 1

        shutil.move(str(string_path_obj), new_path)  # Переміщуємо файл

        some_field.unknown_formats.add(string_path_obj.suffix[1:])


def unpack_archive(archive_location_string_path):
    """Розпаковує архів у папку з ідентичною назвою і видаляє його"""
    obj_path = Path(archive_location_string_path)
    folder = re.sub(obj_path.suffix, '', archive_location_string_path)
    os.mkdir(folder)
    shutil.unpack_archive(archive_location_string_path, folder)
    os.remove(archive_location_string_path)


def main():
    print('Load complete\n')
    print("\nEnter path or 'back' to go back:")
    is_back = False
    while True:
        some_field.root_str_path = input('>>>').strip()
        if some_field.root_str_path == 'back':
            if __name__ == "__main__":
                sys.exit("Good bye!")
            print("Returning to program selection...")
            is_back = True
            break
        elif some_field.root_str_path == '':
            print("\nYou have entered the wrong folder path. Try again or enter the 'back' key to exit this program")
            continue

        try:
            some_field.path = Path(some_field.root_str_path)
            if len(os.listdir(some_field.path)) == 0:
                print("\nThis folder is empty. Try again or enter the 'back' key to exit this program")
                continue
            break
        except (IndexError, FileNotFoundError, OSError):
            print("\nYou have entered the wrong folder path. Try again or enter the 'back' key to exit this program")
            continue

    if not is_back:
        print(main_function(some_field.path))

        if __name__ == "__main__":
            input("Sorting successfully completed! (Press 'Enter' key to exit)")
            sys.exit("Good bye!")

        print("Sorting successfully completed!\nReturning to program selection...")


suffix = {
    "images": '.jpeg .png .jpg .svg',
    "video": '.avi .mp4 .mov .mkv',
    "documents": '.doc .docx .txt .pdf .xlsx .pptx',
    "audio": '.mp3 .ogg .wav .amr',
    "archives": '.zip .gz .tar',
    "other": ''
}

some_field = SomeField()

if __name__ == "__main__":
    main()
