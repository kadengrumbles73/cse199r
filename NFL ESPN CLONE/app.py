from flask import Flask, render_template
import sqlite3
import os

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "nfl_stats.db")

def get_db_connection():
    conn  = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row 
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    #gets all the teams out of the database
    teams = conn.execute('SELECT * FROM teams').fetchall()
    conn.close()
    return render_template('index.html', teams=teams)

@app.route('/team/<abbr>')
def team_page(abbr):
    # 1. Connect to your database
    conn = get_db_connection()
    
    # 2. Ask SQL for the specific team matching the abbreviation in the URL
    team = conn.execute('SELECT * FROM teams WHERE team_abbr = ?', (abbr,)).fetchone()
    
    # 3. (Optional for now) Ask SQL for that team's games
    games = conn.execute('SELECT * FROM games WHERE home_team = ? OR away_team = ?', (abbr, abbr)).fetchall()
    
    conn.close()

    # 4. Send that specific team data to a new team.html template
    return render_template('team.html', team=team, games=games)

if __name__ == '__main__':
    app.run(debug=True)  