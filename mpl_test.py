import mpl.core as mpl


TEST_PLAYLIST_PATH = "playlists/generated_example.mpl"

SAMPLE_TRACKS = [
    "/home/konnosr/Music/Internet/Big Thief/Two Hands/1.07 - Not.flac",
    "/home/konnosr/Music/Internet/Adrianne Lenker/songs/1.02 - ingydar.flac",
    "/home/konnosr/Music/Internet/Mitski/Bury Me At Makeout Creek/1.02 - Townie.flac",
    "/home/konnosr/Projects/RhythmSync/playlists/pyproject.toml"
]


def test_create(tracks=None, path=None, name=None):
    tracks = tracks or SAMPLE_TRACKS
    path = path or TEST_PLAYLIST_PATH
    name = name or "Test Playlist"

    print(f"Creating playlist: {name}")
    result = mpl.create_playlist(tracks, path, playlist_name=name)
    print(f"  Saved to: {result}\n")
    return result


def test_load(path=None):
    path = path or TEST_PLAYLIST_PATH

    print(f"Loading playlist: {path}")
    tracks = mpl.load_playlist(path)
    print(f"  Found {len(tracks)} track(s):")
    for t in tracks:
        print(f"    {t}")
    print()
    return tracks


def test_repair(path=None, search_dirs=None):
    path = path or TEST_PLAYLIST_PATH
    search_dirs = search_dirs or ["~"]

    print(f"Repairing playlist: {path}")
    print(f"  Searching: {search_dirs}")
    fixed = mpl.repair_playlist(path, search_dirs)
    print(f"  Fixed {fixed} track(s)\n")
    return fixed


if __name__ == "__main__":
    while True:
        cmd = input()

        if cmd == "create":
            test_create()
        elif cmd == "load":
            test_load()
        elif cmd == "repair":
            test_repair()
        else:
            break