import mpl.core as mpl

mpl.create_playlist(
    ["/home/konnosr/Music/Internet/Mitski/Lush - needs fixes/04-Mitski-Real Men.flac"],
    "my_mix.mpl",
    playlist_name="My Chill Mix"
)

tracks = mpl.load_playlist("my_mix.mpl")
print(tracks)

fixed = mpl.repair_playlist(
    "my_mix.mpl",
    ["~"]
)