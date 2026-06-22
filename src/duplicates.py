import hashlib
import os

_hash_cache = {}


def get_file_hash(filepath: str, chunk_size: int = 65536) -> str | None:
    """Вычисляет SHA256-хеш файла. Кеширует результат."""
    if filepath in _hash_cache:
        return _hash_cache[filepath]

    sha256 = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                sha256.update(chunk)
        file_hash = sha256.hexdigest()
        _hash_cache[filepath] = file_hash
        return file_hash
    except OSError:
        return None


def is_duplicate(filepath: str, dest_dir: str, filename: str) -> bool:
    """Проверяет, есть ли в dest_dir файл с таким же именем и содержимым."""
    dest_path = os.path.join(dest_dir, filename)
    if not os.path.exists(dest_path):
        return False

    source_hash = get_file_hash(filepath)
    dest_hash = get_file_hash(dest_path)

    if source_hash is None or dest_hash is None:
        return False

    return source_hash == dest_hash
  