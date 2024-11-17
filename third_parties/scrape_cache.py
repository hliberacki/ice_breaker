import sqlite3
import json

CACHE_DB_FILE = "cached.db"


def init_db():
    """Initialize the SQLite database and create table if not exists"""
    conn = sqlite3.connect(CACHE_DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS profile_cache (
            url TEXT PRIMARY KEY,
            data TEXT
        )
    """
    )
    conn.commit()
    conn.close()


def get_cached_profile(profile_url: str):
    conn = sqlite3.connect(CACHE_DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT data FROM profile_cache WHERE url = ?", (profile_url,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return json.loads(row[0])  # Return JSON-decoded data
    return None


# Step 4: Write to Cache
def save_to_cache(profile_url, data):
    conn = sqlite3.connect(CACHE_DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR REPLACE INTO profile_cache (url, data) VALUES (?, ?)",
        (profile_url, json.dumps(data)),
    )  # Save JSON-encoded data
    conn.commit()
    conn.close()
