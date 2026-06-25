import os
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path
from src.config import ARCHIVE_SOURCE, ARCHIVE_DEST, ARCHIVE_START_YEAR


def _find_7zip():
    for p in [r"C:\Program Files\7-Zip\7z.exe", r"C:\Program Files (x86)\7-Zip\7z.exe"]:
        if os.path.isfile(p):
            return p
    return None


def _test_archive(seven_zip, zip_path):
    try:
        r = subprocess.run([seven_zip, "t", str(zip_path)], capture_output=True, text=True, timeout=300)
        return r.returncode == 0
    except Exception:
        return False


def _create_archive(seven_zip, source_dir, zip_path):
    list_file = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8") as tf:
            for f in sorted(source_dir.rglob("*")):
                if f.is_file():
                    tf.write(str(f) + "\n")
            list_file = tf.name
        r = subprocess.run([seven_zip, "a", "-tzip", "-mx0", "-y", str(zip_path), f"@{list_file}"],
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        return r.returncode == 0
    except Exception:
        return False
    finally:
        if list_file and os.path.isfile(list_file):
            os.unlink(list_file)


def archive_photos():
    seven_zip = _find_7zip()
    if not seven_zip:
        print("7-Zip не найден! Установите с https://7-zip.org/")
        return

    print(f"Найден 7-Zip: {seven_zip}\n")
    source_path = Path(ARCHIVE_SOURCE)
    dest_path = Path(ARCHIVE_DEST)

    if not source_path.exists():
        print(f"Ошибка: папка '{ARCHIVE_SOURCE}' не найдена!")
        return

    entries = []
    for year_dir in sorted(source_path.iterdir()):
        if not year_dir.is_dir() or not (year_dir.name.isdigit() and len(year_dir.name) == 4): continue
        if ARCHIVE_START_YEAR and year_dir.name < ARCHIVE_START_YEAR: continue
        for month_dir in sorted(year_dir.iterdir()):
            if not month_dir.is_dir() or not (month_dir.name.isdigit() and len(month_dir.name) == 2): continue
            entries.append((f"{year_dir.name}-{month_dir.name}", month_dir))

    if not entries:
        print("Папки год-месяц не найдены.")
        return

    total = len(entries)
    dest_path.mkdir(parents=True, exist_ok=True)
    ok = failed = skipped = 0
    start_all = datetime.now()
    print(f"Начало: {start_all.strftime('%Y-%m-%d %H:%M:%S')} | Всего папок: {total}\n")

    for index, (label, source_dir) in enumerate(entries, 1):
        zip_path = dest_path / f"{label}.zip"
        start_item = datetime.now()
        print(f"[{index}/{total}] {label} — ", end="", flush=True)

        if zip_path.exists() and zip_path.stat().st_size > 0:
            print("проверка...", end="", flush=True)
            if _test_archive(seven_zip, zip_path):
                d = (datetime.now() - start_item).total_seconds()
                print(f" ок ({zip_path.stat().st_size / (1024*1024):.1f} MB, {d:.0f} сек)")
                skipped += 1
                continue
            else:
                print(" битый, удаляю...", end="", flush=True)
                zip_path.unlink()

        print("создаю...", end="", flush=True)
        success = _create_archive(seven_zip, source_dir, zip_path)
        d = (datetime.now() - start_item).total_seconds()
        if success and zip_path.exists() and zip_path.stat().st_size > 0:
            print(f" готово ({zip_path.stat().st_size / (1024*1024):.1f} MB, {d:.0f} сек)")
            ok += 1
        else:
            print(f" ошибка ({d:.0f} сек)")
            failed += 1
            if zip_path.exists(): zip_path.unlink()

    total_d = (datetime.now() - start_all).total_seconds()
    print(f"\n{'=' * 40}")
    print(f"  Создано: {ok} | Пропущено: {skipped} | Ошибок: {failed}")
    print(f"  Общее время: {total_d:.0f} сек")
    print(f"{'=' * 40}")
