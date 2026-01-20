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

if __name__ == "__main__":
    init_db() 