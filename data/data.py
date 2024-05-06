import requests
import json
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

def save_to_dataframe(data_list: list, filename: str) -> None:
    df = pd.DataFrame(data_list)
    df.to_csv(filename, index=False)

def get_league_name(url: str) -> str:
    return url.split("/")[6]


def get_data():
    urls = [
        "https://site.api.espn.com/apis/site/v2/sports/soccer/ita.1/teams/103/schedule",

    ]

    for url in urls:
        match_list = []
        data = request_data(url)

        for i in range(0, len(data["events"])):
            match = format_data(data["events"][i])
            match_list.append(match)

        league_name = match_list[0]["league"]
        save_to_dataframe(match_list, f"{league_name}.csv")
    

if __name__ == "__main__":
    get_data()

