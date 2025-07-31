import spotipy
from spotipy.oauth2 import SpotifyOAuth

# These are the APP credentials I got from Spotify Developer
# Note-to-self: REMEMBER❗️ that 127.0.0.1 is just a universal loopback IP address, so it just means "this computer"
CLIENT_ID = 'a3a292cbf6e64874abbb239292731d10'
CLIENT_SECRET = '2aeee62be798425298e9624af778b348'
REDIRECT_URI = 'http://127.0.0.1:8888/callback'

SCOPE = 'playlist-read-private'

# Authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE
))

# Printing my current Playlists name and Id
playlists = sp.current_user_playlists()

# I am going to keep this print as in the future it will allow me to identify which playlists I have and then manually convert from there
# What am I saying, I can just use user input
# Storing these in a dictionary/map will make accessing the metadata so much easier (so will do that)

playlist_map = {
    playlist['name']: {
        'id': playlist['id'],
        'song_count': playlist['tracks']['total']
    } for playlist in playlists['items']
}
#Testing 🏁
#print(playlist_map)


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


# Values will have to be updated based on input here
# SO far we get the tracks from the playlist correctly
playlist_name = "Cardio"
playlist_info = playlist_map.get(playlist_name)

if playlist_info:
    song_list = get_songs_from_playlist(sp, playlist_info['id'])
    print(f"Tracks in '{playlist_name}':")
    for song in song_list:
        print(song)
else:
    print(f"Playlist '{playlist_name}' not found.")



