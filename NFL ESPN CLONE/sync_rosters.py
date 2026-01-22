import sqlite3
import requests
import os

# Use the same absolute path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "nfl_stats.db")

def sync_all_rosters():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # get abbreviations from teams table
    teams = cursor.execute("SELECT team_abbr FROM teams").fetchall()
    print(f"Starting sync for {len(teams)} teams...")
    
    for (abbr,) in teams:
        # ESPN uses 'WSH' for Washington
        api_abbr = 'WSH' if abbr == 'WAS' else abbr
        url = f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{api_abbr}/roster"
        
        try:
            response = requests.get(url)
            data = response.json()
            
            if 'athletes' in data:
                for group in data.get('athletes', []):
                    for athlete in group.get('items', []):
                        player_data = (
                            athlete.get("id"),
                            abbr,
                            athlete.get('fullName'),
                            athlete.get('position', {}).get('abbreviation'),
                            athlete.get('jersey'),
                            athlete.get('headshot', {}).get('href'),
                        )
                        # Save athlete to the correct table
                        cursor.execute('''
                            INSERT OR REPLACE INTO players 
                            (player_id, team_abbr, full_name, position, jersey_number, headshot_url)
                            VALUES (?, ?, ?, ?, ?, ?)
                        ''', player_data)
                print(f"Synced {abbr}")
        except Exception as e:
            print(f"Failed to sync {abbr}: {e}")
        conn.commit()
    conn.close()
    print("Done! Your rosters are full.")
    
if __name__ == "__main__":
    sync_all_rosters()