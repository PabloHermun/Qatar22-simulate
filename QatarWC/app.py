import os

from flask import Flask, flash, redirect, render_template, request, session
from cs50 import SQL
from datetime import datetime

from helpers import Team, create_teams, simulate_match, simulate_group_stage

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///qatarwc.db")

# Load the labels of all groups
group_labels = db.execute('SELECT DISTINCT "group" FROM teams') # Returns a list of dicts
GROUPS = [list(d.values())[0] for d in group_labels]
# Load code: team dict 
TEAM_CODES = db.execute('SELECT code, team FROM teams;')
TEAM_CODES = {team['code']:team['team'] for team in TEAM_CODES}

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
def index():

    TEAMS = create_teams()
    scores = simulate_group_stage(TEAMS).to_dict('index')
    # Organize teams and fixtures by groups
    group_teams = dict()
    group_fixtures = dict()
    for g in GROUPS:
        teams = db.execute('SELECT code FROM teams WHERE "group"=?', g)
        group_teams[g] = [team['code'] for team in teams]

        fixtures = db.execute('SELECT * FROM fixtures WHERE team1 IN (SELECT code FROM teams WHERE "group"=?) ORDER BY date;', g)
        # Change date formant e.g. 2022-12-02 into "Dec 02"
        group_fixtures[g] = [{'date': datetime.strptime(match['date'], "%Y-%m-%d").strftime("%b %d"),
                             'id':match['match'], 't1': match['team1'], 't2' :match['team2'], 
                             't1_goals': scores[match['match']]['t1_goals'],
                             't2_goals': scores[match['match']]['t2_goals']} for match in fixtures]
    
    if request.method == 'GET':
        simulate = request.args.get("match_id")
        score = simulate_match()

    else:
        simulate = None
        score = None
            
    return render_template("/home.html", groups=GROUPS, zip=zip, teams=group_teams, fixtures=group_fixtures, names=TEAM_CODES, simulate=simulate, score=score)