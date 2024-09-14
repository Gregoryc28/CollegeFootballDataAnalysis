import traceback

from data import *
from dotenv import load_dotenv
import os
import requests
from datetime import datetime
from itertools import chain
import time

# Load environment variables
load_dotenv()

# Handle warnings
import warnings

warnings.simplefilter("error", RuntimeWarning)


def access_cfb_api():
    api_key = os.getenv("API_KEY")

    # Please note that API keys should be supplied with "Bearer " prepended (e.g. "Bearer your_key")
    headers = {"Authorization": "Bearer " + api_key}

    # Base URL for the API
    base_url = "https://api.collegefootballdata.com/"

    # Return access to the API
    return headers, base_url


def clean_team_names():
    """
    This function cleans the team names from the College Football Data API.

    :return: team_names (list) - a list of all the team names in the FBS; team_names_dict (dict) - a dictionary that links all of the team names to their filtered names
    """
    headers, base_url = access_cfb_api()

    # Get the list of teams (in the FBS)
    endpoint = "teams/fbs"
    url = base_url + endpoint
    response = requests.get(url, headers=headers)
    data = response.json()

    # Store the team names in a list
    team_names = []
    for team in data:
        team_names.append(team["school"])

    # If a team name contains "State", convert "State" to "St."
    for i in range(len(team_names)):
        if "State" in team_names[i]:
            team_names[i] = team_names[i].replace("State", "St.")

    # Make the following changes to the teams in the team_names list:
    # "App St." -> "Appalachian St."
    # "Army" -> "Army West Point"
    # "Central Michigan" -> "Central Mich."
    # "Eastern Michigan" -> "Eastern Mich.
    # Remove Florida Atlantic
    # Remove Florida International
    # Remove Georgia Southern
    # "Hawai'i" -> "Hawaii"
    # Remove Kennesaw St.
    # "Middle Tennessee" -> "Middle Tenn."
    # "Northern Illinois" -> "Northern Ill."
    # "San José St." -> "San Jose St."
    # "Southern Miss" -> "Southern Miss."
    # "South Florida" -> "South Fla."
    # "UL Monroe" -> "La.-Monroe"
    # "USC" -> "Southern California"
    # "Western Kentucky" -> "Western Ky."
    # "Western Michigan" -> "Western Mich."

    i = 0
    while i < len(team_names):
        if team_names[i] == "App St.":
            team_names[i] = "Appalachian St."
        elif team_names[i] == "Army":
            team_names[i] = "Army West Point"
        elif team_names[i] == "Central Michigan":
            team_names[i] = "Central Mich."
        elif team_names[i] == "Eastern Michigan":
            team_names[i] = "Eastern Mich."
        elif team_names[i] == "Florida Atlantic":
            team_names[i] = "Fla. Atlantic"
        elif team_names[i] == "Florida International":
            team_names[i] = "FIU"
        elif team_names[i] == "Georgia Southern":
            team_names[i] = "Ga. Southern"
        elif team_names[i] == "Hawai'i":
            team_names[i] = "Hawaii"
        elif team_names[i] == "Kennesaw St.":
            team_names.pop(i)
            i -= 1
        elif team_names[i] == "Middle Tennessee":
            team_names[i] = "Middle Tenn."
        elif team_names[i] == "Northern Illinois":
            team_names[i] = "Northern Ill."
        elif team_names[i] == "San José St.":
            team_names[i] = "San Jose St."
        elif team_names[i] == "Southern Miss":
            team_names[i] = "Southern Miss."
        elif team_names[i] == "South Florida":
            team_names[i] = "South Fla."
        elif team_names[i] == "UL Monroe":
            team_names[i] = "La.-Monroe"
        elif team_names[i] == "USC":
            team_names[i] = "Southern California"
        elif team_names[i] == "Western Kentucky":
            team_names[i] = "Western Ky."
        elif team_names[i] == "Western Michigan":
            team_names[i] = "Western Mich."
        elif team_names[i] == "Miami (OH)":
            team_names[i] = "Miami OH"

        i += 1

    # Create a dictionary that links all the team names to their filtered names
    team_names_dict = {}
    for team in data:
        team_names_dict[team["school"]] = team["school"]
    team_names_dict["App St."] = "Appalachian St."
    team_names_dict["Army"] = "Army West Point"
    team_names_dict["Central Michigan"] = "Central Mich."
    team_names_dict["Eastern Michigan"] = "Eastern Mich."
    team_names_dict["Florida Atlantic"] = "Fla. Atlantic"
    team_names_dict["Florida International"] = "FIU"
    team_names_dict["Georgia Southern"] = "Ga. Southern"
    team_names_dict["Hawai'i"] = "Hawaii"
    team_names_dict.pop("Kennesaw State")
    team_names_dict["Middle Tennessee"] = "Middle Tenn."
    team_names_dict["Northern Illinois"] = "Northern Ill."
    team_names_dict["San José St."] = "San Jose St."
    team_names_dict["Southern Miss"] = "Southern Miss."
    team_names_dict["South Florida"] = "South Fla."
    team_names_dict["UL Monroe"] = "La.-Monroe"
    team_names_dict["USC"] = "Southern California"
    team_names_dict["Western Kentucky"] = "Western Ky."
    team_names_dict["Western Michigan"] = "Western Mich."
    team_names_dict["Miami (OH)"] = "Miami OH"

    # Go through the dictionary and for any value (not key) that contains "State", convert "State" to "St."
    for key, value in team_names_dict.items():
        if "State" in value:
            team_names_dict[key] = value.replace("State", "St.")

    # Return the list of team names
    return team_names, team_names_dict


