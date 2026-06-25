# ========== НАСТРОЙКИ ПАПОК ==========
# Сортировка
SOURCE_DIR = r"D:\DUPLICATES\UNSORTED\2025"
TARGET_PHOTO_DIR = r"D:\DUPLICATES\PHOTO"
TARGET_VIDEO_DIR = r"D:\DUPLICATES\VIDEO"
TARGET_UNDEFINED_DIR = r"D:\DUPLICATES\UNDEFINED"
DUPLICATES_DIR = r"D:\DUPLICATES\DUPLICATES"

# Переименование
RENAME_DIR = r"D:\DUPLICATES\UNSORTED\Photos from 2014"

# Архивация
ARCHIVE_SOURCE = r"D:\DUPLICATES\PHOTO"
ARCHIVE_DEST = r"D:\DUPLICATES\PHOTO_ARCHIVES"
ARCHIVE_START_YEAR = ""
# =====================================

# Путь к ffprobe (если не в PATH)
FFPROBE_PATH = r"C:\Program Files\ffmpeg\bin\ffprobe.exe"

PHOTO_EXTENSIONS = {
    '.jpg', '.jpeg', '.png', '.heic', '.heif',
    '.cr2', '.nef', '.arw', '.dng', '.orf', '.rw2', '.pef', '.raf',
    '.tif', '.tiff', '.webp', '.bmp'
}

VIDEO_EXTENSIONS = {
    '.mp4', '.mov', '.avi', '.mkv', '.mts', '.m2ts', '.wmv',
    '.3gp', '.webm', '.flv', '.m4v', '.mpg', '.mpeg', '.ts'
}
