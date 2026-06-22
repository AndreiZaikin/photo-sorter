import os
import re
from pathlib import Path

# ========== НАСТРОЙКА ==========
TARGET_DIR = r"Z:\PHOTO"
# ==============================

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

# Суффикс: _число из 1-2 цифр в конце имени
SHORT_SUFFIX_PATTERN = re.compile(r'^(.+)_(\d{1,2})$')


def transliterate(name: str) -> str:
    result = []
    for char in name:
        result.append(RU_TO_EN.get(char, char))
    return ''.join(result)


def deduplicate_parts(name: str) -> str:
    parts = name.split('_')
    seen = []
    for part in parts:
        if part not in seen:
            seen.append(part)
    return '_'.join(seen)


def clean_name(name: str) -> str:
    name = transliterate(name)
    name = name.replace('(', '_').replace(')', '_')
    name = name.replace(' ', '_')

    invalid_chars = '<>:"/\\|?*&%#!'
    for char in invalid_chars:
        name = name.replace(char, "_")

    name = name.strip("._ ")
    name = re.sub(r'_+', '_', name)
    name = deduplicate_parts(name)
    name = name.lower()
    return name


def strip_all_suffixes(stem: str) -> str:
    while True:
        match = SHORT_SUFFIX_PATTERN.match(stem)
        if match:
            stem = match.group(1)
        else:
            break
    return stem


def find_free_name(directory: str, base: str, ext: str, current_name: str = None) -> str:
    """
    Находит минимальное свободное имя base_N.ext.
    Если current_name уже имеет минимальный номер — возвращает его же.
    """
    counter = 1
    while True:
        candidate = f"{base}_{counter}{ext}"
        if candidate == current_name:
            for smaller in range(1, counter):
                smaller_candidate = f"{base}_{smaller}{ext}"
                if not os.path.exists(os.path.join(directory, smaller_candidate)):
                    return smaller_candidate
            return candidate
        if not os.path.exists(os.path.join(directory, candidate)):
            return candidate
        counter += 1


def count_files(target_dir: str) -> int:
    """Считает общее количество файлов во всех подпапках."""
    total = 0
    for _, _, files in os.walk(target_dir):
        total += len(files)
    return total


def process_directory(target_dir: str) -> None:
    if not os.path.exists(target_dir):
        print(f"Ошибка: папка '{target_dir}' не найдена!")
        return

    stats = {'total': 0, 'renamed': 0, 'skipped': 0, 'errors': 0}

    print(f"Сканирую: {target_dir}")
    total_files = count_files(target_dir)
    print(f"Найдено файлов: {total_files}\n")

    for root, _, files in os.walk(target_dir):
        for filename in files:
            stats['total'] += 1

            # Прогресс: выводим поверх текущей строки
            percent = stats['total'] / total_files * 100 if total_files else 0
            print(f"\rПрогресс: {stats['total']}/{total_files} ({percent:.1f}%)", end="", flush=True)

            stem = Path(filename).stem
            ext = Path(filename).suffix.lower()

            clean_stem = clean_name(stem)
            base = strip_all_suffixes(clean_stem)
            target_filename = f"{base}{ext}"

            if target_filename == filename:
                stats['skipped'] += 1
                continue

            if target_filename.lower() == filename.lower():
                old_path = os.path.join(root, filename)
                new_path = os.path.join(root, target_filename)
                try:
                    os.rename(old_path, new_path)
                    stats['renamed'] += 1
                except OSError as e:
                    stats['errors'] += 1
                continue

            if not os.path.exists(os.path.join(root, target_filename)):
                old_path = os.path.join(root, filename)
                new_path = os.path.join(root, target_filename)
                try:
                    os.rename(old_path, new_path)
                    stats['renamed'] += 1
                except OSError as e:
                    stats['errors'] += 1
                continue

            final_filename = find_free_name(root, base, ext, filename)

            if final_filename == filename:
                stats['skipped'] += 1
                continue

            old_path = os.path.join(root, filename)
            new_path = os.path.join(root, final_filename)

            try:
                os.rename(old_path, new_path)
                stats['renamed'] += 1
            except OSError as e:
                stats['errors'] += 1

    # Переход на новую строку после прогресс-бара
    print()

    print(f"\n{'=' * 40}")
    print(f"  Всего проверено: {stats['total']}")
    print(f"  Переименовано:   {stats['renamed']}")
    print(f"  Пропущено:       {stats['skipped']}")
    print(f"  Ошибок:          {stats['errors']}")
    print(f"{'=' * 40}")


if __name__ == "__main__":
    process_directory(TARGET_DIR)
