import numpy as np
import pandas as pd
from cs50 import SQL
from random import randint
from scipy.stats import rv_discrete

db = SQL("sqlite:///qatarwc.db")


class Team:
    """Football team in World Cup"""
    def __init__(self, name, group):
        self.name = name
        self.group = group
        self.points = 0
        self.goals_scored = 0
        self.goals_received = 0
        self.stage = "groups"

    def match(self, scored, received):
        self.goals_scored += scored
        self.goals_received += received
        # Update points depending on result
        if scored > received:
            self.points += 3
        elif scored == received:
            self.points += 1

    def eliminate(self):
        self.stage = 'eliminated'


def create_teams(): 
    """Loads teams from db into Team objects."""
    # Dict of Team instances
    TEAMS = {}   
    for i, team in enumerate(db.execute('SELECT code, "group" FROM teams;')):
        TEAMS[team['code']] = Team(team['code'], team['group'])
    return TEAMS

def simulate_match():
    """
    Returns the final score of a simulated football match. 
    The max goals ever scored in a WC match are 12.
    The max goals scored by one team are 10.
    """
    # Custom probability distribution of total match goals
    xk = range(13)
    pk = (0.09, 0.18, 0.28, 0.24, 0.09, 0.065, 0.025, 0.015, 0.0065, 0.004, 0.002, 0.0015, 0.001)
    pdist = rv_discrete(values=(xk, pk))

    # Generate sample
    total_goals = pdist.rvs() 
    # Assign a portion of goals to one team (max 10)
    t1_goals = randint(total_goals%10,10) if total_goals>10 else randint(0, total_goals)

    # Return score
    return t1_goals, total_goals - t1_goals

def simulate_group_stage(TEAMS):
    """"
    Simulates all the group stage matches according to FIFA rules.
    https://digitalhub.fifa.com/m/2744a0a5e3ded185/original/FIFA-World-Cup-Qatar-2022-Regulations_EN.pdf
    """
    group_matches = db.execute("SELECT match, team1, team2 FROM fixtures WHERE stage = 'group matches';")
    groups_df = pd.DataFrame(group_matches).set_index('match')

    t1_goals=[]
    t2_goals=[]
    for _, row in groups_df.iterrows():
        g1, g2 = simulate_match()
        # Store score
        t1_goals.append(g1)
        t2_goals.append(g2)
        # Update statistics of both teams
        TEAMS[row['team1']].match(g1, g2)
        TEAMS[row['team2']].match(g2, g1)

    groups_df.insert(2, 't1_goals', t1_goals)
    groups_df.insert(3, 't2_goals', t2_goals)

    return(groups_df)

