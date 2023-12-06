import csv
import json
import os
from pathlib import Path

from yfpy.query import YahooFantasySportsQuery

project_dir = Path(__file__).parent.parent
auth_dir = project_dir / "auth"
artifacts_dir = project_dir / "artifacts"

def main():

    consumer_key, consumer_secret = get_credentials()

    season = 2023
    game_code = "nhl"
    league_id = "60441"
    team_id = "6"
    chosen_week = 9  # Replace with the current week or the week you want to retrieve

    yahoo_query = YahooFantasySportsQuery(
        auth_dir,
        league_id,
        game_code,
        offline=False,
        all_output_as_json_str=False,
        consumer_key=consumer_key,
        consumer_secret=consumer_secret
    )

    league_key = yahoo_query.get_league_key()


    get_my_current_team(yahoo_query, team_id, chosen_week)

    get_available_free_agents(yahoo_query, league_key)


def get_my_current_team(yahoo_query, team_id, chosen_week):
    team_roster = yahoo_query.get_team_roster_by_week(team_id, chosen_week)
    for player in team_roster:
        print(player)

    return team_roster

def get_available_free_agents(yahoo_query, league_key):
    free_agents = yahoo_query.query(
        f"https://fantasysports.yahooapis.com/fantasy/v2/league/{league_key}/players;status=FA;sort=AR",
        ["league", "players"]
    )
    unavailable_statuses = ["NA", "IR", "IR-LT", "O"]
    available_free_agents = [
        player for player in free_agents
        if getattr(player, "status", None) not in unavailable_statuses
           and "injury" not in getattr(player, "status_full", "").lower()
    ]

    # print(f"available free agents: {available_free_agents}")

    if not os.path.exists(artifacts_dir):
        os.makedirs(artifacts_dir)

    csv_file_path = os.path.join(artifacts_dir, 'available_free_agents.csv')
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Player Name", "Player Key", "Status", "Position", "Team"])

        for player in available_free_agents:
            writer.writerow([getattr(player, "name").full, getattr(player, "player_key"),
                             getattr(player, "status", "N/A"), getattr(player, "primary_position"),
                             getattr(player, "editorial_team_abbr")])

    print("Available free agents written to available_free_agents.csv")

    return available_free_agents

def get_credentials():
    with open(auth_dir / "private.json", 'r') as f:
        credentials = json.load(f)
    consumer_key = credentials["consumer_key"]
    consumer_secret = credentials["consumer_secret"]
    return consumer_key, consumer_secret

if __name__ == "__main__":
    main()