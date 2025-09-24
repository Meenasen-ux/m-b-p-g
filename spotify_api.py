import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

def get_spotify_client():
    auth_manager = SpotifyClientCredentials(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET
    )
    return spotipy.Spotify(auth_manager=auth_manager)

def search_tracks_by_keywords(keywords, limit=12):
    sp = get_spotify_client()
    try:
        results = sp.search(q=keywords, type="track", limit=limit)
        tracks = []
        for item in results["tracks"]["items"]:
            track = {
                "name": item["name"],
                "artists": ", ".join([a["name"] for a in item["artists"]]),
                "album": item["album"]["name"],
                "link": item["external_urls"]["spotify"],
                "cover": item["album"]["images"][0]["url"] if item["album"]["images"] else None,
                "preview_url": item.get("preview_url")
            }
            tracks.append(track)
        return tracks
    except:
        return []
