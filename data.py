# Begin by importing the necessary libraries and modules.
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
from tabulate import tabulate
from scipy import stats

# # Load the data (Stored in the CFBdata folder)
# data17 = pd.read_csv('CFBdata/cfb17.csv')
# data18 = pd.read_csv('CFBdata/cfb18.csv')
# data19 = pd.read_csv('CFBdata/cfb19.csv')
# data20 = pd.read_csv('CFBdata/cfb20.csv')
# data21 = pd.read_csv('CFBdata/cfb21.csv')
# data22 = pd.read_csv('CFBdata/cfb22.csv')
# data23 = pd.read_csv('CFBdata/cfb23.csv')

# # Take the CFB division out of the team name (The division is in the parentheses)
# data17['Team'] = data17['Team'].str.split('(').str[0]
# data18['Team'] = data18['Team'].str.split('(').str[0]
# data19['Team'] = data19['Team'].str.split('(').str[0]
# data20['Team'] = data20['Team'].str.split('(').str[0]
# data21['Team'] = data21['Team'].str.split('(').str[0]
# data22['Team'] = data22['Team'].str.split('(').str[0]
# data23['Team'] = data23['Team'].str.split('(').str[0]

# # Update the files with the new team names (Create a function)
# def update_files():
#     data17.to_csv('CFBdata/cfb17.csv', index=False)
#     data18.to_csv('CFBdata/cfb18.csv', index=False)
#     data19.to_csv('CFBdata/cfb19.csv', index=False)
#     data20.to_csv('CFBdata/cfb20.csv', index=False)
#     data21.to_csv('CFBdata/cfb21.csv', index=False)
#     data22.to_csv('CFBdata/cfb22.csv', index=False)
#     data23.to_csv('CFBdata/cfb23.csv', index=False)


# Great! Now we have our main dataframe.
# Load the main data (Stored in the CFBdata folder)
data = pd.read_csv('CFBdata/cfb.csv')

# Keep in mind that all column names are lowercase

years = ['2017', '2018', '2019', '2020', '2021', '2022', '2023']

