from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time

# ---- USER INPUT ----
date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

# ---- SCRAPE BILLBOARD ----
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}
billboard_url = "https://www.billboard.com/charts/hot-100/" + date
response = requests.get(url=billboard_url, headers=header)

soup = BeautifulSoup(response.text, 'html.parser')
song_names_spans = soup.select("li ul li h3")
song_names = [song.get_text().strip() for song in song_names_spans]

# ---- SPOTIFY AUTHENTICATION ----
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id="your-client-id",  # <-- Replace with your actual client ID
        client_secret="your-client-secret",  # <-- Replace with your actual client secret
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]
print(f"Authenticated Spotify user ID: {user_id}")

# ---- SEARCH AND COLLECT SONG URIs ----
song_uris = []
year = date.split("-")[0]

for i, song in enumerate(song_names):
    print(f"Searching for: {song} ({i + 1}/{len(song_names)})")
    try:
        result = sp.search(q=f"{song} year:{year}", type="track", limit=1)
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except (IndexError, KeyError):
        print(f"❌ {song} doesn't exist in Spotify. Skipped.")
    time.sleep(0.3)  # Add delay to avoid rate limiting

# ---- CREATE PLAYLIST ----
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
print(f"✅ Playlist created: {playlist['name']}")

# ---- ADD SONGS TO PLAYLIST ----
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
print("✅ All found songs added to the playlist.")
