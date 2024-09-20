# Begin by importing the necessary libraries and modules.
import traceback

import pandas as pd
import numpy as np
from tabulate import tabulate
import main

# Load the main data (Stored in the CFBdata folder)
data = pd.read_csv("CFBdata/cfb.csv")

# Keep in mind that all column names are lowercase and snakecase

years = ["2017", "2018", "2019", "2020", "2021", "2022", "2023"]


def get_team_names():
    """
    Get the names of all the teams in the dataset.

    :return: A list containing the names of all the teams in the dataset.
    """
    # Get each team name from the cfb.csv file, ignoring the team years (remove last 5 characters)
    # Do not include duplicates
    # Store them in a list
    cfb_team_names = []
    for index, row in data.iterrows():
        cfb_team_names.append(row["team"][:-5])
    # Remove duplicates
    cfb_team_names = list(set(cfb_team_names))

    return cfb_team_names


def getAverages(team):
    """
    Get the averages of several categorical statistics for a team.

    :param team: The name of the team to get the averages for.
    :return: A dictionary containing the averages of several categorical statistics for the team.
    """
    instances = []
    for index, row in data.iterrows():
        # Check if the team name is the same as the team we are looking for
        # To do so, ignore the last 4 characters of the team name (the year)
        if row["team"][:-5] == team:
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
        wins.append(instance["win"])
        losses.append(instance["loss"])
        off_yards_per_game.append(instance["off_yards_per_game"])
        yards_per_game_allowed.append(instance["yards_per_game_allowed"])
        rushing_yards_per_game.append(instance["rushing_yards_per_game"])
        rush_yards_per_game_allowed.append(instance["rush_yards_per_game_allowed"])
        pass_yards_per_game.append(instance["pass_yards_per_game"])
        pass_yards_per_game_allowed.append(instance["pass_yards_per_game_allowed"])
        avg_points_per_game_allowed.append(instance["avg_points_per_game_allowed"])
        points_per_game.append(instance["points_per_game"])
        fourth_percent.append(instance["4th_percent"])
        opponent_fourth_percent.append(instance["opponent_4th_percent"])
        third_percent.append(instance["3rd_percent"])
        opponent_third_percent.append(instance["opponent_3rd_percent"])
        avg_turnover_margin_per_game.append(instance["avg_turnover_margin_per_game"])

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
    avg_turnover_margin_per_game = np.array(
        avg_turnover_margin_per_game, dtype=np.double
    )

    averageStats["team"] = team
    # Instead of calculating the averages, simply store the lists of each statistic in the dictionary as the value for the key
    # But first, convert all the values in all the lists to valid doubles
    averageStats["win"] = wins
    averageStats["loss"] = losses
    averageStats["off_yards_per_game"] = off_yards_per_game
    averageStats["yards_per_game_allowed"] = yards_per_game_allowed
    averageStats["rushing_yards_per_game"] = rushing_yards_per_game
    averageStats["rush_yards_per_game_allowed"] = rush_yards_per_game_allowed
    averageStats["pass_yards_per_game"] = pass_yards_per_game
    averageStats["pass_yards_per_game_allowed"] = pass_yards_per_game_allowed
    averageStats["avg_points_per_game_allowed"] = avg_points_per_game_allowed
    averageStats["points_per_game"] = points_per_game
    averageStats["fourth_percent"] = fourth_percent
    averageStats["opponent_fourth_percent"] = opponent_fourth_percent
    averageStats["third_percent"] = third_percent
    averageStats["opponent_third_percent"] = opponent_third_percent
    averageStats["avg_turnover_margin_per_game"] = avg_turnover_margin_per_game

    return averageStats


