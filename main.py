from data import *
from dotenv import load_dotenv
import os
import requests
from datetime import datetime

# Load environment variables
load_dotenv()

def access_cfb_api():
    api_key = os.getenv('API_KEY')

    # Please note that API keys should be supplied with "Bearer " prepended (e.g. "Bearer your_key")
    headers = {
        'Authorization': 'Bearer ' + api_key
    }

    # Base URL for the API
    base_url = 'https://api.collegefootballdata.com/'

    # Return access to the API
    return headers, base_url

def clean_team_names():
    '''
    This function cleans the team names from the College Football Data API.

    :return: team_names (list) - a list of all the team names in the FBS; team_names_dict (dict) - a dictionary that links all of the team names to their filtered names
    '''
    headers, base_url = access_cfb_api()

    # Get the list of teams (in the FBS)
    endpoint = 'teams/fbs'
    url = base_url + endpoint
    response = requests.get(url, headers=headers)
    data = response.json()

    # Store the team names in a list
    team_names = []
    for team in data:
        team_names.append(team['school'])

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
    # "NC St." -> "NC State"
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
        elif team_names[i] == "NC St.":
            team_names[i] = "NC State"
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
        team_names_dict[team['school']] = team['school']
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
    team_names_dict["NC St."] = "NC State"
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
    '''
    This function gets the games for the current week.

    :return: games (list) - a list of all the games for the current week
    '''
    headers, base_url = access_cfb_api()

    # Get the games for the current week
    endpoint = 'games?year=2024&week=' + str(current_week)
    url = base_url + endpoint
    response = requests.get(url, headers=headers)
    data = response.json()

    # Store the games in a list
    games = []
    for game in data:
        games.append(game)

    # Format the games in this format: (home_team, away_team)
    for i in range(len(games)):
        home_team = games[i]['home_team']
        away_team = games[i]['away_team']
        games[i] = (home_team, away_team)

    # Return the list of games
    return games

def get_current_week():
    '''
    This function gets the current week of the college football season.

    :return: current_week (int) - the current week of the college football season
    '''
    current_week = 1
    date = datetime.now()
    # Get the current week of the college football season
    endpoint = ('calendar?year=2024')
    headers, base_url = access_cfb_api()
    url = base_url + endpoint
    response = requests.get(url, headers=headers)
    data = response.json()
    for week in data:
        first_game_start = week['firstGameStart']
        last_game_start = week['lastGameStart']
        first_game_start = first_game_start.split('T')[0]
        last_game_start = last_game_start.split('T')[0]
        first_game_start = datetime.strptime(first_game_start, '%Y-%m-%d')
        last_game_start = datetime.strptime(last_game_start, '%Y-%m-%d')
        if date >= first_game_start and date <= last_game_start:
            current_week = week['week']
            break

    return current_week


def main():
    global current_week
    current_week = get_current_week()

    print(get_current_week_games())

if __name__ == "__main__":
    main()