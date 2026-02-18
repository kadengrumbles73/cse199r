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
    teams = conn.execute('SELECT * FROM teams ORDER BY team_conf, team_division').fetchall()
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
@app.route('/scores/<int:year>/<int:season_type>/<int:week_num>')
def scores(year=2025, season_type=2, week_num=1):
    # ESPN API Endpoint
    url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
    
    # params: seasontype 2 = Regular, 3 = Postseason
    params = {
        'dates': str(year),
        'seasontype': str(season_type),
        'week': str(week_num)
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        games = data.get('events', [])
        
        # Determine current week for the header title if needed
        # We pass the parameters back to the template to keep the dropdowns synced
        return render_template(
            'scores.html', 
            games=games, 
            current_year=year, 
            current_season=season_type, 
            current_week=week_num
        )
    except Exception as e:
        print(f"Error: {e}")
        return "Scoreboard unavailable.", 500

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)