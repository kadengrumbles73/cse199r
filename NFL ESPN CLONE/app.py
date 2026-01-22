from flask import Flask, render_template
import sqlite3
import os

app = Flask(__name__)
# Absolute path to match the other scripts
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "nfl_stats.db")

def get_db_connection():
    conn  = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row 
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    teams = conn.execute('SELECT * FROM teams').fetchall()
    conn.close()
    return render_template('index.html', teams=teams)

@app.route('/team/<abbr>')
def team_page(abbr):
    conn = get_db_connection()
    team = conn.execute('SELECT * FROM teams WHERE team_abbr = ?', (abbr,)).fetchone()
    # Query must match the 'team_abbr' column filled by sync_rosters
    players = conn.execute('SELECT * FROM players WHERE team_abbr = ?', (abbr,)).fetchall()
    conn.close()
    return render_template('team.html', team=team, players=players)

if __name__ == '__main__':
    app.run(debug=True)