import requests
import json
import os
import pandas as pd

def request_data(url: str) -> json:
    response = requests.get(url)
    return response.json()

def format_data(data: json) -> json:
    home_win = data["competitions"][0]["competitors"][0]["winner"]
    away_win = data["competitions"][0]["competitors"][1]["winner"]
    if home_win:
        winner = data["competitions"][0]["competitors"][0]["team"]["displayName"]
    elif away_win:
        winner = data["competitions"][0]["competitors"][1]["team"]["displayName"]
    else:
        winner = "Draw"

    home_team_goals = data["competitions"][0]["competitors"][0]["score"]["value"]
    away_team_goals = data["competitions"][0]["competitors"][1]["score"]["value"]
    normal_duration = data["competitions"][0]["status"]["clock"]
    added_duration = data["competitions"][0]["status"]["addedClock"]
    match = {
        "league" : data["league"]["name"],
        "date" : data["date"],
        "home_team" : data["competitions"][0]["competitors"][0]["team"]["displayName"],
        "away_team" : data["competitions"][0]["competitors"][1]["team"]["displayName"],
        "winner" : winner,
        "home_team_goals" : home_team_goals,
        "away_team_goals" : away_team_goals,
        "score": f"{home_team_goals} - {away_team_goals}",
        "venue" : data["competitions"][0]["venue"]["fullName"],
        "attendance" : data["competitions"][0]["attendance"],
        "duration" : f"{normal_duration} + {added_duration}"
    }
    return match

def save_to_dataframe(data_list: list, dirname: str, filename: str) -> None:
    dirname = os.path.join("data", dirname)
    os.makedirs(dirname, exist_ok=True)
    file_path = os.path.join(dirname, filename)
    df = pd.DataFrame(data_list)
    df.to_csv(file_path, index=False)

def get_league_name(url: str) -> str:
    return url.split("/")[6]

def get_team_ids(league_id: str) -> list:
    team_ids = []
    url = f"https://site.api.espn.com/apis/site/v2/sports/soccer/{league_id}/teams"
    data = request_data(url)

    for i in range(0, len(data["sports"][0]["leagues"][0]["teams"])):
        team_ids.append(data["sports"][0]["leagues"][0]["teams"][i]["team"]["id"])
    return team_ids

def generate_league_team_urls(league_id: str) -> list:
    team_urls = []
    team_ids = get_team_ids(league_id)
    for team_id in team_ids:
        url = f"https://site.api.espn.com/apis/site/v2/sports/soccer/{league_id}/teams/{team_id}/schedule"
        team_urls.append(url)
    return team_urls

def get_data():
    urls = []
    urls.extend(generate_league_team_urls("ger.1"))
    # urls.extend(generate_league_team_urls("eng.1"))
    # urls.extend(generate_league_team_urls("ita.1"))

    for url in urls:
        match_list = []
        data = request_data(url)

        for i in range(0, len(data["events"])):
            match = format_data(data["events"][i])
            match_list.append(match)

        league = match_list[0]["league"].replace(' ', '_').lower()
        team_name = data["team"]["name"].replace(' ', '_').lower() + ".csv"
        
        save_to_dataframe(match_list, league, team_name)
    

if __name__ == "__main__":
    get_data()

