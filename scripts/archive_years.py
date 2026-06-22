import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

# ========== НАСТРОЙКИ ==========
SOURCE_ROOT = r"Z:\PHOTO"
DEST_ROOT = r"Z:\PHOTO_ARCHIVES"
START_YEAR = ""                 # Начать с этого года (4 цифры). "" — с самого раннего.
# ==============================

SEVEN_ZIP_PATHS = [
    r"C:\Program Files\7-Zip\7z.exe",
    r"C:\Program Files (x86)\7-Zip\7z.exe",
]


def find_7zip() -> str | None:
    for path in SEVEN_ZIP_PATHS:
        if os.path.isfile(path):
            return path
    return None


def format_duration(seconds: float) -> str:
    if seconds < 60:
        return f"{seconds:.0f} сек"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f} мин"
    else:
        hours = seconds / 3600
        return f"{hours:.1f} ч"


def test_archive(seven_zip: str, zip_path: Path) -> bool:
    """Проверяет целостность архива через 7z t."""
    try:
        result = subprocess.run(
            [seven_zip, "t", str(zip_path)],
            capture_output=True,
            text=True,
            timeout=300,
        )
        return result.returncode == 0
    except Exception:
        return False


def create_archive(seven_zip: str, source_dir: Path, zip_path: Path) -> bool:
    """
    Создаёт архив из всех файлов в source_dir (рекурсивно) одной командой.
    Возвращает True при успехе.
    """
    list_file = None
    try:
        import tempfile
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8") as tf:
            for f in sorted(source_dir.rglob("*")):
                if f.is_file():
                    tf.write(str(f) + "\n")
            list_file = tf.name

        result = subprocess.run(
            [seven_zip, "a", "-tzip", "-mx0", "-y", str(zip_path), f"@{list_file}"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )

        return result.returncode == 0

    except Exception:
        return False
    finally:
        if list_file and os.path.isfile(list_file):
            os.unlink(list_file)


def collect_year_months(source_root: str, start_year: str) -> list[tuple[str, Path]]:
    """
    Собирает список (год-месяц, путь) для всех подпапок.
    Возвращает отсортированный список.
    """
    source_path = Path(source_root)
    result = []

    for year_dir in sorted(source_path.iterdir()):
        if not year_dir.is_dir():
            continue
        if not (year_dir.name.isdigit() and len(year_dir.name) == 4):
            continue
        if start_year and year_dir.name < start_year:
            continue

        for month_dir in sorted(year_dir.iterdir()):
            if not month_dir.is_dir():
                continue
            if not (month_dir.name.isdigit() and len(month_dir.name) == 2):
                continue

            label = f"{year_dir.name}-{month_dir.name}"
            result.append((label, month_dir))

    return result


def main() -> None:
    seven_zip = find_7zip()
    if seven_zip is None:
        print("7-Zip не найден! Установите с https://7-zip.org/")
        input("\nНажмите Enter для выхода...")
        sys.exit(1)

    print(f"Найден 7-Zip: {seven_zip}\n")

    # Собираем список год-месяц
    entries = collect_year_months(SOURCE_ROOT, START_YEAR)
    if not entries:
        print("Папки год-месяц не найдены.")
        input("\nНажмите Enter для выхода...")
        return

    total = len(entries)
    dest_path = Path(DEST_ROOT)
    dest_path.mkdir(parents=True, exist_ok=True)

    ok_count = 0
    failed_count = 0
    skipped_count = 0

    start_all = datetime.now()
    print(f"Начало: {start_all.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Всего папок: {total}\n")

    for index, (label, source_dir) in enumerate(entries, 1):
        zip_path = dest_path / f"{label}.zip"
        start_item = datetime.now()

        # Прогресс
        print(f"[{index}/{total}] {label} — ", end="", flush=True)

        # Существующий архив — проверяем
        if zip_path.exists() and zip_path.stat().st_size > 0:
            print("проверка...", end="", flush=True)
            if test_archive(seven_zip, zip_path):
                duration = (datetime.now() - start_item).total_seconds()
                size_mb = zip_path.stat().st_size / (1024 * 1024)
                print(f" ок ({size_mb:.1f} MB, {format_duration(duration)})")
                skipped_count += 1
                continue
            else:
                print(" битый, удаляю...", end="", flush=True)
                zip_path.unlink()

        # Создаём архив
        print("создаю...", end="", flush=True)
        success = create_archive(seven_zip, source_dir, zip_path)

        duration = (datetime.now() - start_item).total_seconds()

        if success and zip_path.exists() and zip_path.stat().st_size > 0:
            size_mb = zip_path.stat().st_size / (1024 * 1024)
            print(f" готово ({size_mb:.1f} MB, {format_duration(duration)})")
            ok_count += 1
        else:
            print(f" ошибка ({format_duration(duration)})")
            failed_count += 1
            if zip_path.exists():
                zip_path.unlink()

    end_all = datetime.now()
    total_duration = (end_all - start_all).total_seconds()

    print(f"\n{'=' * 50}")
    print(f"  ИТОГО")
    print(f"  Всего папок: {total}")
    print(f"  Создано:     {ok_count}")
    print(f"  Пропущено:   {skipped_count}")
    print(f"  Ошибок:      {failed_count}")
    print(f"{'=' * 50}")
    print(f"  Начало:      {start_all.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Конец:       {end_all.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Общее время: {format_duration(total_duration)}")
    print(f"{'=' * 50}")
    print("\nГотово.")
    input("\nНажмите Enter для выхода...")


if __name__ == "__main__":
    main()
