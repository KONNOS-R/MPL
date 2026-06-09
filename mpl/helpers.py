import os
import hashlib


def generate_hash(path: str, chunk: int = 1_048_576) -> str:
    size = os.path.getsize(path)
    
    with open(path, "rb") as f:
        head = f.read(chunk)
        if size > chunk * 2:
            f.seek(-chunk, os.SEEK_END)

        else:
            f.seek(0)

        tail = f.read(chunk)

    h = hashlib.sha256()
    h.update(head)
    h.update(tail)
    h.update(str(size).encode())

    return h.hexdigest()


def validate_abs_path(path: str) -> str:
    abs_path = os.path.abspath(os.path.expanduser(path))
    if not os.path.isfile(abs_path):
        raise FileNotFoundError(f"File not found: {abs_path}")
    
    return abs_path