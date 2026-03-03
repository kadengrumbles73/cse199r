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
    # Sort by conference and division to ensure consistent grouping
    teams_raw = conn.execute('SELECT * FROM teams ORDER BY team_conf, team_division').fetchall()
    conn.close()

    grouped_teams = {}
    for team in teams_raw:
        conf = team['team_conf']
        div = team['team_division']
        if conf not in grouped_teams:
            grouped_teams[conf] = {}
        if div not in grouped_teams[conf]:
            grouped_teams[conf][div] = []
        grouped_teams[conf][div].append(team)

    return render_template('index.html', conferences=grouped_teams)

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
    url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
    params = {'dates': str(year), 'seasontype': str(season_type), 'week': str(week_num)}
    try:
        response = requests.get(url, params=params)
        data = response.json()
        raw_games = data.get('events', [])
        
        # --- SMART FILTER ---
        # 1. Keep the game if it's the Super Bowl (based on the name)
        # 2. Otherwise, filter out AFC/NFC Pro Bowl teams
        games = []
        for game in raw_games:
            game_name = game.get('name', '').lower()
            is_super_bowl = "super bowl" in game_name
            
            away_abbr = game['competitions'][0]['competitors'][1]['team']['abbreviation']
            home_abbr = game['competitions'][0]['competitors'][0]['team']['abbreviation']
            
            if is_super_bowl:
                games.append(game)
            elif away_abbr not in ['AFC', 'NFC'] and home_abbr not in ['AFC', 'NFC']:
                games.append(game)
        
        return render_template('scores.html', games=games, current_year=year, 
                               current_season=season_type, current_week=week_num)
    except Exception as e:
        print(f"Scores Error: {e}")
        return "Scoreboard Error", 500
        
@app.route('/game/<event_id>')
def game_stats(event_id):
    # ESPN Game Summary Endpoint for high-density stats
    url = f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/summary?event={event_id}"
    try:
        response = requests.get(url)
        data = response.json()
        
        # Extracting specific data for the game_stats.html template
        header = data.get('header', {})
        boxscore = data.get('boxscore', {})
        pickcenter = data.get('pickcenter', [])
        
        return render_template('game_stats.html', 
                               header=header, 
                               boxscore=boxscore, 
                               odds=pickcenter[0] if pickcenter else None)
    except Exception as e:
        print(f"Error: {e}")
        return "Game Stats Error", 500

if __name__ == '__main__':
    app.run(debug=True)