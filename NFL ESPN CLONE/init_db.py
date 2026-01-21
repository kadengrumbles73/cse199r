import sqlite3
import nfl_data_py as nfl

def init_db():
    print("Connecting to database...")
    # creates database file
    conn = sqlite3.connect('nfl_stats.db')
    
    print("Downloading NFL team data (this may take a minute)...")
    # fetches data from the NFL API
    teams = nfl.import_team_desc()
    
    # saves data in db
    teams.to_sql('teams', conn, if_exists='replace', index=False)
    
    conn.close()
    print("Success! Database Ready.") 

import sqlite3

def init_players_table():
    """
    Creates the players table in the nfl_stats database if it doesn't already exist.
    """
    try:
        # Connect db
        with sqlite3.connect('nfl_stats.db') as conn:
            cursor = conn.cursor()
            
            #Define players table
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
            print("Players table is ready (created or already exists).")
            
    except sqlite3.Error as e:
        print(f"Database error: {e}")

# To run it, just call the function at the bottom of the file
if __name__ == "__main__":
    init_db() 
    init_players_table()
