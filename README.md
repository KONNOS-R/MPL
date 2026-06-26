# MPL – **M**usic **Pl**aylist Format

A minimal, human‑readable playlist format designed for local music players.  
MPL stores **absolute file paths** and **partial file hashes**, so tracks can be
found even after they've been moved or renamed.

## Format

``` json
{
  "format": "mpl/1.0",
  "playlist_name": "My Chill Mix",
  "tracks": [
    {
      "path": "/home/user/Music/Artist/Album/track1.flac",
      "hash": "sha256:abc123..."
    }
  ]
}
```

- **path** – absolute, UTF‑8 encoded file location
- **hash** – `sha256:<hexdigest>` of the first 1 MB + last 1 MB + file size
- **format** – always `mpl/1.0` for this version

## Installation

``` 
pip install mpl
```

## Usage

### Create a playlist

``` python
from mpl import create_playlist

tracks = [
    "/home/user/Music/song1.flac",
    "/home/user/Music/song2.mp3",
]

path = create_playlist(
    output_path="my_playlist.mpl",
    file_list=tracks,
    playlist_name="My Mix",
)
print(f"Playlist saved to {path}")
```

### Load a playlist

``` python
from mpl import load_playlist

files = load_playlist("my_playlist.mpl")
for f in files:
    print(f)
```

### Repair broken paths

If you've moved your music collection, `repair_playlist` scans one or more
directories, matches files by their hash, and updates the `.mpl` file.

``` python
from mpl import repair_playlist

fixed = repair_playlist(
    "my_playlist.mpl",
    search_dirs=["~/Music", "/media/external"],
)
print(f"Fixed {fixed} missing tracks.")
```

## Advanced: message callbacks

All functions accept an optional `msg_callback(level, message)` (`info` and `warning` levels).
This lets you integrate with your own logging or UI without relying on stderr.

``` python
def my_logger(level, msg):
    if level == "warning":
        print(f"Warning: {msg}")

load_playlist("playlist.mpl", msg_callback=my_logger)
```

## File structure

```
mpl/
├── __init__.py     # public API
├── core.py         # create_playlist, load_playlist, repair_playlist
└── helpers.py      # supported audio formats, hash generation, path validation
```