# Create a dictionary to store the averages of several categorical statistics for a team
def getAverages(team):
    # Get all instances of the team. Do this by looking for every occurance of the team name (minus the year)
    # in the team column. However, we must look for identical matches, as you do not want to be looking for say
    # South Alabama, and pick up Alabama on accident.
    instances = []
    for index, row in data.iterrows():
        # Check if the team name is the same as the team we are looking for
        # To do so, ignore the last 4 characters of the team name (the year)
        if row['team'][:-5] == team:
            instances.append(row)

    # Now that we have all instances of the team, we can calculate the averages of the statistics
    # We will store the averages in a dictionary
    averageStats = {}

    # Get the averages for win, loss, off_yards_per_game, yards_per_game_allowed, rush_yards_per_game, pass_yards_per_game,
    # avg_points_per_game_allowed, points_per_game, 4th_percent, opponent_4th_percent, 3rd_percent,
    # opponent_3rd_percent, avg_turnover_margin_per_game
    wins = []
    losses = []
    off_yards_per_game = []
    yards_per_game_allowed = []
    rushing_yards_per_game = []
    rush_yards_per_game_allowed = []
    pass_yards_per_game = []
    pass_yards_per_game_allowed = []
    avg_points_per_game_allowed = []
    points_per_game = []
    fourth_percent = []
    opponent_fourth_percent = []
    third_percent = []
    opponent_third_percent = []
    avg_turnover_margin_per_game = []
    for instance in instances:
        wins.append(instance['win'])
        losses.append(instance['loss'])
        off_yards_per_game.append(instance['off_yards_per_game'])
        yards_per_game_allowed.append(instance['yards_per_game_allowed'])
        rushing_yards_per_game.append(instance['rushing_yards_per_game'])
        rush_yards_per_game_allowed.append(instance['rush_yards_per_game_allowed'])
        pass_yards_per_game.append(instance['pass_yards_per_game'])
        pass_yards_per_game_allowed.append(instance['pass_yards_per_game_allowed'])
        avg_points_per_game_allowed.append(instance['avg_points_per_game_allowed'])
        points_per_game.append(instance['points_per_game'])
        fourth_percent.append(instance['4th_percent'])
        opponent_fourth_percent.append(instance['opponent_4th_percent'])
        third_percent.append(instance['3rd_percent'])
        opponent_third_percent.append(instance['opponent_3rd_percent'])
        avg_turnover_margin_per_game.append(instance['avg_turnover_margin_per_game'])

    # Convert all the lists to numpy arrays with doubles
    wins = np.array(wins, dtype=np.double)
    losses = np.array(losses, dtype=np.double)
    off_yards_per_game = np.array(off_yards_per_game, dtype=np.double)
    yards_per_game_allowed = np.array(yards_per_game_allowed, dtype=np.double)
    rushing_yards_per_game = np.array(rushing_yards_per_game, dtype=np.double)
    rush_yards_per_game_allowed = np.array(rush_yards_per_game_allowed, dtype=np.double)
    pass_yards_per_game = np.array(pass_yards_per_game, dtype=np.double)
    pass_yards_per_game_allowed = np.array(pass_yards_per_game_allowed, dtype=np.double)
    avg_points_per_game_allowed = np.array(avg_points_per_game_allowed, dtype=np.double)
    points_per_game = np.array(points_per_game, dtype=np.double)
    fourth_percent = np.array(fourth_percent, dtype=np.double)
    opponent_fourth_percent = np.array(opponent_fourth_percent, dtype=np.double)
    third_percent = np.array(third_percent, dtype=np.double)
    opponent_third_percent = np.array(opponent_third_percent, dtype=np.double)
    avg_turnover_margin_per_game = np.array(avg_turnover_margin_per_game, dtype=np.double)

    # Calculate the averages
    averageStats['team'] = team
    # Instead of calculating the averages, simply store the lists of each statistic in the dictionary as the value for the key
    # But first, convert all the values in all the lists to valid doubles
    averageStats['win'] = wins
    averageStats['loss'] = losses
    averageStats['off_yards_per_game'] = off_yards_per_game
    averageStats['yards_per_game_allowed'] = yards_per_game_allowed
    averageStats['rushing_yards_per_game'] = rushing_yards_per_game
    averageStats['rush_yards_per_game_allowed'] = rush_yards_per_game_allowed
    averageStats['pass_yards_per_game'] = pass_yards_per_game
    averageStats['pass_yards_per_game_allowed'] = pass_yards_per_game_allowed
    averageStats['avg_points_per_game_allowed'] = avg_points_per_game_allowed
    averageStats['points_per_game'] = points_per_game
    averageStats['fourth_percent'] = fourth_percent
    averageStats['opponent_fourth_percent'] = opponent_fourth_percent
    averageStats['third_percent'] = third_percent
    averageStats['opponent_third_percent'] = opponent_third_percent
    averageStats['avg_turnover_margin_per_game'] = avg_turnover_margin_per_game

    # averageStats['win'] = round(np.mean(wins), 3)
    # averageStats['loss'] = round(np.mean(losses), 3)
    # averageStats['off_yards_per_game'] = round(np.mean(off_yards_per_game), 3)
    # averageStats['yards_per_game_allowed'] = round(np.mean(yards_per_game_allowed), 3)
    # averageStats['rushing_yards_per_game'] = round(np.mean(rushing_yards_per_game), 3)
    # averageStats['rush_yards_per_game_allowed'] = round(np.mean(rush_yards_per_game_allowed), 3)
    # averageStats['pass_yards_per_game'] = round(np.mean(pass_yards_per_game), 3)
    # averageStats['pass_yards_per_game_allowed'] = round(np.mean(pass_yards_per_game_allowed), 3)
    # averageStats['avg_points_per_game_allowed'] = round(np.mean(avg_points_per_game_allowed), 3)
    # averageStats['points_per_game'] = round(np.mean(points_per_game), 3)
    # averageStats['fourth_percent'] = round(np.mean(fourth_percent), 3)
    # averageStats['opponent_fourth_percent'] = round(np.mean(opponent_fourth_percent), 3)
    # averageStats['third_percent'] = round(np.mean(third_percent), 3)
    # averageStats['opponent_third_percent'] = round(np.mean(opponent_third_percent), 3)
    # averageStats['avg_turnover_margin_per_game'] = round(np.mean(avg_turnover_margin_per_game), 3)

    return averageStats


