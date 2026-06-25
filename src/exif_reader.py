import subprocess
import json
from datetime import datetime
from pathlib import Path
from PIL import Image
from src.config import VIDEO_EXTENSIONS, FFPROBE_PATH


def get_exif_date_pillow(filepath: str) -> datetime | None:
    try:
        with Image.open(filepath) as img:
            if img.format in ('GIF', 'BMP', 'PCX', 'PPM', 'SGI', 'TGA', 'XBM', 'XPM', 'ICO', 'CUR'):
                return None
            try:
                exif_data = img._getexif()
            except AttributeError:
                exif_data = img.getexif()
            if exif_data:
                date_str = exif_data.get(36867)
                if date_str:
                    return datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S")
    except Exception:
        pass
    return None


def get_video_date_ffprobe(filepath: str) -> datetime | None:
    try:
        result = subprocess.run(
            [FFPROBE_PATH, '-v', 'quiet', '-print_format', 'json', '-show_format', '-show_streams', filepath],
            capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            return None
        data = json.loads(result.stdout)
        for stream in data.get('streams', []):
            tags = stream.get('tags', {})
            for key in ('creation_time', 'date', 'DateTimeOriginal'):
                if key in tags:
                    date_str = tags[key].replace('Z', '').replace('T', ' ').split('.')[0].split('+')[0].strip()
                    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y:%m:%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S"):
                        try:
                            return datetime.strptime(date_str, fmt)
                        except ValueError:
                            continue
        format_tags = data.get('format', {}).get('tags', {})
        for key in ('creation_time', 'date', 'DateTimeOriginal'):
            if key in format_tags:
                date_str = format_tags[key].replace('Z', '').replace('T', ' ').split('.')[0].split('+')[0].strip()
                for fmt in ("%Y-%m-%d %H:%M:%S", "%Y:%m:%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S"):
                    try:
                        return datetime.strptime(date_str, fmt)
                    except ValueError:
                        continue
    except Exception:
        pass
    return None


def get_date_taken(filepath: str, is_video: bool = False) -> datetime | None:
    ext = Path(filepath).suffix.lower()
    if is_video:
        return get_video_date_ffprobe(filepath)
    else:
        if ext in {'.gif', '.bmp', '.txt', '.ini', '.db', '.thm', '.xmp', '.zip', '.rar'}:
            return None
        if ext in VIDEO_EXTENSIONS:
            return None
        return get_exif_date_pillow(filepath)
