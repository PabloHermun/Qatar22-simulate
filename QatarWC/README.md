# Qatar2022 World Cup Simulator
#### Video Demo:  <[QWC Simulator](https://youtu.be/xfvCNBkWF8U)>
#### Description: 

> This project consist of a Flask web application that allows the user to simulate all the stages of the 2022 FIFA world cup.


The project contains the following files:

* `qatarwc.db`: A SQL database file containing two tables:
  - The `teams` table containing the name of the teams qualified to the 2022 WC, their 3-letter code, and their assigned group.
  - The `fixture` table containing the number of match, the date, the codes of the two teams playing and the correspondent stage of the tournament.

  All the data in these tables was extracted from the csv files contained in the `static/data` folder using SQLite 3. 
  Those csv files were first obtained from [Kaggle](https://www.kaggle.com/datasets/amineteffal/qatar2022worldcupschudule?resource=download) and then modified with the python scripts saved in the `static/data` folder. <br>
  Finally, the *code* field was set as a UNIQUE INDEX in the `.db`file.
  
* `app.py`: The main file of the Flask application. 

  It makes use of CS50's SQL module to acces the database, and the datetime module to handle dates.

  First off, the labels of all existing groups in the database are loaded into the GROUPS list, and the dict TEAM_CODES, relating every team name with its code, is created. Thereafter, only the route `/`is defined, which only accepts the GET method.
Here, all the information of the database is organized by groups and stored in different lists and dictionaries which will be returned in order to display the calendar in a structured way in the HTML.

  The latter will always be displayed in the page. However if the user requests the route by clicking the *simulate button* more computations need to be done. This is checked in the `if` statement. If the simulation is not requested (`else` case), the route will return a `0` value. 
  Otherwise, using the functions of `helpers.py`, scores are simulated for all the group-stage matches and then appended to the `group_fixtures` dict to be displayed.
  Additionally the route will return the rankigs of each group according to the simulation results.
  
* `helpers.py`: Python file with functions to perform the group-stage simulation and group-ranking computation using a bit of object-oriented programming as well as the numpy, pandas and scipy modules.

  - A Team `class` is created in order to store a team's name, group, and the stats relevant to evaluate if the team will qualify to the knockout round.
  
  - As it's usual in football (soccer if you like) when a team wins it gets 3 points, when it loses it gets 0 points and if there is a tie both teams receive 1 point. This logic is implemented by the function `score2pts`, which receives the goals scored and received by a team during one match and returns the corresponding points.
  - The `create_teams`function returns a TEAMS dict containing a Team instance for each participating team according to the database. The teams' codes are used as keys.
  - The `simulate_score`function returns a random score with a max total of 12 goals (historic WC max) and max of 10 goals scored by a single team. A probability distribution is customized to generate the number of total goals with reasonable ocurrence rates.
  - The `simulate_group_stage` uses the previous definitions to simulate all the group-stage matches and store the corresponding stats for every team in the TEAMS dict. It finally returns a pandas dataframe containing the results of all matches.
  - get_group_rank

* `home.html`
* `stles.css`
* `ko_simulate.js`

* `requirements.txt`: contains the names of the python libraries used.
