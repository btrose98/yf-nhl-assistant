# main.py

import os
from pathlib import Path
import json
from yfpy.query import YahooFantasySportsQuery

# Set directory location of private.json for authentication
project_dir = Path(__file__).parent.parent
auth_dir = project_dir / "auth"



def main():
#   fetch keys and user information

    with open(auth_dir / "private.json", 'r') as f:
        credentials = json.load(f)

    consumer_key = credentials["consumer_key"]
    consumer_secret = credentials["consumer_secret"]

    # Set the season year
    season = 2023

    # Set the game code to 'nhl' for NHL hockey
    game_code = "nhl"

    # Set your specific league ID for NHL
    league_id = "60441"

    # Set your specific team ID within the league
    team_id = "6"

    # Set the desired week
    chosen_week = 1  # Replace with the current week or the week you want to retrieve

    # Initialize the YahooFantasySportsQuery object with your credentials
    yahoo_query = YahooFantasySportsQuery(
        auth_dir,
        league_id,
        game_code,
        offline=False,
        all_output_as_json_str=False,
        consumer_key=consumer_key,
        consumer_secret=consumer_secret
    )

    # Fetch the team roster for the specified week
    team_roster = yahoo_query.get_team_roster_by_week(team_id, chosen_week)

    # Print out the player names
    for player in team_roster:
        print(player)
#     fetch current team

# fetch current free agents

# make comparisons

# display ordered list of players


if __name__ == "__main__":
    main()