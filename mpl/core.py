import json
import os
import sys
from pathlib import Path
from typing import List, Optional, Dict, Callable

import mpl.helpers as helpers


def create_playlist(
    output_path: str,
    file_list: List[str],
    playlist_name: Optional[str] = None,
    msg_callback: Optional[Callable[[str, str], None]] = None,
) -> str:

    def _warn(msg: str) -> None:
        if msg_callback:
            msg_callback("warning", msg)

    output_path = os.path.abspath(os.path.expanduser(output_path))
    if not output_path.endswith(".mpl"):
        output_path += ".mpl"

    AUDIO_EXTENSIONS = (".mp3", ".flac", ".wav", ".ogg")
    tracks = []

    for raw in file_list:
        try:
            abs_path = helpers.get_abs_path(raw)
        except FileNotFoundError as e:
            _warn(str(e))
            continue

        if not abs_path.lower().endswith(AUDIO_EXTENSIONS):
            _warn(f"Unsupported file – {abs_path}")
            continue

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


def load_playlist(
    playlist_path: str,
    msg_callback: Optional[Callable[[str, str], None]] = None,
) -> List[str]:

    def _warn(msg: str) -> None:
        if msg_callback:
            msg_callback("warning", msg)

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
        _warn("Playlist is empty.")
        return []

    resolved = []
    for entry in tracks:
        file_path = entry.get("path", "")
        abs_path = os.path.abspath(os.path.expanduser(file_path))
        if os.path.isfile(abs_path):
            resolved.append(abs_path)
        else:
            _warn(f"Missing file – {abs_path}")

    return resolved


def repair_playlist(
    playlist_path: str,
    search_dirs: List[str],
    msg_callback: Optional[Callable[[str, str], None]] = None,
) -> int:

    def _info(msg: str) -> None:
        if msg_callback:
            msg_callback("info", msg)

    def _warn(msg: str) -> None:
        if msg_callback:
            msg_callback("warning", msg)

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
        _info("No missing tracks to repair.")
        return 0

    AUDIO_EXTENSIONS = (".mp3", ".flac", ".wav", ".ogg")
    hash_map: Dict[str, str] = {}

    for directory in search_dirs:
        dir_path = os.path.abspath(os.path.expanduser(directory))
        if not os.path.isdir(dir_path):
            _warn(f"Not a directory – {dir_path}")
            continue

        for root, _, files in os.walk(dir_path):
            for fname in files:
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

    _info(f"Repaired {updated} of {len(missing)} missing tracks.")
    return updated