# # Find all instances of a team with name Alabama and a year in its name, and print out the wins
# for index, row in data.iterrows():
#     if 'Alabama' in row['team'] and '2021' in row['team']:
#         print(row['win'])
#
# # print the name of all teams with Alabama in the team name
# for index, row in data.iterrows():
#     if 'Alabama' in row['team']:
#         print(row['team'])
#
# # How can I write the above code to account for the fact that some teams have the word Alabama in the name but are not
# # the same team as Alabama. For instance, South Alabama.
# # I can use the split method to split the team name by the space character and then check if the first word is Alabama
# for year in years:
#     for index, row in data.iterrows():
#         if row['team'].split(' ')[0] == 'Alabama' and year in row['team']:
#             print(row['team'])
#             print(row['win'])
#
# # Do the same thing as the above code, except just print the average wins for the team
# wins = []
# for year in years:
#     for index, row in data.iterrows():
#         if row['team'].split(' ')[0] == 'Alabama' and year in row['team']:
#             wins.append(row['win'])
# print(wins)
# # Convert the list of wins to a list of ints
# wins = [int(i) for i in wins]
# print(np.mean(wins))

# Create a function that, given the dictionary of averages, will print out the top 3 statistics positiively correlated with wins, and the top 3 statistics negatively correlated with wins
def getTopStats(averages):
    # Get the correlation between wins and all the other statistics
    correlations = {}
    for key in averages:
        if key != 'team' and key != 'win' and key != 'loss':
            correlations[key] = np.corrcoef(averages['win'], averages[key])[0][1]

    # Sort the correlations
    sorted_correlations = sorted(correlations.items(), key=lambda x: x[1], reverse=True)

    # Print out the top 3 positively correlated statistics
    top_three_positively_correlated_wins = []
    for i in range(3):
        # Store these top 3 statistics for later access (round them to 5 decimal places)
        top_three_positively_correlated_wins.append((sorted_correlations[i][0], round(sorted_correlations[i][1], 5)))

    # Print out the top 3 negatively correlated statistics
    top_three_negatively_correlated_wins = []
    for i in range(3):
        # Store these top 3 statistics for later access (round them to 5 decimal places)
        top_three_negatively_correlated_wins.append((sorted_correlations[-i-1][0], round(sorted_correlations[-i-1][1], 5)))

    # Also find the top 3 statistics that are positively correlated with losses and the top 3 statistics that are negatively correlated with losses
    correlations = {}
    for key in averages:
        if key != 'team' and key != 'win' and key != 'loss':
            correlations[key] = np.corrcoef(averages['loss'], averages[key])[0][1]

    # Sort the correlations
    sorted_correlations = sorted(correlations.items(), key=lambda x: x[1], reverse=True)

    # Print out the top 3 positively correlated statistics
    top_three_positively_correlated_losses = []
    for i in range(3):
        # Store these top 3 statistics for later access (round them to 5 decimal places)
        top_three_positively_correlated_losses.append((sorted_correlations[i][0], round(sorted_correlations[i][1], 5)))

    # Print out the top 3 negatively correlated statistics
    top_three_negatively_correlated_losses = []
    for i in range(3):
        # Store these top 3 statistics for later access (round them to 5 decimal places)
        top_three_negatively_correlated_losses.append((sorted_correlations[-i-1][0], round(sorted_correlations[-i-1][1], 5)))

    # # Print out our stored results in a nice format
    # print('Top 3 positively correlated statistics with wins:')
    # for stat in top_three_positively_correlated_wins:
    #     print(stat[0] + ': ' + str(stat[1]))
    # print('Top 3 negatively correlated statistics with wins:')
    # for stat in top_three_negatively_correlated_wins:
    #     print(stat[0] + ': ' + str(stat[1]))
    # print('Top 3 positively correlated statistics with losses:')
    # for stat in top_three_positively_correlated_losses:
    #     print(stat[0] + ': ' + str(stat[1]))
    # print('Top 3 negatively correlated statistics with losses:')
    # for stat in top_three_negatively_correlated_losses:
    #     print(stat[0] + ': ' + str(stat[1]))

    # Store our results in a table
    results = pd.DataFrame(columns=['Statistic', 'Correlation with Wins', 'Correlation with Losses'])

    # Fill the dataframe with the results
    for i in range(3):
        # We cannot use append because dataframes do not have that method
        results.loc[i] = [top_three_positively_correlated_wins[i][0], top_three_positively_correlated_wins[i][1], top_three_positively_correlated_losses[i][1]]
    for i in range(3):
        results.loc[i+3] = [top_three_negatively_correlated_wins[i][0], top_three_negatively_correlated_wins[i][1], top_three_negatively_correlated_losses[i][1]]

    return results

