import sqlite3
from pathlib import Path

DB_PATH = Path("db/app.db")

with sqlite3.connect(DB_PATH) as conn:
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM expert_photos;")
    print("expert_photos count =", cur.fetchone()[0])

    cur.execute("SELECT COUNT(*) FROM expert_scene_stats;")
    print("expert_scene_stats count =", cur.fetchone()[0])

    cur.execute("SELECT scene_type, iso_mean, shutter_mean FROM expert_scene_stats ORDER BY scene_type;")
    print("scene stats preview =", cur.fetchall())
