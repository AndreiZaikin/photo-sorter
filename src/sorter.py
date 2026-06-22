import os
from pathlib import Path

from src.config import PHOTO_EXTENSIONS, VIDEO_EXTENSIONS
from duplicates import is_duplicate
from exif_reader import get_date_taken
from file_ops import sanitize_filename, is_already_sorted, move_to_dir, get_dest_subdir, remove_empty_dirs


def process_file(filepath: str, target_dir: str, duplicates_dir: str, is_video: bool = False) -> tuple[str, str]:
    """
    Обрабатывает один файл.
    Возвращает (статус, путь): 'sorted', 'na', 'duplicate', 'skipped'
    """
    original_stem = Path(filepath).stem
    original_ext = Path(filepath).suffix.lower()
    safe_name = sanitize_filename(original_stem)
    already_sorted = is_already_sorted(original_stem)
    date_taken = get_date_taken(filepath, is_video)
    current_dir = os.path.dirname(filepath)

    if is_video:
        dup_base = os.path.join(duplicates_dir, "VIDEO")
    elif original_ext in PHOTO_EXTENSIONS:
        dup_base = os.path.join(duplicates_dir, "PHOTO")
    else:
        dup_base = os.path.join(duplicates_dir, "UNDEFINED")

    # Без даты → NA
    if date_taken is None:
        na_dir = os.path.join(target_dir, "NA")
        new_filename = f"{safe_name}{original_ext}"
        dest_path = os.path.join(na_dir, new_filename)

        if os.path.normpath(filepath) == os.path.normpath(dest_path):
            return ('skipped', filepath)
        if os.path.normpath(current_dir) == os.path.normpath(na_dir):
            return ('skipped', filepath)
        if is_duplicate(filepath, na_dir, new_filename):
            dup_na_dir = os.path.join(dup_base, "NA")
            dest_path = move_to_dir(filepath, dup_na_dir, new_filename)
            return ('duplicate', dest_path)

        dest_path = move_to_dir(filepath, na_dir, new_filename)
        return ('na', dest_path)

    # Есть дата → сортируем
    date_prefix = date_taken.strftime("%Y%m%d_%H%M%S")
    dest_subdir = get_dest_subdir(target_dir, date_taken)

    if already_sorted:
        rest_of_name = original_stem[16:] if len(original_stem) > 16 else original_stem
        safe_rest = sanitize_filename(rest_of_name)
        new_filename = f"{date_prefix}_{safe_rest}{original_ext}" if safe_rest else f"{date_prefix}{original_ext}"
    else:
        new_filename = f"{date_prefix}_{safe_name}{original_ext}"

    dest_path = os.path.join(dest_subdir, new_filename)

    if os.path.normpath(filepath) == os.path.normpath(dest_path):
        return ('skipped', filepath)
    if os.path.normpath(current_dir) == os.path.normpath(dest_subdir):
        os.rename(filepath, dest_path)
        return ('sorted', dest_path)
    if is_duplicate(filepath, dest_subdir, new_filename):
        dup_dest_subdir = os.path.join(
            dup_base,
            date_taken.strftime("%Y"),
            date_taken.strftime("%m"),
            date_taken.strftime("%d")
        )
        dest_path = move_to_dir(filepath, dup_dest_subdir, new_filename)
        return ('duplicate', dest_path)

    dest_path = move_to_dir(filepath, dest_subdir, new_filename)
    return ('sorted', dest_path)


