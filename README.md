# Photo-Sorter

Утилиты для сортировки, переименования и архивации фото- и видеоматериалов.

## Структура проекта

```text
photo-sorter/
├── src/                       # Основной код
│   ├── __init__.py
│   ├── config.py              # Настройки путей, расширений, ffprobe
│   ├── duplicates.py          # Проверка дубликатов по SHA256
│   ├── exif_reader.py         # Чтение даты из фото (Pillow) и видео (ffprobe)
│   ├── file_ops.py            # Операции с файлами и именами
│   ├── sorter.py              # Сортировка фото и видео
│   ├── renamer.py             # Переименование (транслитерация)
│   └── archiver.py            # Архивация по месяцам
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
- **[7-Zip](https://www.7-zip.org/)** — только для архивации

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

Или:

```cmd
make.bat install
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

Скачайте с [7-zip.org](https://www.7-zip.org/) и установите. Скрипт архивации ищет 7z.exe в стандартных путях.

## Запуск

### Интерактивное меню

```bash
python main.py
```

### Отдельные команды

#### Windows (CMD)

```cmd
make.bat menu      # Интерактивное меню
make.bat sort      # Сортировка фото и видео
make.bat rename    # Переименование (транслитерация)
make.bat archive   # Архивация по месяцам
make.bat clean     # Удалить пустые папки
```

#### Windows (PowerShell)

```powershell
.\Makefile.ps1 menu
.\Makefile.ps1 sort
.\Makefile.ps1 rename
.\Makefile.ps1 archive
.\Makefile.ps1 clean
```

## Меню

```text
==================================================
  PHOTO-SORTER
==================================================
  1. Сортировать фото и видео
  2. Переименовать файлы (транслитерация)
  3. Архивировать по месяцам
  4. Удалить пустые папки
  5. Выход
--------------------------------------------------
```

## Настройка путей

Все пути задаются в `src/config.py`:

```python
# Сортировка
SOURCE_DIR = r"Z:\UNSORTED"              # Откуда берём
TARGET_PHOTO_DIR = r"Z:\PHOTO"           # Целевая для фото
TARGET_VIDEO_DIR = r"Z:\VIDEO"           # Целевая для видео
TARGET_UNDEFINED_DIR = r"Z:\UNDEFINED"   # Для неопознанных
DUPLICATES_DIR = r"Z:\DUPLICATES"        # Для дубликатов

# Переименование
RENAME_DIR = r"Z:\PHOTO"                 # Папка для переименования

# Архивация
ARCHIVE_SOURCE = r"Z:\PHOTO"             # Откуда берём
ARCHIVE_DEST = r"Z:\PHOTO_ARCHIVES"      # Куда складываем
ARCHIVE_START_YEAR = ""                  # Начать с года ("" — все)
```

### Расширения файлов

```python
PHOTO_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.heic', '.heif',
    '.cr2', '.nef', '.arw', '.dng', '.orf', '.rw2', '.pef', '.raf',
    '.tif', '.tiff', '.webp', '.bmp'}

VIDEO_EXTENSIONS = {'.mp4', '.mov', '.avi', '.mkv', '.mts', '.m2ts',
    '.wmv', '.3gp', '.webm', '.flv', '.m4v', '.mpg', '.mpeg', '.ts'}
```

## Порядок работы

1. **Сортировка** — разложить фото и видео по датам в структуру `Год/Месяц/Число/`. Имена очищаются сразу при сортировке.
2. **Переименование** — дополнительная очистка имён: транслитерация, уплотнение повторов, удаление суффиксов.
3. **Архивация** — упаковать в zip по месяцам (`2017-01.zip`, `2017-02.zip`...) без сжатия.

## Примечания

- Проект рассчитан на Windows. Пути задаются в формате `Z:\...`
- Дубликаты определяются по SHA256-хешу и перемещаются в отдельную папку
- Видео без даты съёмки попадают в `VIDEO/NA/`
- Архивы создаются без сжатия (`-mx0`), только для хранения
- При повторной сортировке имена не задваиваются

## Лицензия

MIT