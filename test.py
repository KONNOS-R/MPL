import json
import hashlib
import os
import sys
from pathlib import Path


def generate_hash(file_path, chunck=1048576):
    file_size = os.path.getsize(file_path)
    
    with open(file_path, 'rb') as f:
        first = f.read(chunck)
        
        if file_size > chunck * 2:
            f.seek(-chunck, os.SEEK_END)
        else:
            f.seek(0)
        last = f.read(chunck)
    
    hasher = hashlib.sha256()
    hasher.update(first)
    hasher.update(last)
    hasher.update(str(file_size).encode())
    
    return hasher.hexdigest()


def expand_path(path_str):
    return str(Path(os.path.expanduser(path_str)).resolve())


def get_input_paths():
    print("File paths:\n")
    
    paths = []
    while True:
        raw = input(f"Path {len(paths) + 1}: ").strip()
        
        if not raw:
            if paths:
                break
            else:
                print("Add at least one track first.\n")
                continue
        
        raw = raw.strip('\'"')
        expanded = expand_path(raw)
        
        if not os.path.isfile(expanded):
            print(f"Error: File not found - {expanded}\n")
            continue
        
        paths.append(expanded)
        print(f"Added: {expanded}\n")
    
    return paths

def save_playlist(paths, output_dir=None):
    playlist_name = input("\nPlaylist name: ").strip()
    if not playlist_name:
        playlist_name = "Untitled"
    
    print("\nGenerating hashes...")
    tracks = []
    for i, path in enumerate(paths, 1):
        print(f"  [{i}/{len(paths)}] {os.path.basename(path)}")
        hash_val = generate_hash(path)
        home = str(Path.home())

        tracks.append({
            "path": path,
            "hash": f"sha256:{hash_val}"
        })
    
    playlist = {
        "format": "mpl/1.0",
        "playlist_name": playlist_name,
        "tracks": tracks
    }
    
    filename = f"{playlist_name.replace(' ', '_')}.mpl"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(playlist, f, indent=4, ensure_ascii=False)
    
    print(f"\nSaved: {os.path.abspath(filename)}")


def main():
    paths = get_input_paths()
    save_playlist(paths)

if __name__ == "__main__":
    main()