def get_current_week_games():
    """
    This function gets the games for the current week.

    :return: games (list) - a list of all the games for the current week
    """
    headers, base_url = access_cfb_api()

    # Get the games for the current week in the FBS only
    endpoint = f"games?year=2024&week={current_week}&division=fbs"
    url = base_url + endpoint
    response = requests.get(url, headers=headers)
    data = response.json()

    team_names, team_names_dict = clean_team_names()

    # Convert the team names to the filtered names
    for i in range(len(data)):
        try:
            home_team = data[i]["home_team"]
            away_team = data[i]["away_team"]
            data[i]["home_team"] = team_names_dict[home_team]
            data[i]["away_team"] = team_names_dict[away_team]
        except:
            pass

    # If a team is playing a team that is not in the FBS, remove that game
    i = 0
    while i < len(data):
        if (
            data[i]["home_team"] not in team_names
            or data[i]["away_team"] not in team_names
        ):
            data.pop(i)
            i -= 1
        i += 1

    # Store the games in a list
    games = []
    for game in data:
        games.append(game)

    # Format the games in this format: (home_team, away_team)
    for i in range(len(games)):
        home_team = games[i]["home_team"]
        away_team = games[i]["away_team"]
        games[i] = (home_team, away_team)

    # Return the list of games
    return games


def get_current_week():
    """
    This function gets the current week of the college football season.

    :return: current_week (int) - the current week of the college football season
    """
    current_week = 1
    date = datetime.now()
    # Get the current week of the college football season
    endpoint = "calendar?year=2024"
    headers, base_url = access_cfb_api()
    url = base_url + endpoint
    response = requests.get(url, headers=headers)
    data = response.json()
    for week in data:
        first_game_start = week["firstGameStart"]
        last_game_start = week["lastGameStart"]
        first_game_start = first_game_start.split("T")[0]
        last_game_start = last_game_start.split("T")[0]
        first_game_start = datetime.strptime(first_game_start, "%Y-%m-%d")
        last_game_start = datetime.strptime(last_game_start, "%Y-%m-%d")
        if date >= first_game_start and date <= last_game_start:
            current_week = week["week"]
            break

    return current_week


def predict_this_weeks_games():
    """
    This function predicts the games for the current week.

    :return: winners (list) - a list of the predicted winners for the current week
    """
    current_week_games = get_current_week_games()

    matchups = []
    for game in current_week_games:
        matchup = f"{game[1]} at {game[0]}"
        matchups.append(matchup)

    winners = []
    error_games = []
    team_names, team_names_dict = clean_team_names()
    for game in current_week_games:
        # If there is an error, remove the game
        try:
            home_team = game[0]
            away_team = game[1]
            home_team = team_names_dict[home_team]
            away_team = team_names_dict[away_team]
            winner = predict_winner_all_stats(home_team, away_team)
            winners.append(winner)
        except:
            error_games.append(game)

    # If there are error games, remove them from the matchups
    for game in error_games:
        matchup = f"{game[1]} at {game[0]}"
        matchups.remove(matchup)

    return winners, matchups


