# Photo-Sorter

Утилиты для сортировки, переименования и архивации фото- и видеоматериалов.

## Структура проекта
```bash
photo/
├── src/ # Основной код сортировки
│ ├── config.py # Настройки путей и расширений
│ ├── duplicates.py # Проверка дубликатов по хешу
│ ├── exif_reader.py # Чтение метаданных (Pillow, ffprobe)
│ ├── file_ops.py # Операции с файлами (перемещение, очистка)
│ └── sorter.py # Основная логика сортировки
├── scripts/ # Вспомогательные утилиты
│ ├── archive_years.py # Архивирование по годам (требует 7-Zip)
│ └── rename_cyrillic.py # Переименование файлов (транслитерация)
├── main.py # Точка входа (консольное меню)
└── README.md
```
## Требования

- **Python 3.8+**
- **[Pillow](https://python-pillow.org/)** — чтение EXIF из фото
- **[exifread](https://pypi.org/project/exifread/)** — чтение EXIF из RAW
- **[FFmpeg](https://ffmpeg.org/)** — чтение метаданных из видео (ffprobe)
- **[7-Zip](https://www.7-zip.org/)** — только для скрипта `archive_years.py`

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

Или через Makefile:

```bash
make install
```

### 3. Установить FFmpeg
* Скачайте [ffmpeg-release-essentials.zip](https://www.gyan.dev/ffmpeg/builds/)
* Распакуйте в C:\Program Files\ffmpeg\
* В src/config.py укажите путь:

```python
FFPROBE_PATH = r"C:\Program Files\ffmpeg\bin\ffprobe.exe"
```
Добавлять в системный PATH не нужно.

### 4. Установить 7-Zip (только для архивации)
Скачайте с [7-zip.org](https://www.7-zip.org/) и установите. Скрипт archive_years.py ищет 7z.exe в стандартных путях.

## Использование

### Основное меню (сортировка фото и видео)

```bash
python main.py
```

Меню:

* 1 — Сортировать всё (фото, видео, неопознанные)
* 2 — Удалить пустые папки
* 3 — Выход

### Архивация по месяцам
```bash
python scripts/archive_years.py
```

Создаёт zip-архивы без сжатия в формате `2017-01.zip`, `2017-02.zip`...

Перед запуском укажите пути в `scripts/archive_years.py`:

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
Перед запуском укажите путь в скрипте:

```python
TARGET_DIR = r"Z:\PHOTO"DIR в скрипте
```

## Команды Makefile

```bash
make help      # Показать все команды
make install   # Установить зависимости
make run       # Запустить основное меню
make sort      # Запустить сортировку напрямую
make archive   # Запустить архивацию
make rename    # Запустить переименование
make clean     # Очистить временные файлы
```

## Настройка путей

Все пути к папкам задаются в `src/config.py`:

```python
SOURCE_DIR = r"Z:\UNSORTED"              # Исходная папка (откуда берём)
TARGET_PHOTO_DIR = r"Z:\PHOTO"           # Целевая для фото
TARGET_VIDEO_DIR = r"Z:\VIDEO"           # Целевая для видео
TARGET_UNDEFINED_DIR = r"Z:\UNDEFINED"   # Для неопознанных файлов
DUPLICATES_DIR = r"Z:\DUPLICATES"        # Для дубликатов
FFPROBE_PATH = r"C:\Program Files\ffmpeg\bin\ffprobe.exe"  # Путь к ffprobe
```

## Расширения файлов
В src/config.py также настраиваются обрабатываемые расширения:

```python
PHOTO_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.heic', '.heif',
    '.cr2', '.nef', '.arw', '.dng', '.orf', '.rw2', '.pef', '.raf',
    '.tif', '.tiff', '.webp', '.bmp'}

VIDEO_EXTENSIONS = {'.mp4', '.mov', '.avi', '.mkv', '.mts', '.m2ts',
    '.wmv', '.3gp', '.webm', '.flv', '.m4v', '.mpg', '.mpeg', '.ts'}
```

## Примечания
* Файлы сортируются в структуру: Год/Месяц/Число/
* Дубликаты определяются по SHA256-хешу и перемещаются в отдельную папку
* Русские буквы в именах транслитерируются при переименовании
* Видео без даты съёмки попадают в VIDEO/NA/
* Архивы создаются без сжатия (-mx0), только для хранения

## Порядок работы
* Сортировка (main.py) — разложить фото и видео по датам
* Переименование (rename_cyrillic.py) — очистить имена файлов
* Архивация (archive_years.py) — упаковать в zip по месяцам

## 📄 Лицензия

MIT