import sqlite3

conn = sqlite3.connect('nfl_stats.db')
cursor = conn.cursor()

# 1. Define the 32 current team abbreviations
current_teams = (
    'ARI', 'ATL', 'BAL', 'BUF', 'CAR', 'CHI', 'CIN', 'CLE',
    'DAL', 'DEN', 'DET', 'GB', 'HOU', 'IND', 'JAX', 'KC',
    'LV', 'LAC', 'LAR', 'MIA', 'MIN', 'NE', 'NO', 'NYG',
    'NYJ', 'PHI', 'PIT', 'SEA', 'SF', 'TB', 'TEN', 'WAS'
)

# 2. Delete any team NOT in that list
cursor.execute('DELETE FROM teams WHERE team_abbr NOT IN ({})'.format(
    ','.join(['?'] * len(current_teams))), current_teams)

# 3. Save and close
conn.commit()
conn.close()

print("Cleaned up! Only the current 32 teams remain.")