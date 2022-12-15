import numpy as np
import pandas as pd
from cs50 import SQL
from scipy.stats import rv_discrete

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///qatarwc.db")


class Team:
    """Football team in World Cup"""
    def __init__(self, name, group):
        self.name = name
        self.group = group
        self.points = 0
        self.goals_scored = 0
        self.goals_received = 0

    def match(self, scored, received):
        self.goals_scored += scored
        self.goals_received += received
        # Update points depending on score
        self.points += score2pts(scored, received)

def score2pts(scored, received):
    """Given a score, returns the number of points for one team."""
    if scored > received:
            return 3
    elif scored == received:
            return 1
    else:
        return 0

def create_teams(): 
    """Loads teams from db into Team objects."""
    # Dict of Team instances
    TEAMS = {}   
    for i, team in enumerate(db.execute('SELECT code, "group" FROM teams;')):
        TEAMS[team['code']] = Team(team['code'], team['group'])
    return TEAMS


def simulate_score():
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
    t1_goals = np.random.randint(total_goals%10,11) if total_goals>10 else np.random.randint(0, total_goals + 1)

    # Return score
    return t1_goals, total_goals - t1_goals

def simulate_group_stage(TEAMS):
    """"
    Simulates all the group stage matches
    """
    group_matches = db.execute("SELECT match, team1, team2 FROM fixtures WHERE stage = 'group matches';")
    groups_df = pd.DataFrame(group_matches).set_index('match')

    t1_goals=[]
    t2_goals=[]
    for _, row in groups_df.iterrows():
        g1, g2 = simulate_score()
        # Store score
        t1_goals.append(g1)
        t2_goals.append(g2)
        # Update statistics of both teams
        TEAMS[row['team1']].match(g1, g2)
        TEAMS[row['team2']].match(g2, g1)

    groups_df.insert(2, 't1_goals', t1_goals)
    groups_df.insert(3, 't2_goals', t2_goals)

    return(groups_df)

def get_group_rank(label, team_names, TEAMS, fixtures):
    """
    Obtains the ranking of a given group according to FIFA rules:
    https://digitalhub.fifa.com/m/2744a0a5e3ded185/original/FIFA-World-Cup-Qatar-2022-Regulations_EN.pdf
    Return a dict of [position: team] values and the criteria used for tie-break (if necessary)
    """
    
    # Create a list of relevant group stats
    group_stats = list()
    for team in team_names:
        t = TEAMS[team]
        group_stats.append([t.name, t.points, t.goals_scored - t.goals_received, t.goals_scored])
        
    # Order teams by pts, gdf and gs (CRITERIA (a)-(c))
    group_df = pd.DataFrame(group_stats, columns=['team','pts','gdf', 'gs']).sort_values(['pts','gdf','gs'], ascending=[False, False, False])
    group_df.index = [1,2,3,4]
    #print(group_df)
    
    # Check if two or more teams (out of the first 3) are still tied
    dups = group_df.duplicated(subset=['pts','gdf','gs'], keep=False)
    is_tied = dups[0:3].sum()
    if is_tied <= 1:
        # No ties
        return group_df[['team']].to_dict()['team'], 'a-c'
    
    # Consider matches among tied teams
    tied_teams = group_df[dups]['team'].to_list()
    tiebreak = dict() # Stores pts, gdf and gs only from those mathces (CRITERIA (d)-(f))
    
    if group_df[dups].drop_duplicates(subset=['pts','gdf','gs']).shape[0] != 1:
    # If there are two pairs of tied teams (i.e. 1&2 and 3&4) we only care about 1&2
        tied_teams = tied_teams[:2]
        
    for match in fixtures:
        # Select matches of interest
        if match['t1'] in tied_teams and match['t2'] in tied_teams:
            # Store stats
            g1, g2 = match['t1_goals'], match['t2_goals']
            if match['t1'] not in tiebreak:
                tiebreak[match['t1']] = np.asarray([score2pts(g1, g2), g1-g2, g1])
            else:
                tiebreak[match['t1']] += np.asarray([score2pts(g1, g2), g1-g2, g1])

            if match['t2'] not in tiebreak:
                tiebreak[match['t2']] = np.asarray([score2pts(g2, g1), g2-g1, g2])
            else:
                tiebreak[match['t2']] += np.asarray([score2pts(g2, g1), g2-g1, g2])
            #print(match)
            
    # Order tied teams 
    tbreak = pd.DataFrame.from_dict(tiebreak, orient='index', columns=['pts','gdf', 'gs']).sort_values(['pts','gdf','gs'], ascending=[False, False, False])
    #print(tbreak)
    
    # Rebuilt table of positions after tie-break
    positions=dict()
    j=0
    for i in range(1,5):
        if dups[i] == True:
            positions[i] = tbreak.index[j]
            j += 1
        else:
            positions[i] = group_df.iloc[i-1]['team']
    
    # If there are still ties the remaining criteria are not handled here (CRITERIA (g) & (h)))
    dups = tbreak.duplicated(subset=['pts','gdf','gs'], keep=False)
    is_tied = dups.sum()
    
    if is_tied <= 0:
        return positions, 'd-f'

    else:
        return positions, 'g-h'