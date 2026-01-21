import sqlite3
import requests

def sync_all_rosters():
    # connect db
    conn = sqlite3.connect('nfl_stats.db')
    cursor = conn.cursor()
    
    # get abbreviations from teams table
    teams = cursor.execute("SELECT team_abbr FROM teams").fetchall()
    
    print(f"Starting sync for {len(teams)}")