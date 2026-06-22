import os
import re
import shutil
from datetime import datetime
from pathlib import Path

SORTED_PATTERN = re.compile(r'^\d{8}_\d{6}_')

# Таблица транслитерации русских букв в латинские
RU_TO_EN = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
    'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
    'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
    'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
    'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
    'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'Yo',
    'Ж': 'Zh', 'З': 'Z', 'И': 'I', 'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M',
    'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U',
    'Ф': 'F', 'Х': 'Kh', 'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Sch',
    'Ъ': '', 'Ы': 'Y', 'Ь': '', 'Э': 'E', 'Ю': 'Yu', 'Я': 'Ya',
}


def transliterate(name: str) -> str:
    """Заменяет русские буквы на латинские."""
    result = []
    for char in name:
        result.append(RU_TO_EN.get(char, char))
    return ''.join(result)


def sanitize_filename(name: str) -> str:
    """
    Очищает имя файла:
    - транслитерирует русские буквы в латинские
    - заменяет недопустимые в Windows символы на подчёркивание
    - убирает точки и пробелы в начале и конце
    """
    # Сначала транслитерация
    name = transliterate(name)

    # Замена недопустимых символов
    invalid_chars = '<>:"/\\|?*&%#!'
    for char in invalid_chars:
        name = name.replace(char, "_")

    # Убираем пробелы и точки по краям
    name = name.strip(". ")

    # Убираем множественные подчёркивания
    name = re.sub(r'_+', '_', name)

    return name


def is_already_sorted(filename: str) -> bool:
    """Проверяет, начинается ли имя файла с префикса даты."""
    return bool(SORTED_PATTERN.match(filename))


def move_to_dir(filepath: str, dest_dir: str, new_name: str = None) -> str:
    """Перемещает файл в указанную папку, разрешая конфликты имён."""
    os.makedirs(dest_dir, exist_ok=True)

    if new_name is None:
        new_name = os.path.basename(filepath)

    dest_path = os.path.join(dest_dir, new_name)
    counter = 1
    stem = Path(new_name).stem
    ext = Path(new_name).suffix

    while os.path.exists(dest_path):
        new_name = f"{stem}_{counter}{ext}"
        dest_path = os.path.join(dest_dir, new_name)
        counter += 1

    shutil.move(filepath, dest_path)
    return dest_path


def get_dest_subdir(target_dir: str, date_taken: datetime) -> str:
    """Возвращает путь Год/Месяц/Число внутри target_dir."""
    year_dir = date_taken.strftime("%Y")
    month_dir = date_taken.strftime("%m")
    day_dir = date_taken.strftime("%d")
    return os.path.join(target_dir, year_dir, month_dir, day_dir)


def remove_empty_dirs(path: str) -> int:
    """Рекурсивно удаляет пустые папки."""
    removed = 0
    for root, dirs, _ in os.walk(path, topdown=False):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            try:
                if not os.listdir(dir_path):
                    os.rmdir(dir_path)
                    removed += 1
            except OSError:
                pass
    return removed