def most_guaranteed_to_win(winners, matchups):
    """
    This function predicts the 12 games that are the most guaranteed to win.

    :return: None
    """
    # Each item in winners is stored as such: (winning_team, winning_team_points, losing_team_points)
    # Find the 12 games that are the most guaranteed to win (biggest difference in points)
    biggest_differences = []
    for i in range(len(winners)):
        difference = winners[i][1] - winners[i][2]
        biggest_differences.append((difference, matchups[i]))

    biggest_differences.sort(reverse=True)
    for i in range(12):
        print(
            f"\n{biggest_differences[i][1]}: \033[92m{winners[matchups.index(biggest_differences[i][1])][0]}\033[0m"
        )
        print(f"Points Difference: {biggest_differences[i][0]}")


def predict_this_weeks_SEC_games():
    """
    This function predicts the games for the current week in the SEC.

    :return: winners (list) - a list of the predicted winners for the current week in the SEC
    """
    current_week_games = get_current_week_games()

    matchups = []
    for game in current_week_games:
        matchup = f"{game[1]} at {game[0]}"
        matchups.append(matchup)

    winners = []
    total_scores = []
    error_games = []
    team_names, team_names_dict = clean_team_names()
    for game in current_week_games:
        # If there is an error, remove the game
        try:
            home_team = game[0]
            away_team = game[1]
            if home_team in SEC_TEAMS or away_team in SEC_TEAMS:
                winner = predict_winner_all_stats(home_team, away_team)
                winners.append(winner)
                total_score = predict_points(home_team, away_team)
                total_scores.append(total_score)
            else:
                matchups.remove(f"{away_team} at {home_team}")
        except:
            error_games.append(game)

    # If there are error games, remove them from the matchups
    for game in error_games:
        try:
            matchup = f"{game[1]} at {game[0]}"
            matchups.remove(matchup)
        except:
            pass

    return winners, matchups, total_scores


def get_current_week_winners(winners, matchups):
    """
    This function gets the winners for the current week.

    :return: None
    """
    # Print the predicted winners for the current week
    for i in range(len(matchups)):
        print(f"{matchups[i]}: {winners[i]}")


def get_current_week_most_guaranteed(winners, matchups):
    """
    This function gets the 12 games that are the most guaranteed to win.

    :return: None
    """
    # Print the 12 games that are the most guaranteed to win (biggest difference in points)
    print("\n12 Games Most Guaranteed to Win:\n")
    most_guaranteed_to_win(winners, matchups)


def get_current_week_SEC_predictions(winners, matchups):
    """
    This function gets the predicted winners and totals for the current week in the SEC.

    :return: None
    """
    # Print the predicted winners and totals for the current week in the SEC
    winners, matchups, total_scores = predict_this_weeks_SEC_games()

    return winners, matchups, total_scores


def get_current_SEC_overUnder_lines():
    """
    This function gets the over/under lines for the current week in the SEC

    :return: home_team (str) - the home team in the game; away_team (str) - the away team in the game; over_under (float) - the over/under line for the game
    """
    headers, base_url = access_cfb_api()
    endpoint = f"lines?year=2024&week={current_week}&conference=SEC"
    url = base_url + endpoint
    response = requests.get(url, headers=headers)
    data = response.json()

    for game in data:
        home_team = game["homeTeam"]
        away_team = game["awayTeam"]
        over_under = game["lines"][0]["overUnder"]

    return (home_team, away_team, over_under)


def get_anyWeek_SEC_overUnder_lines(week):
    """
    This function gets the over/under lines for any week in the SEC

    :return: home_team (str) - the home team in the game; away_team (str) - the away team in the game; over_under (float) - the over/under line for the game
    """
    headers, base_url = access_cfb_api()
    endpoint = f"lines?year=2024&week={week}&conference=SEC"
    url = base_url + endpoint
    response = requests.get(url, headers=headers)
    data = response.json()

    overUnderLines = []

    for game in data:
        home_team = game["homeTeam"]
        away_team = game["awayTeam"]
        over_under = game["lines"][0]["overUnder"]
        overUnderLines.append((home_team, away_team, over_under))

    return overUnderLines