def getTopStats(averages):
    """
    Get the top 3 statistics that are positively correlated with wins and the top 3 statistics that are negatively correlated with wins.
    Also get the top 3 statistics that are positively correlated with losses and the top 3 statistics that are negatively correlated with losses.

    :param averages: The averages of the statistics for a team.
    :return: A table containing the top 3 statistics that are positively correlated with wins, the top 3 statistics
    that are negatively correlated with wins,
    """
    # Get the correlation between wins and all the other statistics
    correlations = {}
    for key in averages:
        if key not in ("team", "win", "loss"):
            correlations[key] = np.corrcoef(averages["win"], averages[key])[0][1]

    # Sort the correlations
    sorted_correlations = sorted(correlations.items(), key=lambda x: x[1], reverse=True)

    top_three_positively_correlated_wins = []
    for i in range(3):
        # Store these top 3 statistics for later access (round them to 5 decimal places)
        top_three_positively_correlated_wins.append(
            (sorted_correlations[i][0], round(sorted_correlations[i][1], 5))
        )

    top_three_negatively_correlated_wins = []
    for i in range(3):
        # Store these top 3 statistics for later access (round them to 5 decimal places)
        top_three_negatively_correlated_wins.append(
            (sorted_correlations[-i - 1][0], round(sorted_correlations[-i - 1][1], 5))
        )

    # Also find the top 3 statistics that are positively correlated with losses and the top 3 statistics that are negatively correlated with losses
    correlations = {}
    for key in averages:
        if key not in ("team", "win", "loss"):
            correlations[key] = np.corrcoef(averages["loss"], averages[key])[0][1]

    # Sort the correlations
    sorted_correlations = sorted(correlations.items(), key=lambda x: x[1], reverse=True)

    # Print out the top 3 positively correlated statistics
    top_three_positively_correlated_losses = []
    for i in range(3):
        # Store these top 3 statistics for later access (round them to 5 decimal places)
        top_three_positively_correlated_losses.append(
            (sorted_correlations[i][0], round(sorted_correlations[i][1], 5))
        )

    # Print out the top 3 negatively correlated statistics
    top_three_negatively_correlated_losses = []
    for i in range(3):
        # Store these top 3 statistics for later access (round them to 5 decimal places)
        top_three_negatively_correlated_losses.append(
            (sorted_correlations[-i - 1][0], round(sorted_correlations[-i - 1][1], 5))
        )

    # Store our results in a table
    results = pd.DataFrame(
        columns=["Statistic", "Correlation with Wins", "Correlation with Losses"]
    )

    # Fill the dataframe with the results
    for i in range(3):
        # We cannot use append because dataframes do not have that method
        results.loc[i] = [
            top_three_positively_correlated_wins[i][0],
            top_three_positively_correlated_wins[i][1],
            top_three_positively_correlated_losses[i][1],
        ]
    for i in range(3):
        results.loc[i + 3] = [
            top_three_negatively_correlated_wins[i][0],
            top_three_negatively_correlated_wins[i][1],
            top_three_negatively_correlated_losses[i][1],
        ]

    return results


def print_table(df):
    """
    Print a table in a nice format.

    :param df: The dataframe to print.
    :return: None
    """
    print(tabulate(df, headers="keys", tablefmt="pretty"))


def predict_winner(team1, team2):
    """
    Predict the winner of a game between two teams based on the three statistics most closely correlated with wins.

    :param team1: The first team.
    :param team2: The second team.
    :return: The predicted winner of the game, the number of points the predicted winner is expected to score, and the number of points the predicted loser is expected to score.
    """
    # Keep in mind the stats that have the highest correlation with wins
    # We will use the stats that have the highest correlation with wins
    # Get the averages for both teams (using the getAverages function)
    averagesTeam1 = getAverages(team1)
    averagesTeam2 = getAverages(team2)

    # Get the top 3 stats that are positively correlated with wins for both teams
    topStatsTeam1 = getTopStats(averagesTeam1)
    topStatsTeam2 = getTopStats(averagesTeam2)

    # Get the stats that are positively correlated with wins for both teams and store them properly.
    statsTeam1PositivelyCorrelatedWins = topStatsTeam1["Statistic"][:3]
    statsTeam2PositivelyCorrelatedWins = topStatsTeam2["Statistic"][:3]

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
    statsTeam1NegativelyCorrelatedWins = topStatsTeam1["Statistic"][3:6]
    statsTeam2NegativelyCorrelatedWins = topStatsTeam2["Statistic"][3:6]

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


def calculate_rolling_averages(averages):
    rolling_averages = {}

    for stat, data in averages.items():
        if stat not in ("team", "win", "loss"):
            rolling_average = 0
            for value in data:
                rolling_average = (rolling_average + value) / 2
            rolling_averages[stat] = rolling_average

    return rolling_averages


