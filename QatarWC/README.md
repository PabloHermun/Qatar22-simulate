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

  It makes use of CS50's SQL module to access the database, and the datetime module to handle dates.

  First off, the labels of all existing groups in the database are loaded into the GROUPS list, and the dict TEAM_CODES, relating every team name with its code, is created. Thereafter, only the route `/`is defined, which only accepts the GET method.
  Here, all the information of the database is organized by groups and stored in different lists and dictionaries which will be returned in order to display the calendar in a structured way in the HTML.

  The latter will always be displayed in the page. However if the user requests the route by clicking the *simulate button*, more computations need to be done. This is checked in the `if` statement. If the simulation is not requested (`else` case), the route will return a `0` value. 
  Otherwise, using the functions of `helpers.py`, scores are simulated for all the group-stage matches and then appended to the `group_fixtures` dict to be displayed.
  Additionally the route will return the rankings of each group according to the simulation results.
  
* `helpers.py`: Python file with functions to perform the group-stage simulation and group-ranking computation using a bit of object-oriented programming as well as the numpy, pandas and scipy modules.

  - A Team `class` is created in order to store a team's name and the stats relevant to evaluate if the team will qualify to the knockout round.
  
  - As it's usual in football (soccer if you like) when a team wins it gets 3 points, when it loses it gets 0 points and if there is a tie both teams receive 1 point. This logic is implemented by the function `score2pts`, which receives the goals scored and received by a team during one match and returns the corresponding points.
  - The `create_teams`function returns a TEAMS dict containing a Team instance for each participating team according to the database. The teams' codes are used as keys.
  - The `simulate_score`function returns a random score with a max total of 12 goals (historic WC max) and max of 10 goals scored by a single team. A probability distribution is customized to generate the number of total goals with reasonable occurrence rates.
  - The previous definitions are used within the `simulate_group_stage` function to simulate all the group-stage matches and store the corresponding stats for each team in the TEAMS dict. It finally returns a pandas dataframe containing the results of all matches.
  - The most complex task of the project is implemented via the `get_group_rank` function. 
  To define the final rank-position of each team in a given group, the [FIFA rules](https://digitalhub.fifa.com/m/2744a0a5e3ded185/original/FIFA-World-Cup-Qatar-2022-Regulations_EN.pdf) were consulted.
  First, all the team-codes given as input are used to search the respective team-objects in TEAMS, from which the name, points, goal difference and goals scored are extracted.
  Hence a table of the group teams is organized into the `group_df` dataframe to then be sorted by the number of points, goal difference, and goals scored, in that preference order.

  If no teams out of the first 3 (since only 1st and 2nd matter[<u>this could be upgraded<u>]) are tied on all the criteria, return group_df as it is.
  If there are ties, a new rank (with the same columns) is computed just for the tied teams, but only considering the matches between them.
  This tie-break table is finally complemented with the original ranking and returned, together with a string reporting the criteria used to break the tie. The latter is used in the HTML to mark the group ranking with an asterisk if tie-breaks had to be computed.

* `home.html`: The client side consist of only this one HTML file.
  In the `<head>` element of the file, you can see that some external API's are used. Bootstrap is used for the style of the page. A cloudinary api is used to load the flags of all countries remotely. And another api is used to get the typography for the Qatar title.

  The page is divided into two sections, one for the group-stage simulation and another one for the KO-stages simulation. Both sections can be accessed from the navbar.

  The first section displays the calendar of matches organized by groups, by iterating with Jinja code over the data provided by the server-side (see `app.py`).
  There is only one interactive button in the section which makes a request for the simulation to take place (in the server) and then the page is reloaded and displays all the results and rankings returned from the simulation. Notice that there are a few lines of commented HTML code. These are intended to display one button for each group that would allow to simulate a single group at a time. This will be implemented in the future.

  The second section consist of a grid where all the flags of the KO-stages' contenders will be display as they progress in the 'bracket' during the simulation. When the group-stage simulation is executed the qualified teams of each group are collocated in their corresponding spot of the round of 16. 
  There are several buttons that the user can use to simulate the KO-stages one by one or all at once.
  All the functionality of this section is implemented on the client-side with the `ko_simulate.js` file.

* `stles.css`: This stylesheet contains a few lines only to set the main colors of the website. Additionally a `.btn-container`style is defined for the group buttons that will be implemented in the future.

* `ko_simulate.js`: JavaScript file containing four functions that build up the functionality of the KO-stages section of the site:

  - The first anonymous function fills the R16 grid spots with the flags corresponding to the qualified teams playing each game, as long as the group-stage simulation has ben executed.
  
  - The `sim_r16` function implements the simulation of the round of 16. Using the `rand_winner` function, one of each pair of flags is selected as the winner of the corresponding match and used to populate the QF spots of the grid as the FIFA calendar dictates. The looser flag is also reduced in opacity.

  - The `sim_ko_games` function implements the simulation of a range of games which are labeled with their corresponding number of game from the database using css selectors. Similarly to the `sim_r16` function, it randomly selects a winner of each match and populates the corresponding spots of the next round.
  Finally it customizes the style of the finalists and champion for a better design.

* `requirements.txt`: The flask requirements file contains the names of the python libraries used.

THIS WAS CS50!