def get_actual_SEC_totalScores(week):
    """
    This function gets the actual total scores for the SEC games in a given week

    :return: home_team (str) - the home team in the game; away_team (str) - the away team in the game; total_score (int) - the total score for the game
    """
    headers, base_url = access_cfb_api()
    endpoint = f"games?year=2024&week={week}&conference=SEC"
    url = base_url + endpoint
    response = requests.get(url, headers=headers)
    data = response.json()

    actualTotalScores = []

    team_names, team_names_dict = clean_team_names()

    for game in data:
        home_team = game["home_team"]
        away_team = game["away_team"]

        # Try to clean the team names (if it fails, remove the game)
        try:
            home_team = team_names_dict[home_team]
            away_team = team_names_dict[away_team]
            total_score = game["home_points"] + game["away_points"]
        except:
            continue

        actualTotalScores.append((home_team, away_team, total_score))

    return actualTotalScores


def predict_anyWeek_SEC_totalScores(week):
    """
    This function predicts the total scores for the SEC games in a given week

    :return: home_team (str) - the home team in the game; away_team (str) - the away team in the game; total_score (int) - the total score for the game
    """
    headers, base_url = access_cfb_api()
    endpoint = f"games?year=2024&week={week}&conference=SEC"
    url = base_url + endpoint
    response = requests.get(url, headers=headers)
    data = response.json()

    predictedTotalScores = []

    team_names, team_names_dict = clean_team_names()

    for game in data:
        home_team = game["home_team"]
        away_team = game["away_team"]

        # Try to clean the team names (if it fails, remove the game)
        try:
            home_team = team_names_dict[home_team]
            away_team = team_names_dict[away_team]
            total_score = predict_points(home_team, away_team)
        except:
            continue

        predictedTotalScores.append((home_team, away_team, total_score))

    return predictedTotalScores


def check_prior_SEC_overUnder_accuracy(overUnderLines):
    """
    This function checks the accuracy of the over/under lines for the SEC games in prior weeks

    :param overUnderLines: the over/under lines for the SEC games in prior weeks
    :return: accuracy (float) - the accuracy of the over/under lines for the SEC games in prior weeks
    """
    # Get the actual total scores for each SEC game in every week prior to the current week
    actualTotalScores = []
    for week in range(1, current_week):
        actualTotalScores.append(get_actual_SEC_totalScores(week))

    # Get the predicted total scores for each SEC game in every week prior to the current week
    predictedTotalScores = []
    for week in range(1, current_week):
        predictedTotalScores.append(predict_anyWeek_SEC_totalScores(week))

    correct = 0
    wrong = 0

    # Currently both the lists have arrays in them for each week
    # We need to flatten them to compare them
    actualTotalScores = list(chain.from_iterable(actualTotalScores))
    predictedTotalScores = list(chain.from_iterable(predictedTotalScores))

    # Flatten the overUnderLines list
    overUnderLines = list(chain.from_iterable(overUnderLines))

    # Filter the team names in overUnderLines to their filtered names
    team_names, team_names_dict = clean_team_names()
    for i in range(len(overUnderLines)):
        try:
            home_team = overUnderLines[i][0]
            away_team = overUnderLines[i][1]
            overUnderLines[i] = (
                team_names_dict[home_team],
                team_names_dict[away_team],
                overUnderLines[i][2],
            )
        except:
            continue

    # Remove any games with teams in overUnderLines that are not in actualTotalScores or predictedTotalScores
    i = 0
    while i < len(overUnderLines):
        if overUnderLines[i][0] not in [
            team[0] for team in actualTotalScores
        ] or overUnderLines[i][1] not in [team[1] for team in actualTotalScores]:
            overUnderLines.pop(i)
            i -= 1
        i += 1

    # Sort the team names in OverUnderLines to match the order of the team names in actualTotalScores and predictedTotalScores
    overUnderLines = sorted(overUnderLines, key=lambda x: x[0])
    predictedTotalScores = sorted(predictedTotalScores, key=lambda x: x[0])
    actualTotalScores = sorted(actualTotalScores, key=lambda x: x[0])

    for i in range(len(actualTotalScores)):
        thisActualTotalScore = float(actualTotalScores[i][2])
        thisPredictedTotalScore = float(predictedTotalScores[i][2])
        thisOverUnderLine = float(overUnderLines[i][2])
        if (
            thisActualTotalScore > thisOverUnderLine
            and thisPredictedTotalScore > thisOverUnderLine
        ):
            correct += 1
        elif (
            thisActualTotalScore < thisOverUnderLine
            and thisPredictedTotalScore < thisOverUnderLine
        ):
            correct += 1
        else:
            wrong += 1

    accuracy = correct / (correct + wrong) * 100
    return accuracy


