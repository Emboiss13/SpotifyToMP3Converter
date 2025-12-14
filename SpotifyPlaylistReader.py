import spotipy
import yt_dlp
import os
import re
from spotipy.oauth2 import SpotifyOAuth

# 🔓 Authentication ----------------------
# These are the APP credentials I got from Spotify Developer
# Note: 127.0.0.1 is just a universal loopback IP address, so it just means "this computer"
CLIENT_ID = 'id' # Replace with your Spotify Client ID
CLIENT_SECRET = 'secret' # Replace with your Spotify Client Secret
REDIRECT_URI = 'http://127.0.0.1:8888/callback'
SCOPE = 'playlist-read-private'

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
print("\n🎵 YOUR SPOTIFY PLAYLISTS 🎧\n")
for name in playlist_map.keys():
    print(f"- {name}")

# Prompt user to choose one
selected_playlist = input("\nEnter the name of the playlist you want to convert to MP3 files: ").strip()




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
                songs.append(f"{track_name} - {artists} lyrics") # Added "lyrics" to improve YouTube search results
        
        if results['next']:
            results = sp.next(results)
        else:
            results = None
    
    return songs


# Getting selected playlists songs
playlist_info = playlist_map.get(selected_playlist)

if playlist_info:
    song_list = get_songs_from_playlist(sp, playlist_info['id'])
    print(f"Tracks in '{selected_playlist}':")
    for song in song_list:
        print(song)
else:
    print(f"Playlist '{selected_playlist}' not found. Please make sure you typed the playlist correctly.")




# 📹 Searching for Youtube song ----------------------
def search_youtube(query):
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'format': 'bestaudio/best',
        'default_search': 'ytsearch1',  # return top result
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(query, download=False)
            video_url = info['entries'][0]['webpage_url']
            return video_url
        except Exception as e:
            print(f"Failed to find video for: {query}\nError: {e}")
            return None
        
print(f"\n🔍 Searching YouTube for tracks in '{selected_playlist}':\n")




# 📹 Youtube to MP3 ----------------------
def clean_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)

def download_as_mp3(youtube_url, song_name, output_folder='[ADD YOUR PATH HERE]'):
    safe_filename = clean_filename(song_name)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_folder}/{safe_filename}.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
    }

    os.makedirs(output_folder, exist_ok=True)

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([youtube_url])
            print(f"✅ Downloaded: {safe_filename}.mp3")
        except Exception as e:
            print(f"❌ Failed to download {youtube_url}\nError: {e}")


# 🎉 OUTPUT!!!--------------------------------------------------------
for song in song_list:
    print(f"\n🔍 Searching YouTube for: {song}")
    url = search_youtube(song)
    
    if url:
        print(f"🎧 Downloading: {song}")
        download_as_mp3(url, song)
    else:
        print(f"❌ Could not find: {song}")