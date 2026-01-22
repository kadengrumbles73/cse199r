import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "nfl_stats.db")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check if table exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='players'")
if not cursor.fetchone():
    print("❌ ERROR: The 'players' table does not exist in the database!")
else:
    # Check if data exists
    count = cursor.execute("SELECT COUNT(*) FROM players").fetchone()[0]
    print(f"✅ SUCCESS: Found {count} players in the database.")
    
    # Peek at one player
    sample = cursor.execute("SELECT full_name, team_abbr FROM players LIMIT 1").fetchone()
    if sample:
        print(f"✅ SAMPLE DATA: {sample[0]} is on the {sample[1]}")

conn.close()