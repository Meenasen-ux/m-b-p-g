import streamlit as st
from gemini_api import interpret_mood_with_fallback
from spotify_api import search_tracks_by_keywords
from db import init_db, save_playlist, list_playlists
from utils import tracks_to_json
import pandas as pd
import json

st.set_page_config(page_title="Mood-Based Playlist Generator", layout="wide")
init_db()

st.title("AI Mood-Based Playlist Generator ⋆˚꩜｡𐔌՞. .՞𐦯⋆.")
st.write("Type your mood and get a playlist!")

with st.form("mood_form"):
    mood = st.text_input("Your mood (e.g., 'love')", "")
    num_tracks = st.slider("Number of tracks", 6, 30, 12)
    submit = st.form_submit_button("Generate Playlist")

if submit and mood.strip():
    with st.spinner("Interpreting mood..."):
        keywords, summary = interpret_mood_with_fallback(mood)
    st.markdown("**Keywords:** " + (keywords or "-"))
    st.caption(summary)

    with st.spinner("Fetching tracks from Spotify..."):
        tracks = search_tracks_by_keywords(keywords, limit=num_tracks)

    if not tracks:
        st.warning("No tracks found.")
    else:
        st.subheader("Your Playlist")
        cols = st.columns(3)
        for i, t in enumerate(tracks):
            col = cols[i % 3]
            with col:
                if t["cover"]:
                    st.image(t["cover"], width=200)
                st.markdown(f"**{t['name']}**")
                st.markdown(f"*{t['artists']}*")
                st.markdown(f"{t['album']}")
                st.markdown(f"[Open in Spotify]({t['link']})")
                if t.get("preview_url"):
                    st.audio(t["preview_url"])
                st.markdown("---")

        if st.button("Save this playlist"):
            save_playlist(mood, keywords, tracks_to_json(tracks))
            st.success("Saved playlist to history.")

        if st.button("Export playlist to CSV"):
            df = pd.DataFrame(tracks)
            csv = df.to_csv(index=False)
            st.download_button("Download CSV", csv, file_name="playlist.csv", mime="text/csv")

st.title("Saved Playlists")
saved = list_playlists()
if not saved:
    st.info("No playlists saved yet.")
else:
    for s in saved:
        st.markdown(f"### {s['mood']} - <small>{s['created_at']}</small>", unsafe_allow_html=True)
        st.markdown(f"**Keywords:** {s['keywords']}")
        tracks = []
        try:
            tracks = json.loads(s['tracks_json'])
        except:
            pass
        if tracks:
            cols = st.columns(4)
            for i, t in enumerate(tracks):
                c = cols[i % 4]
                with c:
                    if t.get("cover"):
                        st.image(t["cover"], width=120)
                    st.write(t.get("name"))
                    st.write(t.get("artists"))
        st.markdown("---")
