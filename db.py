import sqlite3
import datetime
import os

DB_PATH = os.getenv("MPG_DB_PATH", "playlists.sqlite3")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS saved_playlists (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        mood TEXT,
        keywords TEXT,
        created_at TEXT,
        tracks_json TEXT
    )
    """)
    conn.commit()
    conn.close()

def save_playlist(mood, keywords, tracks_json):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO saved_playlists (mood, keywords, created_at, tracks_json) VALUES (?, ?, ?, ?)",
        (mood, keywords, datetime.datetime.utcnow().isoformat(), tracks_json)
    )
    conn.commit()
    conn.close()

def list_playlists():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, mood, keywords, created_at, tracks_json FROM saved_playlists ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return [{"id": r[0], "mood": r[1], "keywords": r[2], "created_at": r[3], "tracks_json": r[4]} for r in rows]