def predict_winner_all_stats(team1, team2, homeTeam=None, awayTeam=None):
    """
    Predict the winner of a game between two teams based on all the statistics of the two teams.

    :param team1: The first team.
    :param team2: The second team.
    :return: The predicted winner of the game, the number of points the predicted winner is expected to score, and the number of points the predicted loser is expected to score.
    """
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
        if key not in ("team", "win", "loss"):
            correlations[key] = np.corrcoef(averagesTeam1["win"], averagesTeam1[key])[
                0
            ][1]

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

    # # Make a list called rollingAverages
    # rollingAveragesTeam1 = {}
    # rollingAveragesTeam2 = {}
    #
    # # For each stat in averagesTeam1, calculate the rolling average
    # # A rolling average is not just the average of the stat, but the average of the first two instances, then the average of (the average of the first two isntances, and the third instance), and so on
    # count = 0
    # try:
    #     for stat in averagesTeam1:
    #         if stat not in ("team", "win", "loss"):
    #             # Calculate the rolling average for team 1
    #             rollingAverageTeam1 = 0
    #             for i in range(len(averagesTeam1[stat])):
    #                 rollingAverageTeam1 += averagesTeam1[stat][i]
    #                 if count != 0:
    #                     rollingAverageTeam1 /= 2
    #                 count += 1
    #             # Append the rolling average to the dictionary as the value for the key (stat)
    #             rollingAveragesTeam1[stat] = rollingAverageTeam1
    # except:
    #     pass
    #
    # count = 0
    # try:
    #     for stat in averagesTeam2:
    #         if stat not in ("team", "win", "loss"):
    #             # Calculate the rolling average for team 2
    #             rollingAverageTeam2 = 0
    #             for i in range(len(averagesTeam2[stat])):
    #                 rollingAverageTeam2 += averagesTeam2[stat][i]
    #                 if count != 0:
    #                     rollingAverageTeam2 /= 2
    #                 count += 1
    #             # Append the rolling average to the dictionary as the value for the key (stat)
    #             rollingAveragesTeam2[stat] = rollingAverageTeam2
    # except:
    #     pass

    rollingAveragesTeam1 = calculate_rolling_averages(averagesTeam1)
    rollingAveragesTeam2 = calculate_rolling_averages(averagesTeam2)

    # Add a point to the team that has a higher value in a good stat (using the rolling averages)
    # Use the rolling averages dictionary (the key is the stat and the value is the rolling average)
    # Compare the key to each stat in the goodStats list to determine if it is a good stat
    for stat in range(len(goodStats)):
        if (
            rollingAveragesTeam1[goodStats[stat]]
            > rollingAveragesTeam2[goodStats[stat]]
        ):
            team1Points += 1
        else:
            team2Points += 1

    # Add a point to the team that has a lower value in a bad stat (using the rolling averages)
    # Use the rolling averages dictionary (the key is the stat and the value is the rolling average)
    # Compare the key to each stat in the badStats list to determine if it is a bad stat
    # Loop through all the badStats (this is okay since we are looking for keys) - no starting point needed
    for stat in range(len(badStats)):
        if rollingAveragesTeam1[badStats[stat]] < rollingAveragesTeam2[badStats[stat]]:
            team1Points += 1
        else:
            team2Points += 1

    # # Add a point to the team that has a higher value in a good stat
    # for stat in goodStats:
    #     if averagesTeam1[stat].mean() > averagesTeam2[stat].mean():
    #         team1Points += 1
    #     else:
    #         team2Points += 1
    #
    # # Add a point to the team that has a lower value in a bad stat
    # for stat in badStats:
    #     if averagesTeam1[stat].mean() < averagesTeam2[stat].mean():
    #         team1Points += 1
    #     else:
    #         team2Points += 1

    # Get the conference multipliers
    try:
        conference_multipliers = main.CONFERENCE_MULTIPLIERS

        # Adjust the points based on the conference multipliers
        # Get the conference of each team from the conference column in the data
        team1conference = data.loc[data["team"].str.contains(team1)].iloc[0][
            "conference"
        ]
        team2conference = data.loc[data["team"].str.contains(team2)].iloc[0][
            "conference"
        ]
        team1Points *= conference_multipliers[team1conference]
        team2Points *= conference_multipliers[team2conference]

        # If homeTeam and awayTeam are provided, adjust the points based on the home field advantage
        if homeTeam and awayTeam:
            home_field_advantage = main.Home_Field_Advantage
            away_field_disadvantage = main.Away_Field_Disadvantage
            if team1 == homeTeam:
                team1Points *= home_field_advantage
                team2Points *= away_field_disadvantage
            elif team2 == homeTeam:
                team2Points *= home_field_advantage
                team1Points *= away_field_disadvantage

    except:
        pass

    # Now that we have the number of points for each team, we can predict the winner
    if team1Points > team2Points:
        return team1, team1Points, team2Points
    else:
        return team2, team2Points, team1Points


