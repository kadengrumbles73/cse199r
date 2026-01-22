import sqlite3
import nfl_data_py as nfl
import os

# Define absolute path to the database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "nfl_stats.db")

def init_db():
    print("Connecting to database...")
    conn = sqlite3.connect(DB_PATH)
    
    print("Downloading NFL team data...")
    teams = nfl.import_team_desc()
    
    # Saves teams to database
    teams.to_sql('teams', conn, if_exists='replace', index=False)
    
    # Run the cleanup to keep only 32 teams
    clean_data(conn)
    conn.close()
    print("Success! Teams table ready and cleaned.") 

def init_players_table():
    print("Creating players table structure...")
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            # This creates the table that sync_rosters.py is looking for
            create_table_sql = """
            CREATE TABLE IF NOT EXISTS players (
                player_id INTEGER PRIMARY KEY,
                team_abbr TEXT,
                full_name TEXT,
                position TEXT,
                jersey_number TEXT,
                headshot_url TEXT,
                FOREIGN KEY (team_abbr) REFERENCES teams (team_abbr)
            );
            """
            cursor.execute(create_table_sql)
            conn.commit()
            print("Success! Players table is now ready for syncing.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")

def clean_data(conn):
    cursor = conn.cursor()
    current_teams = (
        'ARI', 'ATL', 'BAL', 'BUF', 'CAR', 'CHI', 'CIN', 'CLE',
        'DAL', 'DEN', 'DET', 'GB', 'HOU', 'IND', 'JAX', 'KC',
        'LV', 'LAC', 'LAR', 'MIA', 'MIN', 'NE', 'NO', 'NYG',
        'NYJ', 'PHI', 'PIT', 'SEA', 'SF', 'TB', 'TEN', 'WAS'
    )
    cursor.execute('DELETE FROM teams WHERE team_abbr NOT IN ({})'.format(
        ','.join(['?'] * len(current_teams))), current_teams)
    conn.commit()

if __name__ == "__main__":
    init_db() 
    init_players_table()