def print_table(df):
    print(tabulate(df, headers='keys', tablefmt='pretty'))

#print(getAverages('South Alabama'))
averages = getAverages('South Alabama')

test = getTopStats(averages)

# Get rid of the index column
test = test.set_index('Statistic')

# Knowing what we now know about the correlation between wins and the other statistics, we can now create a function
# that will predict which team will win a game between two teams based on the statistics of the two teams
# First, make sure we take into account the statistics with the highest correlation with wins
# We will use the linear regression model to predict the winner of the game
# We will use the statsmodels library to do this
import statsmodels.api as sm

# Create a function that will predict the winner of a game between two teams
def predict_winner(team1, team2):
    # Keep in mind the stats that have the highest correlation with wins
    # We will use the stats that have the highest correlation with wins
    # Get the averages for both teams (using the getAverages function)
    averagesTeam1 = getAverages(team1)
    averagesTeam2 = getAverages(team2)

    # Get the top 3 stats that are positively correlated with wins for both teams
    topStatsTeam1 = getTopStats(averagesTeam1)
    topStatsTeam2 = getTopStats(averagesTeam2)

    # Get the stats that are positively correlated with wins for both teams and store them properly.
    statsTeam1PositivelyCorrelatedWins = topStatsTeam1['Statistic'][:3]
    statsTeam2PositivelyCorrelatedWins = topStatsTeam2['Statistic'][:3]

    # Figure out which team does better in the stats that are positively correlated with wins
    # If a team does better in a stat, give them a point
    team1Points = 0
    team2Points = 0

    # Add a point to the team that does better in the stats that are positively correlated with wins
    for stat in statsTeam1PositivelyCorrelatedWins:
        if averagesTeam1[stat].mean() > averagesTeam2[stat].mean():
            team1Points += 1
        else:
            team2Points += 1

    # Get the stats that are negatively correlated with wins for both teams and store them properly.
    # Get all numbers in the correlation with wins column that are negative
    statsTeam1NegativelyCorrelatedWins = topStatsTeam1['Statistic'][3:6]
    statsTeam2NegativelyCorrelatedWins = topStatsTeam2['Statistic'][3:6]

    # Add a point to the other team if they do better in a stat that is negatively correlated with wins
    for stat in statsTeam1NegativelyCorrelatedWins:
        if averagesTeam1[stat].mean() > averagesTeam2[stat].mean():
            team2Points += 1
        else:
            team1Points += 1

    # Now that we have the number of points for each team, we can predict the winner
    if team1Points > team2Points:
        return team1, team1Points, team2Points
    else:
        return team2, team2Points, team1Points

# Test the function
# Print the predicted winner in a nice format, utilizing the returned winner, winner_points, and loser_points
winner, winner_points, loser_points = predict_winner('Kansas St.', 'Arkansas')
#print(winner + ' is predicted to win the game with ' + str(winner_points) + ' points to ' + str(loser_points) + ' points.')

