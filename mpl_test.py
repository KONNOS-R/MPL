import mpl.core as mpl


path = "playlists/generated_example.mpl"

'''
mpl.create_playlist(
    ["/home/konnosr/Music/Internet/Big Thief/Two Hands/1.07 - Not.flac",
    "/home/konnosr/Music/Internet/Adrianne Lenker/songs/1.02 - ingydar.flac",
    "/home/konnosr/Music/Internet/Mitski/Bury Me At Makeout Creek/1.02 - Townie.flac"
    ],
    path,
    playlist_name="My Chill Mix"
)
'''

tracks = mpl.load_playlist(path)
print(tracks)

fixed = mpl.repair_playlist(path, ["~"])