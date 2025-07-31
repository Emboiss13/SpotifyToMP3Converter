import spotipy
from spotipy.oauth2 import SpotifyOAuth

# These are the APP credentials I got from Spotify Developer
# Note-to-self: REMEMBER❗️ that 127.0.0.1 is just a universal loopback IP address, so it just means "this computer"
CLIENT_ID = 'a3a292cbf6e64874abbb239292731d10'
CLIENT_SECRET = '2aeee62be798425298e9624af778b348'
REDIRECT_URI = 'http://127.0.0.1:8888/callback'

SCOPE = 'playlist-read-private'

# 🔓 Authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE
))


# 🎼 Playlist MetaData ----------------------
playlists = sp.current_user_playlists()

playlist_map = {
    playlist['name']: {
        'id': playlist['id'],
        'song_count': playlist['tracks']['total']
    } for playlist in playlists['items']
}

# 👤 User selection ----------------------
print("\n🎵 Giuly's Playlists:")
for name in playlist_map.keys():
    print(f"- {name}")

# Prompt user to choose one
selected_playlist = input("\nEnter the name of the playlist you want to convert: ").strip()


# 🎵 Songs MetaData ----------------------
def get_songs_from_playlist(sp, playlist_id):
    songs = []
    results = sp.playlist_items(playlist_id, fields='items.track.name,items.track.artists.name,next', additional_types=['track'])
    
    while results:
        for item in results['items']:
            track = item['track']
            if track is not None:  # Can be "None" if unavailable
                track_name = track['name']
                artists = ', '.join([artist['name'] for artist in track['artists']])
                songs.append(f"{track_name} - {artists}")
        
        if results['next']:
            results = sp.next(results)
        else:
            results = None
    
    return songs

# Getting the selected songs MetaData
playlist_info = playlist_map.get(selected_playlist)

if playlist_info:
    song_list = get_songs_from_playlist(sp, playlist_info['id'])
    print(f"Tracks in '{selected_playlist}':")
    for song in song_list:
        print(song)
else:
    print(f"Playlist '{selected_playlist}' not found. Please make sure you typed the playlist correctly.")