import requests
import json

def request_data(url: str) -> json:
    response = requests.get(url)
    return response.json()

def format_data(data: json) -> json:
    match = {
        "home_team" : data["competitions"][0]["competitors"][0]["team"]["displayName"],
        "away_team" : data["competitions"][0]["competitors"][1]["team"]["displayName"],
        "home_team_goals" : data["competitions"][0]["competitiors"][0]["score"]["value"],
        "away_team_goals" : data["competitions"][0]["competitiors"][1]["score"]["value"],
        "score" : f"{data['home_team']['goals']} - {data['away_team']['goals']}",
        "date" : data["date"],
        "venue" : data["competitions"][0]["venue"]["fullName"],
        "attendance" : data["competitions"][0]["attendance"],
        "duration" : f"{data["competitions"][0]["status"]["clock"] + data["competitions"][0]["status"]["addedClock"]},
    }
    return match

def get_data():
    urls = [
        "https://site.api.espn.com/apis/site/v2/sports/soccer/ita.1/teams/103/schedule",

    ]

    for url in urls:
        data = request_data(url)
        for i in range(0, len(data["events"])):
            match = format_data(data["events"][i])
            pass
    
    pass
