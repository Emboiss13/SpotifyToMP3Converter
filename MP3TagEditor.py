import os
from mutagen.easyid3 import EasyID3

def tag_all_mp3s_in_folder(folder_path, album_name=None, artist_name=None, genre=None):
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".mp3"):
            file_path = os.path.join(folder_path, filename)

            try:
                audio = EasyID3(file_path)
            except Exception:
                from mutagen.mp3 import MP3
                audio = MP3(file_path, ID3=EasyID3)
                audio.add_tags()

            if album_name:
                audio["album"] = album_name
            if artist_name:
                audio["artist"] = artist_name
            if genre:
                audio["genre"] = genre

            # "Guess" title from file name if missing
            if "title" not in audio:
                audio["title"] = os.path.splitext(filename)[0]

            audio.save()
            print(f"✅ Edited: {filename}")
        else:
            print(f"⏭️ Skipped (not mp3): {filename}")


# ------------------ MAIN FUNCTION (User input is collected & cleaned) ------------------
if __name__ == "__main__":
    folder = input("📁 Enter path to folder with MP3s: ").strip()
    album = input("💽 Enter album name (optional): ").strip()
    artist = input("🎤 Enter artist name (optional): ").strip()
    genre = input("🎼 Enter genre (optional): ").strip()

    tag_all_mp3s_in_folder(
        folder_path=folder,
        album_name=album if album else None,
        artist_name=artist if artist else None,
        genre=genre if genre else None
    )
