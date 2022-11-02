import os

from flask import Flask, flash, redirect, render_template, request
from cs50 import SQL

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

@app.route("/")
def index():
    # Organize teams and fixtures by groups
    group_teams = dict()
    group_fixtures = dict()
    for g in GROUPS:
        teams = db.execute('SELECT code FROM teams WHERE "group"=?', g)
        group_teams[g] = [team['code'] for team in teams]
        fixtures = db.execute('SELECT * FROM fixtures WHERE team1 IN (SELECT code FROM teams WHERE "group"=?) ORDER BY date;', g)
        group_fixtures[g] = [(match['date'], match['team1'], match['team2']) for match in fixtures]

            
    return render_template("/home.html", groups=GROUPS, teams=group_teams, fixtures=group_fixtures, names=TEAM_CODES)