def get_anyWeek_SEC_winners(week):
    """
    This function gets the winners for the SEC games in a given week

    :return: winners (list) - a list of the predicted winners for the SEC games in a given week
    """
    headers, base_url = access_cfb_api()
    endpoint = f"games?year=2024&week={week}&conference=SEC"
    url = base_url + endpoint
    response = requests.get(url, headers=headers)
    data = response.json()

    winners = []
    error_games = []
    team_names, team_names_dict = clean_team_names()
    for game in data:
        # If there is an error, remove the game
        try:
            home_team = game["home_team"]
            away_team = game["away_team"]
            # convert team names to filtered names
            home_team = team_names_dict[home_team]
            away_team = team_names_dict[away_team]
            # Figure out which team had the higher score
            if game["home_points"] > game["away_points"]:
                winner = home_team
            else:
                winner = away_team
            winners.append(winner)
        except:
            error_games.append(game)

    return winners


def predict_anyWeek_SEC_winners(week):
    """
    This function predicts the winners for the SEC games in a given week

    :return: winners (list) - a list of the predicted winners for the SEC games in a given week
    """
    headers, base_url = access_cfb_api()
    endpoint = f"games?year=2024&week={week}&conference=SEC"
    url = base_url + endpoint
    response = requests.get(url, headers=headers)
    data = response.json()

    winners = []
    error_games = []
    team_names, team_names_dict = clean_team_names()
    for game in data:
        # If there is an error, remove the game
        try:
            home_team = game["home_team"]
            away_team = game["away_team"]
            # convert team names to filtered names
            home_team = team_names_dict[home_team]
            away_team = team_names_dict[away_team]
            # Predict the winner
            winner = predict_winner_all_stats(home_team, away_team)
            winners.append(winner)
        except:
            error_games.append(game)

    return winners


def check_prior_SEC_winner_accuracy():
    """
    This function checks the accuracy of the predicted winners for the SEC games in prior weeks

    :return: accuracy (float) - the accuracy of the predicted winners for the SEC games in prior weeks
    """
    # Get the actual winners for each SEC game in every week prior to the current week
    actualWinners = []
    for week in range(1, current_week):
        actualWinners.append(get_anyWeek_SEC_winners(week))

    # Get the predicted winners for each SEC game in every week prior to the current week
    predictedWinnersTuples = []
    for week in range(1, current_week):
        predictedWinnersTuples.append(predict_anyWeek_SEC_winners(week))

    # Seperate the winners from the tuples
    predictedWinners = []
    # Take the first item in each tuple in the predictedWinnersTuples list and get rid of the rest
    for week in predictedWinnersTuples:
        for game in week:
            predictedWinners.append(game[0])

    # Sort the actualWinners and predictedWinners lists to match the order of the team names
    # predictedWinners = sorted(predictedWinners, key=lambda x: x[0])

    correct = 0
    wrong = 0

    # Currently both the lists have arrays in them for each week
    # We need to flatten them to compare them
    actualWinners = list(chain.from_iterable(actualWinners))
    # actualWinners = sorted(actualWinners, key=lambda x: x[0])

    print(actualWinners)
    print(predictedWinners)

    for i in range(len(actualWinners)):
        if actualWinners[i] == predictedWinners[i]:
            correct += 1
        else:
            wrong += 1

    accuracy = correct / (correct + wrong) * 100
    return accuracy


