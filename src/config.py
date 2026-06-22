# ========== НАСТРОЙКИ ПАПОК ==========
DEFAULT_SOURCE = r"Z:\UNSORTED"
DEFAULT_PHOTO = r"Z:\PHOTO"
DEFAULT_VIDEO = r"Z:\VIDEO"
DEFAULT_UNDEFINED = r"Z:\UNDEFINED"
DEFAULT_DUPLICATES = r"Z:\DUPLICATES"

# Для консольной версии
SOURCE_DIR = DEFAULT_SOURCE
TARGET_PHOTO_DIR = DEFAULT_PHOTO
TARGET_VIDEO_DIR = DEFAULT_VIDEO
TARGET_UNDEFINED_DIR = DEFAULT_UNDEFINED
DUPLICATES_DIR = DEFAULT_DUPLICATES
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
