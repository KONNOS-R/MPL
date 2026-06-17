import json
import os
import sys
from pathlib import Path
from typing import List, Optional, Dict

import mpl.helpers as helpers


# create an .mpl file
def create_playlist(file_list: List[str], output_path: str, playlist_name: Optional[str] = None) -> str:
    output_path = os.path.abspath(os.path.expanduser(output_path))

    if not output_path.endswith(".mpl"):
        output_path += ".mpl"

    AUDIO_EXTENSIONS = (".mp3", ".flac", ".wav", ".ogg")

    tracks = []

    for raw in file_list:
        abs_path = helpers.get_abs_path(raw)

        if not os.path.isfile(abs_path):
            print(f"Warning: file not found – {abs_path}", file=sys.stderr)
            continue

        if not abs_path.lower().endswith(AUDIO_EXTENSIONS):
            print(f"Warning: unsupported audio format – {abs_path}", file=sys.stderr)

        h = helpers.generate_hash(abs_path)
        tracks.append({
            "path": abs_path,
            "hash": f"sha256:{h}"
        })

    if not tracks:
        raise ValueError("No valid audio files provided; playlist not created.")

    name = playlist_name or Path(output_path).stem
    playlist = {
        "format": "mpl/1.0",
        "playlist_name": name,
        "tracks": tracks
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(playlist, f, indent=4, ensure_ascii=False)

    return output_path


# load .mpl file
def load_playlist(playlist_path: str) -> List[str]:

    path = os.path.abspath(os.path.expanduser(playlist_path))

    if not path.endswith(".mpl"):
        raise ValueError(f"Not an .mpl file: {path}")

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid .mpl file: {path}") from e

    fmt = data.get("format", "")
    if not fmt.startswith("mpl/"):
        raise ValueError(f"Unsupported format: {fmt}")

    tracks = data.get("tracks", [])
    if not tracks:
        print("Warning: playlist is empty.", file=sys.stderr)
        return []

    resolved = []
    for entry in tracks:
        file_path = entry.get("path", "")

        abs_path = os.path.abspath(os.path.expanduser(file_path))

        if os.path.isfile(abs_path):
            resolved.append(abs_path)
        else:
            print(f"Warning: missing file – {abs_path}", file=sys.stderr)

    return resolved


# repair .mpl file
def repair_playlist(playlist_path: str, search_dirs: List[str]) -> int:

    path = os.path.abspath(os.path.expanduser(playlist_path))

    if not path.endswith(".mpl"):
        raise ValueError(f"Not an .mpl file: {path}")

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid .mpl file: {path}") from e

    tracks = data.get("tracks", [])
    if not tracks:
        return 0

    missing = []
    for i, entry in enumerate(tracks):
        file_path = entry.get("path", "")
        abs_path = os.path.abspath(os.path.expanduser(file_path))
        if not os.path.isfile(abs_path):
            h = entry.get("hash", "")
            if h.startswith("sha256:"):
                missing.append((i, h[7:]))

    if not missing:
        print("No missing tracks to repair.")
        return 0

    AUDIO_EXTENSIONS = (".mp3", ".flac", ".wav", ".ogg")

    hash_map: Dict[str, str] = {}
    for directory in search_dirs:
        dir_path = os.path.abspath(os.path.expanduser(directory))
        if not os.path.isdir(dir_path):
            print(f"Warning: not a directory – {dir_path}")
            continue

        for root, _, files in os.walk(dir_path):
            for fname in files:
                # Only hash files with supported audio extensions
                if not fname.lower().endswith(AUDIO_EXTENSIONS):
                    continue

                full = os.path.join(root, fname)
                try:
                    h = helpers.generate_hash(full)
                    if h not in hash_map:
                        hash_map[h] = full
                except OSError:
                    continue

    updated = 0
    for idx, h_val in missing:
        new_path = hash_map.get(h_val)
        if new_path:
            tracks[idx]["path"] = new_path
            updated += 1

    if updated:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"Repaired {updated} of {len(missing)} missing tracks.")
    return updated