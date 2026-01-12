from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn  = sqlite3.connect('nfl_stats.db')
    conn.row_factory = sqlite3.Row 
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    #gets all the teams out of the database
    teams = conn.execute('SELECT * FROM teams').fetchall()
    conn.close()
    return render_template('index.html', teams=teams)

if __name__ == '__main__':
    app.run(debug=True)  