def create_teamConference_dict():
    """
    This function creates a dictionary that links each team to their conference

    :return: teamConference_dict (dict) - a dictionary that links each team to their conference
    """
    headers, base_url = access_cfb_api()

    # Get the teams and their conferences
    endpoint = "teams/fbs"
    url = base_url + endpoint
    response = requests.get(url, headers=headers)
    data = response.json()

    # Get the filtered team names
    team_names, team_names_dict = clean_team_names()

    teamConference_dict = {}
    for team in data:
        # Convert the team names to the filtered names and link them to their conferences
        try:
            team_name = team["school"]
            team_name = team_names_dict[team_name]
            conference = team["conference"]
            teamConference_dict[team_name] = conference
        except:
            continue

    return teamConference_dict


def add_team_conference_to_cfbCSV():
    """
    This function adds the conference of each team to the CollegeFootballData CSV file

    :return: None
    """
    teamConference_dict = create_teamConference_dict()

    # Read the CollegeFootballData CSV file
    cfb_data = pd.read_csv("CFBdata/cfb.csv")

    # Add the conference of each team to the CollegeFootballData CSV file
    conferences = []
    for index, row in cfb_data.iterrows():
        try:
            team = row["team"]
            # Remove the year from the team name (The last 5 characters)
            team = team[:-5]
            conference = teamConference_dict[team]
            conferences.append(conference)
        except:
            conferences.append("")
            print(f"Error: {team}")
            continue

    cfb_data["conference"] = conferences

    # Save the CollegeFootballData CSV file
    cfb_data.to_csv("CFBdata/cfb.csv", index=False)


def manually_update_team_conference_to_cfbCSV(team, conference):
    """
    This function manually updates the conference of a team in the CollegeFootballData CSV file

    :param team: the team whose conference is being updated
    :param conference: the conference of the team
    :return: None
    """
    # Read the CollegeFootballData CSV file
    cfb_data = pd.read_csv("CFBdata/cfb.csv")

    # Update the conference of the team in the CollegeFootballData CSV file
    for index, row in cfb_data.iterrows():
        if row["team"][:-5] == team:
            cfb_data.at[index, "conference"] = conference

    # Save the CollegeFootballData CSV file
    cfb_data.to_csv("CFBdata/cfb.csv", index=False)


def remove_columns_from_cfbCSV(column):
    """
    This function removes a column from the CollegeFootballData CSV file

    :param column: the column to be removed
    :return: None
    """
    # Read the CollegeFootballData CSV file
    cfb_data = pd.read_csv("CFBdata/cfb.csv")

    # Remove the column from the CollegeFootballData CSV file
    cfb_data.drop(column, axis=1, inplace=True)

    # Save the CollegeFootballData CSV file
    cfb_data.to_csv("CFBdata/cfb.csv", index=False)


def main():
    global current_week
    current_week = get_current_week()

    global SEC_TEAMS
    SEC_TEAMS = [
        "Alabama",
        "Arkansas",
        "Auburn",
        "Florida",
        "Georgia",
        "Kentucky",
        "LSU",
        "Mississippi St.",
        "Missouri",
        "Ole Miss",
        "South Carolina",
        "Tennessee",
        "Texas A&M",
        "Vanderbilt",
        "Texas",
        "Oklahoma",
    ]

    winners, matchups = predict_this_weeks_games()

    # get_current_week_winners(winners, matchups)
    # get_current_week_most_guaranteed(winners, matchups)

    # print(get_current_week_SEC_predictions(winners, matchups))
    # overUnderLines = []
    # for week in range(1, current_week):
    #     overUnderLines.append(get_anyWeek_SEC_overUnder_lines(week))
    # print(check_prior_SEC_overUnder_accuracy(overUnderLines))

    # print(check_prior_SEC_winner_accuracy())

    # add_team_conference_to_cfbCSV()
    # remove_columns_from_cfbCSV("Conference")
    # manually_update_team_conference_to_cfbCSV("Appalachian St.", "Sun Belt")
    # manually_update_team_conference_to_cfbCSV("San Jose St.", "Mountain West")
    # manually_update_team_conference_to_cfbCSV("Coastal Caro.", "Sun Belt")
    # manually_update_team_conference_to_cfbCSV("NIU", "Mid-American")
    # manually_update_team_conference_to_cfbCSV("ULM", "Sun Belt")


if __name__ == "__main__":
    main()