def sort_all(source_dir: str, photo_dir: str, video_dir: str, undefined_dir: str, duplicates_dir: str,
             log_func=None, progress_func=None, stop_flag=None):
    """
    Сортирует все файлы из source_dir.
    log_func(message) — функция для вывода лога.
    progress_func(current, total) — функция для обновления прогресса.
    stop_flag — объект с атрибутом is_set() или None.
    Возвращает словарь со статистикой.
    """
    stats = {
        'photo_sorted': 0, 'photo_na': 0, 'photo_dup': 0, 'photo_skipped': 0,
        'video_sorted': 0, 'video_na': 0, 'video_dup': 0, 'video_skipped': 0,
        'undefined': 0, 'undefined_dup': 0, 'undefined_skipped': 0,
        'total': 0, 'errors': 0
    }

    # Считаем общее количество файлов
    total_files = sum(len(files) for _, _, files in os.walk(source_dir))

    for root, _, files in os.walk(source_dir):
        if stop_flag and stop_flag():
            break

        for filename in files:
            if stop_flag and stop_flag():
                break

            stats['total'] += 1
            if progress_func:
                progress_func(stats['total'], total_files)

            filepath = os.path.join(root, filename)
            ext = Path(filename).suffix.lower()

            is_video = ext in VIDEO_EXTENSIONS
            is_photo = ext in PHOTO_EXTENSIONS and not is_video

            try:
                if is_photo:
                    status, dest = process_file(filepath, photo_dir, duplicates_dir, is_video=False)
                    if status == 'sorted':
                        stats['photo_sorted'] += 1
                    elif status == 'na':
                        stats['photo_na'] += 1
                    elif status == 'duplicate':
                        stats['photo_dup'] += 1
                    elif status == 'skipped':
                        stats['photo_skipped'] += 1
                    if log_func:
                        tag = {'sorted': 'ФОТО', 'na': 'ФОТО/NA', 'duplicate': 'ФОТО/DUP', 'skipped': 'ФОТО/SKIP'}[status]
                        log_func(f"[{tag}] {filename} → {dest}" if status != 'skipped' else f"[{tag}] {filename}")
                elif is_video:
                    status, dest = process_file(filepath, video_dir, duplicates_dir, is_video=True)
                    if status == 'sorted':
                        stats['video_sorted'] += 1
                    elif status == 'na':
                        stats['video_na'] += 1
                    elif status == 'duplicate':
                        stats['video_dup'] += 1
                    elif status == 'skipped':
                        stats['video_skipped'] += 1
                    if log_func:
                        tag = {'sorted': 'ВИДЕО', 'na': 'ВИДЕО/NA', 'duplicate': 'ВИДЕО/DUP', 'skipped': 'ВИДЕО/SKIP'}[status]
                        log_func(f"[{tag}] {filename} → {dest}" if status != 'skipped' else f"[{tag}] {filename}")
                else:
                    dup_undef_dir = os.path.join(duplicates_dir, "UNDEFINED")
                    safe_name = sanitize_filename(Path(filename).stem)
                    new_filename = f"{safe_name}{ext}"
                    dest_path = os.path.join(undefined_dir, new_filename)

                    if os.path.normpath(filepath) == os.path.normpath(dest_path):
                        stats['undefined_skipped'] += 1
                        if log_func:
                            log_func(f"[UNDEF/SKIP] {filename} уже на месте")
                        continue

                    if is_duplicate(filepath, undefined_dir, new_filename):
                        dest = move_to_dir(filepath, dup_undef_dir, new_filename)
                        stats['undefined_dup'] += 1
                        if log_func:
                            log_func(f"[UNDEF/DUP] {filename} → {dest}")
                    else:
                        dest = move_to_dir(filepath, undefined_dir, new_filename)
                        stats['undefined'] += 1
                        if log_func:
                            log_func(f"[UNDEF] {filename} → {dest}")
            except Exception as e:
                stats['errors'] += 1
                try:
                    safe_name = sanitize_filename(Path(filename).stem)
                    new_filename = f"{safe_name}{ext}"
                    dest = move_to_dir(filepath, undefined_dir, new_filename)
                    if log_func:
                        log_func(f"[ERROR] {filename} — {e}. Перемещён в {dest}")
                except Exception:
                    if log_func:
                        log_func(f"[ERROR] {filename} — {e}.")

    return stats


def sort_all_simple():
    """Консольная версия сортировки (для main.py)."""
    from config import SOURCE_DIR, TARGET_PHOTO_DIR, TARGET_VIDEO_DIR, TARGET_UNDEFINED_DIR, DUPLICATES_DIR

    print(f"Сканирую: {SOURCE_DIR}")
    print(f"Фото: {TARGET_PHOTO_DIR}")
    print(f"Видео: {TARGET_VIDEO_DIR}")
    print(f"Неопознанные: {TARGET_UNDEFINED_DIR}")
    print(f"Дубликаты: {DUPLICATES_DIR}\n")

    if not os.path.exists(SOURCE_DIR):
        print(f"Ошибка: папка-источник '{SOURCE_DIR}' не найдена!")
        return

    stats = sort_all(
        SOURCE_DIR, TARGET_PHOTO_DIR, TARGET_VIDEO_DIR, TARGET_UNDEFINED_DIR, DUPLICATES_DIR,
        log_func=lambda msg: print(msg),
        progress_func=lambda cur, total: print(f"\rОбработано: {cur} из {total}", end=""),
    )

    print("\n\n" + "=" * 50)
    print("  РЕЗУЛЬТАТЫ")
    print("=" * 50)
    print(f"  Всего обработано: {stats['total']}")
    print(f"  --- ФОТО ---")
    print(f"  Отсортировано: {stats['photo_sorted']}")
    print(f"  Без даты (NA): {stats['photo_na']}")
    print(f"  Дубликаты:     {stats['photo_dup']}")
    print(f"  Пропущено:     {stats['photo_skipped']}")
    print(f"  --- ВИДЕО ---")
    print(f"  Отсортировано: {stats['video_sorted']}")
    print(f"  Без даты (NA): {stats['video_na']}")
    print(f"  Дубликаты:     {stats['video_dup']}")
    print(f"  Пропущено:     {stats['video_skipped']}")
    print(f"  --- ПРОЧЕЕ ---")
    print(f"  Неопознанные:          {stats['undefined']}")
    print(f"  Неопознанные дубли:    {stats['undefined_dup']}")
    print(f"  Неопознанные пропущено:{stats['undefined_skipped']}")
    print(f"  Ошибки:                {stats['errors']}")
    print("=" * 50)


def clean_empty_dirs():
    """Удаляет пустые папки в SOURCE_DIR (консольная версия)."""
    from config import SOURCE_DIR
    print(f"\nИщу пустые папки в: {SOURCE_DIR}\n")
    removed = remove_empty_dirs(SOURCE_DIR)
    print(f"\nУдалено пустых папок: {removed}")
