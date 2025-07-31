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

# Testing (Printing my current Playlists name and Id)
playlists = sp.current_user_playlists()
for playlist in playlists['items']:
    print(f"Name: {playlist['name']} | ID: {playlist['id']}")
