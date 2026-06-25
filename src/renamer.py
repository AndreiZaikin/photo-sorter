import os
from pathlib import Path
from src.config import RENAME_DIR
from src.file_ops import clean_filename, strip_all_suffixes, find_free_name, count_files


def rename_files():
    if not os.path.exists(RENAME_DIR):
        print(f"Ошибка: папка '{RENAME_DIR}' не найдена!")
        return

    stats = {'total': 0, 'renamed': 0, 'skipped': 0, 'errors': 0}
    print(f"Переименование в: {RENAME_DIR}")
    total_files = count_files(RENAME_DIR)
    print(f"Найдено файлов: {total_files}\n")

    for root, _, files in os.walk(RENAME_DIR):
        for filename in files:
            stats['total'] += 1
            percent = stats['total'] / total_files * 100 if total_files else 0
            print(f"\rПрогресс: {stats['total']}/{total_files} ({percent:.1f}%)", end="", flush=True)

            stem = Path(filename).stem
            ext = Path(filename).suffix.lower()
            clean_stem = clean_filename(stem)
            base = strip_all_suffixes(clean_stem)
            target_filename = f"{base}{ext}"

            if target_filename == filename:
                stats['skipped'] += 1
                continue
            if target_filename.lower() == filename.lower():
                try:
                    os.rename(os.path.join(root, filename), os.path.join(root, target_filename))
                    stats['renamed'] += 1
                except OSError:
                    stats['errors'] += 1
                continue
            if not os.path.exists(os.path.join(root, target_filename)):
                try:
                    os.rename(os.path.join(root, filename), os.path.join(root, target_filename))
                    stats['renamed'] += 1
                except OSError:
                    stats['errors'] += 1
                continue

            final_name = find_free_name(root, base, ext, filename)
            if final_name == filename:
                stats['skipped'] += 1
                continue
            try:
                os.rename(os.path.join(root, filename), os.path.join(root, final_name))
                stats['renamed'] += 1
            except OSError:
                stats['errors'] += 1

    print(f"\n\nПереименовано: {stats['renamed']}, пропущено: {stats['skipped']}, ошибок: {stats['errors']}")