def predict_points(team1, team2):
    """
    Predict the total number of points in a game between two teams.

    :param team1: The first team.
    :param team2: The second team.
    :return: The total number of points in a game between two teams.
    """
    # Get the averages for both teams
    averagesTeam1 = getAverages(team1)
    averagesTeam2 = getAverages(team2)

    # Get the points per game for both teams
    pointsPerGameTeam1 = averagesTeam1["points_per_game"].mean()
    pointsPerGameTeam2 = averagesTeam2["points_per_game"].mean()

    # # Get the points per game for both teams using rolling averages
    # pointsPerGameTeam1 = calculate_rolling_averages(averagesTeam1)["points_per_game"]
    # pointsPerGameTeam2 = calculate_rolling_averages(averagesTeam2)["points_per_game"]

    # Get the points per game allowed for both teams
    pointsPerGameAllowedTeam1 = averagesTeam1["avg_points_per_game_allowed"].mean()
    pointsPerGameAllowedTeam2 = averagesTeam2["avg_points_per_game_allowed"].mean()

    # # Get the points per game allowed for both teams using rolling averages
    # pointsPerGameAllowedTeam1 = calculate_rolling_averages(averagesTeam1)["avg_points_per_game_allowed"]
    # pointsPerGameAllowedTeam2 = calculate_rolling_averages(averagesTeam2)["avg_points_per_game_allowed"]

    # Get the expected points for both teams
    expectedPointsTeam1 = (pointsPerGameTeam1 + pointsPerGameAllowedTeam2) / 2
    expectedPointsTeam2 = (pointsPerGameTeam2 + pointsPerGameAllowedTeam1) / 2

    # # Get the expected points for both teams using just the points per game
    # expectedPointsTeam1 = pointsPerGameTeam1
    # expectedPointsTeam2 = pointsPerGameTeam2

    # Get the conference multipliers
    try:
        conference_multipliers = main.CONFERENCE_MULTIPLIERS

        # Adjust the points based on the conference multipliers
        # Get the conference of each team from the conference column in the data
        team1conference = data.loc[data["team"].str.contains(team1)].iloc[0][
            "conference"
        ]
        team2conference = data.loc[data["team"].str.contains(team2)].iloc[0][
            "conference"
        ]
        expectedPointsTeam1 *= conference_multipliers[team1conference]
        expectedPointsTeam2 *= conference_multipliers[team2conference]
    except:
        pass

    return round(expectedPointsTeam1 + expectedPointsTeam2, 3)


def spread(team1, team2):
    """
    Predict the point spread in a game between two teams.

    :param team1: The first team.
    :param team2: The second team.
    :return: The predicted point spread in a game between two teams.
    """
    # Get the averages for both teams
    averagesTeam1 = getAverages(team1)
    averagesTeam2 = getAverages(team2)

    # Calculate the predicted point differential (spread)
    # We will use points_per_game (offense) and avg_points_per_game_allowed (defense) as primary factors
    team1_offense = averagesTeam1["points_per_game"].mean()
    team1_defense = averagesTeam1["avg_points_per_game_allowed"].mean()

    team2_offense = averagesTeam2["points_per_game"].mean()
    team2_defense = averagesTeam2["avg_points_per_game_allowed"].mean()

    # Calculate the offensive and defensive matchup: (offensive strength - opposing defensive strength)
    team1_predicted_points = team1_offense - team2_defense
    team2_predicted_points = team2_offense - team1_defense

    # Calculate the spread as the difference in predicted points
    point_spread = team1_predicted_points - team2_predicted_points

    return round(point_spread, 2)