# Create a function that will use all the statistics acquired in the getAverages function to predict the winner of a game
def predict_winner_all_stats(team1, team2):
    # Get all the statistics for both teams. If the statistic is a good thing, add a point to the team with the higher value
    # If the statistic is a bad thing, add a point to the team with the lower value
    averagesTeam1 = getAverages(team1)
    averagesTeam2 = getAverages(team2)

    # Identify the statistics that are positively correlated with wins to determine which are good and which are bad
    goodStats = []
    badStats = []

    # Identify the correlation between wins and all the other statistics (except for the team name and the win and loss columns)
    correlations = {}
    for key in averagesTeam1:
        if key != 'team' and key != 'win' and key != 'loss':
            correlations[key] = np.corrcoef(averagesTeam1['win'], averagesTeam1[key])[0][1]

    # Sort the correlations
    sorted_correlations = sorted(correlations.items(), key=lambda x: x[1], reverse=True)

    # If a correlation is positive, add it to the good stats list. If it is negative, add it to the bad stats list
    for stat in sorted_correlations:
        if stat[1] > 0:
            goodStats.append(stat[0])
        else:
            badStats.append(stat[0])

    # Now that we have the good and bad stats, we can predict the winner of the game
    team1Points = 0
    team2Points = 0

    # Add a point to the team that has a higher value in a good stat
    for stat in goodStats:
        if averagesTeam1[stat].mean() > averagesTeam2[stat].mean():
            team1Points += 1
        else:
            team2Points += 1

    # Add a point to the team that has a lower value in a bad stat
    for stat in badStats:
        if averagesTeam1[stat].mean() < averagesTeam2[stat].mean():
            team1Points += 1
        else:
            team2Points += 1

    # Now that we have the number of points for each team, we can predict the winner
    if team1Points > team2Points:
        return team1, team1Points, team2Points
    else:
        return team2, team2Points, team1Points

# Test the function
# Print the predicted winner in a nice format, utilizing the returned winner, winner_points, and loser_points
#winner, winner_points, loser_points = predict_winner_all_stats('Indiana', 'UCLA')
#print(winner + ' is predicted to win the game with ' + str(winner_points) + ' points to ' + str(loser_points) + ' points.')

# Great! Now we can predict the winner of a game between two teams based on the statistics of the two teams

# Create a function to determine the total number of expected points in a game between two teams
# Make sure to take into account points per game, points per game allowed, etc
def predict_points(team1, team2):
    # Get the averages for both teams
    averagesTeam1 = getAverages(team1)
    averagesTeam2 = getAverages(team2)

    # Get the points per game for both teams
    pointsPerGameTeam1 = averagesTeam1['points_per_game'].mean()
    pointsPerGameTeam2 = averagesTeam2['points_per_game'].mean()

    # Get the points per game allowed for both teams
    pointsPerGameAllowedTeam1 = averagesTeam1['avg_points_per_game_allowed'].mean()
    pointsPerGameAllowedTeam2 = averagesTeam2['avg_points_per_game_allowed'].mean()

    # Get the expected points for both teams
    expectedPointsTeam1 = (pointsPerGameTeam1 + pointsPerGameAllowedTeam2) / 2
    expectedPointsTeam2 = (pointsPerGameTeam2 + pointsPerGameAllowedTeam1) / 2

    return round(expectedPointsTeam1 + expectedPointsTeam2, 3)

# Test the function
# Print the expected number of points in a game between two teams
# total = (predict_points('Vanderbilt', 'Georgia St.'))
# print("Total: ", total)

# Great! Now we can predict the total number of points in a game between two teams

# Create a function to predict how much the predicted winner will win by
def spread(team1, team2):
    # Get the averages for both teams
    averagesTeam1 = getAverages(team1)
    averagesTeam2 = getAverages(team2)

    # Calculate the predicted point differential (spread)
    # We will use points_per_game (offense) and avg_points_per_game_allowed (defense) as primary factors
    team1_offense = averagesTeam1['points_per_game'].mean()
    team1_defense = averagesTeam1['avg_points_per_game_allowed'].mean()

    team2_offense = averagesTeam2['points_per_game'].mean()
    team2_defense = averagesTeam2['avg_points_per_game_allowed'].mean()

    # Calculate the offensive and defensive matchup: (offensive strength - opposing defensive strength)
    team1_predicted_points = team1_offense - team2_defense
    team2_predicted_points = team2_offense - team1_defense

    # Calculate the spread as the difference in predicted points
    point_spread = team1_predicted_points - team2_predicted_points

    return round(point_spread, 2)


# Test the function
# Print the spread in a game between two teams
team1 = 'Oklahoma St.'
team2 = 'Tulsa'
spread = spread(team1, team2)
# Print out the predicted spread (indicating which team is favored by how many points)
if spread > 0:
    print(team1 + ' is favored to win by ' + str(spread) + ' points.')
else:
    print(team2 + ' is favored to win by ' + str(abs(spread)) + ' points.')