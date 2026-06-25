import os
from pathlib import Path
from src.config import (
    SOURCE_DIR, TARGET_PHOTO_DIR, TARGET_VIDEO_DIR, TARGET_UNDEFINED_DIR, DUPLICATES_DIR,
    PHOTO_EXTENSIONS, VIDEO_EXTENSIONS
)
from src.duplicates import is_duplicate
from src.exif_reader import get_date_taken
from src.file_ops import (
    sanitize_filename, move_to_dir, get_dest_subdir, remove_empty_dirs,
    build_filename, find_free_name
)


def process_file(filepath, target_dir, duplicates_dir, is_video=False):
    original_stem = Path(filepath).stem
    original_ext = Path(filepath).suffix.lower()
    date_taken = get_date_taken(filepath, is_video)
    current_dir = os.path.dirname(filepath)

    if is_video:
        dup_base = os.path.join(duplicates_dir, "VIDEO")
    elif original_ext in PHOTO_EXTENSIONS:
        dup_base = os.path.join(duplicates_dir, "PHOTO")
    else:
        dup_base = os.path.join(duplicates_dir, "UNDEFINED")

    if date_taken is None:
        safe_name = sanitize_filename(original_stem)
        new_filename = f"{safe_name}{original_ext}"
        na_dir = os.path.join(target_dir, "NA")
        dest_path = os.path.join(na_dir, new_filename)
        if os.path.normpath(filepath) == os.path.normpath(dest_path):
            return ('skipped', filepath)
        if os.path.normpath(current_dir) == os.path.normpath(na_dir):
            return ('skipped', filepath)
        if is_duplicate(filepath, na_dir, new_filename):
            return ('duplicate', move_to_dir(filepath, os.path.join(dup_base, "NA"), new_filename))
        return ('na', move_to_dir(filepath, na_dir, new_filename))

    date_prefix = date_taken.strftime("%Y%m%d_%H%M%S")
    dest_subdir = get_dest_subdir(target_dir, date_taken)
    new_filename = build_filename(original_stem, date_prefix, original_ext)
    dest_path = os.path.join(dest_subdir, new_filename)

    if os.path.normpath(filepath) == os.path.normpath(dest_path):
        return ('skipped', filepath)
    if os.path.normpath(current_dir) == os.path.normpath(dest_subdir):
        os.rename(filepath, dest_path)
        return ('sorted', dest_path)
    if is_duplicate(filepath, dest_subdir, new_filename):
        base = Path(new_filename).stem
        final_name = find_free_name(dest_subdir, base, original_ext, new_filename)
        final_path = os.path.join(dest_subdir, final_name)
        move_to_dir(filepath, dest_subdir, final_name)
        return ('sorted', final_path)
    return ('sorted', move_to_dir(filepath, dest_subdir, new_filename))


def sort_all(source_dir, photo_dir, video_dir, undefined_dir, duplicates_dir, log_func=None, progress_func=None, stop_flag=None):
    stats = {
        'photo_sorted': 0, 'photo_na': 0, 'photo_dup': 0, 'photo_skipped': 0,
        'video_sorted': 0, 'video_na': 0, 'video_dup': 0, 'video_skipped': 0,
        'undefined': 0, 'undefined_dup': 0, 'undefined_skipped': 0,
        'total': 0, 'errors': 0
    }
    total_files = sum(len(files) for _, _, files in os.walk(source_dir))

    for root, _, files in os.walk(source_dir):
        if stop_flag and stop_flag(): break
        for filename in files:
            if stop_flag and stop_flag(): break
            stats['total'] += 1
            if progress_func: progress_func(stats['total'], total_files)

            filepath = os.path.join(root, filename)
            ext = Path(filename).suffix.lower()
            is_video = ext in VIDEO_EXTENSIONS
            is_photo = ext in PHOTO_EXTENSIONS and not is_video

            try:
                if is_photo:
                    status, dest = process_file(filepath, photo_dir, duplicates_dir, False)
                    stats['photo_' + status] += 1
                elif is_video:
                    status, dest = process_file(filepath, video_dir, duplicates_dir, True)
                    stats['video_' + status] += 1
                else:
                    safe_name = sanitize_filename(Path(filename).stem)
                    new_filename = f"{safe_name}{ext}"
                    dest_path = os.path.join(undefined_dir, new_filename)
                    if os.path.normpath(filepath) == os.path.normpath(dest_path):
                        stats['undefined_skipped'] += 1
                        continue
                    if is_duplicate(filepath, undefined_dir, new_filename):
                        move_to_dir(filepath, os.path.join(duplicates_dir, "UNDEFINED"), new_filename)
                        stats['undefined_dup'] += 1
                    else:
                        move_to_dir(filepath, undefined_dir, new_filename)
                        stats['undefined'] += 1
            except Exception:
                stats['errors'] += 1
    return stats


def sort_all_simple():
    print(f"Сканирую: {SOURCE_DIR}")
    if not os.path.exists(SOURCE_DIR):
        print(f"Ошибка: папка '{SOURCE_DIR}' не найдена!")
        return

    total_files = sum(len(files) for _, _, files in os.walk(SOURCE_DIR))
    print(f"Найдено файлов: {total_files}\n")

    def progress_func(current, total):
        percent = current / total * 100 if total else 0
        print(f"\rОбработано: {current}/{total} ({percent:.1f}%)", end="", flush=True)

    stats = sort_all(
        SOURCE_DIR, TARGET_PHOTO_DIR, TARGET_VIDEO_DIR, TARGET_UNDEFINED_DIR, DUPLICATES_DIR,
        progress_func=progress_func
    )

    print("\n")
    print(f"Всего обработано: {stats['total']}")
    print(f"Фото отсортировано: {stats['photo_sorted']}, NA: {stats['photo_na']}, дублей: {stats['photo_dup']}, пропущено: {stats['photo_skipped']}")
    print(f"Видео отсортировано: {stats['video_sorted']}, NA: {stats['video_na']}, дублей: {stats['video_dup']}, пропущено: {stats['video_skipped']}")
    print(f"Неопознанные: {stats['undefined']}, дублей: {stats['undefined_dup']}, пропущено: {stats['undefined_skipped']}")
    print(f"Ошибок: {stats['errors']}")


def clean_empty_dirs():
    print(f"\nИщу пустые папки в: {SOURCE_DIR}")
    removed = remove_empty_dirs(SOURCE_DIR)
    print(f"Удалено пустых папок: {removed}")
