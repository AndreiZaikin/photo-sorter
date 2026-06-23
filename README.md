# Photo-Sorter

Утилиты для сортировки, переименования и архивации фото- и видеоматериалов.

## Структура проекта

```text
photo-sorter/
├── src/                       # Основной код сортировки
│   ├── __init__.py
│   ├── config.py              # Настройки путей, расширений, ffprobe
│   ├── duplicates.py          # Проверка дубликатов по SHA256
│   ├── exif_reader.py         # Чтение даты из фото (Pillow) и видео (ffprobe)
│   ├── file_ops.py            # Перемещение, переименование, очистка
│   └── sorter.py              # Основная логика сортировки
├── scripts/                   # Вспомогательные утилиты
│   ├── archive_photos.py      # Архивирование по месяцам (требует 7-Zip)
│   └── rename_cyrillic.py     # Переименование (транслитерация, очистка имён)
├── main.py                    # Консольное меню
├── make.bat                   # Команды для Windows (CMD)
├── Makefile.ps1               # Команды для PowerShell
├── .gitignore
└── README.md
```

## Требования

- **Windows 10/11**
- **Python 3.8+**
- **[Pillow](https://python-pillow.org/)** — чтение EXIF из фото
- **[exifread](https://pypi.org/project/exifread/)** — чтение EXIF из RAW
- **[FFmpeg](https://ffmpeg.org/)** — чтение метаданных из видео (ffprobe)
- **[7-Zip](https://www.7-zip.org/)** — только для скрипта `archive_photos.py`

## Установка

### 1. Клонировать репозиторий

```bash
git clone https://github.com/yourname/photo-sorter.git
cd photo-sorter
```

### 2. Установить зависимости Python

```bash
pip install Pillow exifread
```

### 3. Установить FFmpeg

1. Скачайте [ffmpeg-release-essentials.zip](https://www.gyan.dev/ffmpeg/builds/)
2. Распакуйте в `C:\Program Files\ffmpeg\`
3. В `src/config.py` укажите путь:

```python
FFPROBE_PATH = r"C:\Program Files\ffmpeg\bin\ffprobe.exe"
```

Добавлять в системный PATH **не нужно**.

### 4. Установить 7-Zip (только для архивации)

Скачайте с [7-zip.org](https://www.7-zip.org/) и установите. Скрипт `archive_photos.py` ищет 7z.exe в стандартных путях.

## Запуск

### Windows (CMD)

```cmd
make.bat run
make.bat archive
make.bat rename
```

### Windows (PowerShell)

```powershell
.\Makefile.ps1 run
.\Makefile.ps1 archive
```

## Использование

### Основное меню (сортировка фото и видео)

```bash
python main.py
```

Меню:
- `1` — Сортировать всё (фото, видео, неопознанные)
- `2` — Удалить пустые папки
- `3` — Выход

### Архивация по месяцам

```bash
python scripts/archive_photos.py
```

Создаёт zip-архивы без сжатия в формате `2017-01.zip`, `2017-02.zip`...

**Перед запуском** укажите пути в `scripts/archive_photos.py`:

```python
SOURCE_ROOT = r"Z:\PHOTO"              # Откуда берём
DEST_ROOT = r"Z:\PHOTO_ARCHIVES"       # Куда складываем
START_YEAR = ""                        # Начать с года ("" — все)
```

### Переименование файлов

Транслитерация русских букв, замена пробелов и спецсимволов, уплотнение суффиксов, нижний регистр.

```bash
python scripts/rename_cyrillic.py
```

**Перед запуском** укажите путь в скрипте:

```python
TARGET_DIR = r"Z:\PHOTO"
```

## Команды

| Команда | CMD | PowerShell |
|---------|-----|------------|
| Установить зависимости | `make.bat install` | `.\Makefile.ps1 install` |
| Основное меню | `make.bat run` | `.\Makefile.ps1 run` |
| Сортировка | `make.bat sort` | `.\Makefile.ps1 sort` |
| Архивация | `make.bat archive` | `.\Makefile.ps1 archive` |
| Переименование | `make.bat rename` | `.\Makefile.ps1 rename` |
| Очистить временные файлы | `make.bat clean` | `.\Makefile.ps1 clean` |

## Настройка путей

Все основные пути задаются в `src/config.py`:

```python
SOURCE_DIR = r"Z:\UNSORTED"              # Исходная папка (откуда берём)
TARGET_PHOTO_DIR = r"Z:\PHOTO"           # Целевая для фото
TARGET_VIDEO_DIR = r"Z:\VIDEO"           # Целевая для видео
TARGET_UNDEFINED_DIR = r"Z:\UNDEFINED"   # Для неопознанных файлов
DUPLICATES_DIR = r"Z:\DUPLICATES"        # Для дубликатов
FFPROBE_PATH = r"C:\Program Files\ffmpeg\bin\ffprobe.exe"  # Путь к ffprobe
```

### Расширения файлов

В `src/config.py` также настраиваются обрабатываемые расширения:

```python
PHOTO_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.heic', '.heif',
    '.cr2', '.nef', '.arw', '.dng', '.orf', '.rw2', '.pef', '.raf',
    '.tif', '.tiff', '.webp', '.bmp'}

VIDEO_EXTENSIONS = {'.mp4', '.mov', '.avi', '.mkv', '.mts', '.m2ts',
    '.wmv', '.3gp', '.webm', '.flv', '.m4v', '.mpg', '.mpeg', '.ts'}
```

## Примечания

- Проект рассчитан на Windows. Пути задаются в формате `Z:\````
- Файлы сортируются в структуру: `Год/Месяц/Число/`
- Дубликаты определяются по SHA256-хешу и перемещаются в отдельную папку
- Русские буквы в именах транслитерируются при переименовании
- Видео без даты съёмки попадают в `VIDEO/NA/`
- Архивы создаются без сжатия (`-mx0`), только для хранения

## Порядок работы

1. **Сортировка** (`main.py`) — разложить фото и видео по датам
2. **Переименование** (`rename_cyrillic.py`) — очистить имена файлов
3. **Архивация** (`archive_photos.py`) — упаковать в zip по месяцам

## Лицензия

MIT
