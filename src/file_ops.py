import os
import re
import shutil
from datetime import datetime
from pathlib import Path

SHORT_SUFFIX_PATTERN = re.compile(r'^(.+)_(\d{1,2})$')

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


def clean_filename(name: str) -> str:
    name = transliterate(name)
    name = name.replace('(', '_').replace(')', '_')
    name = name.replace(' ', '_')
    for char in '<>:"/\\|?*&%#!':
        name = name.replace(char, "_")
    name = name.strip("._ ")
    name = re.sub(r'_+', '_', name)
    return name.lower()


def strip_all_suffixes(stem: str) -> str:
    while True:
        match = SHORT_SUFFIX_PATTERN.match(stem)
        if match:
            stem = match.group(1)
        else:
            break
    return stem


def build_filename(original_stem: str, date_prefix: str, ext: str) -> str:
    stem = strip_all_suffixes(original_stem)
    stem = clean_filename(stem)
    stem = f"{date_prefix}_{stem}"
    stem = deduplicate_parts(stem)
    return f"{stem}{ext}"


def find_free_name(directory: str, base: str, ext: str, current_name: str = None) -> str:
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


def sanitize_filename(name: str) -> str:
    return clean_filename(strip_all_suffixes(name))


def move_to_dir(filepath: str, dest_dir: str, new_name: str = None) -> str:
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
    year_dir = date_taken.strftime("%Y")
    month_dir = date_taken.strftime("%m")
    day_dir = date_taken.strftime("%d")
    return os.path.join(target_dir, year_dir, month_dir, day_dir)


def remove_empty_dirs(path: str) -> int:
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


def count_files(target_dir: str) -> int:
    total = 0
    for _, _, files in os.walk(target_dir):
        total += len(files)
    return total
