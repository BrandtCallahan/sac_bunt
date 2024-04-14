# Sacrifice Bunt Simulation (sac_bunt)

Traditional baseball knowledge says that a sacrifice bunt plays a team into a higher likely to score than to play out the inning without a bunt. I have set out to check that knowledge and set up a simulation that will have a teams lineup run through innings that include a sac bunt and innings that do not include a sac bunt. The major distinction in these inning set ups is that with a sac bunt we will have the runner starting on second with 1 out to be the 'sac bunt inning' and nobody on with 0 outs to be the 'swing away inning.'

#### mlb_stats.py
This code will allow you to pull MLB statistics down from baseball-reference (https://www.baseball-reference.com). Within the code you will be able to adjust what seasons you would like to pull. Also I have included a weighting system to have a player's more recent seasons 'weigh' more heavily in the analysis. This weighing will take effect if multiple seasons are selected and it will ultimately be averaged together to have one value to use in the analysis. 

#### pregame_utils.py
Here I will first ask the user to input the team abbreviation for the 'batting' team followed by the 'fielding' team (or opponent). The list of appropriate abbreviations can be found below. Once those are inputted the code will run gathering the statistics for the lineup given (in play_ball.py). The opponent input will be used for their fielding pct, as this will come in play with the simulation trying to account for errors made by the defense.

#### inning_utils.py
There are three major functions leading up to the actual running of an inning that all take shape here. The first is Lineup() which compiles a team's lineup with the players' respective batting stats as well as the opponent's team fielding pct. The second is At_Bat() which runs through a hitter's at-bat and returns the result of that at-bat whether it be a hit, walk, or out. The third is baserunning() which will allow the baserunners to move around the bases dependent on the at-bat's outcome. Finally, we have the inning() function that will allow us to run through an inning and takes in our argument for where to start in the batting lineup, how many outs to start with, and where runners on base will start. 

#### play_ball.py
Here we will actually set up and run our simulation. The batting lineup can be customizable but I have set up to default to the Atlanta Braves '23 Opening Day lineup. Two inning functions will be used, one for the sac bunt and the other for the swing away scenario. The final output will be a dataframe that shows every player with their respective run scoring % with and without the batter executing a sac bunt. 
