import os
import hashlib


# generates a sha256 partial hash of the requested file
def generate_hash(path: str, chunk: int = 1_048_576) -> str:
    size = os.path.getsize(path)
    with open(path, "rb") as f:
        if size <= chunk:
            data = f.read()
        else:
            head = f.read(chunk)
            f.seek(-chunk, os.SEEK_END)
            tail = f.read(chunk)
            data = head + tail

    h = hashlib.sha256()
    h.update(data)
    h.update(str(size).encode())
    
    return h.hexdigest()


# returns the absolute path of the requested file
def get_abs_path(path: str) -> str:
    abs_path = os.path.abspath(os.path.expanduser(path))
    if not os.path.isfile(abs_path):
        raise FileNotFoundError(f"File not found: {abs_path}")
    
    return abs_path