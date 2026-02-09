from flask import Flask, render_template
import sqlite3
import os
import requests

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "nfl_stats.db")

def get_db_connection():
    conn = sqlite3.connect(db_path)
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
    players = conn.execute('SELECT * FROM players WHERE team_abbr = ?', (abbr,)).fetchall()
    conn.close()
    return render_template('team.html', team=team, players=players)

@app.route('/scores')
@app.route('/scores/<int:week_num>')
def scores(week_num=None):
    # API URL targeting 2025 Regular Season
    url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
    
    # seasontype 2 = Regular Season
    params = {
        'dates': '2025',
        'seasontype': '2'
    }
    
    if week_num:
        params['week'] = week_num
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        games = data.get('events', [])
        
        # Pull week number from API if not specified
        display_week = week_num if week_num else data.get('week', {}).get('number', 1)
        
        return render_template('scores.html', games=games, week=display_week)
    except Exception as e:
        print(f"Error: {e}")
        return "Scoreboard unavailable.", 500

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)