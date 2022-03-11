import requests
import pkg_resources
import pandas as pd

LEAGUES_URL = "https://www.fotmob.com/leagues?id="

def get_league_ids(country: str=None, league: str=None) -> pd.DataFrame:
    data_path = pkg_resources.resource_filename("fotmobpy.assets", "leagues.csv")
    df = pd.read_csv(data_path)
    if country is not None:
        df = df[df["country"] == country].copy()
    if league is not None:
        df = df[df["league"] == league].copy()

    return df

def get_league_table(league_id: int) -> pd.DataFrame:
    r = requests.get(LEAGUES_URL + str(league_id))
    r.raise_for_status()

    r = r.json()
    if r["tableData"] is None:
        raise Exception(f"Invalid league ID {r['details']['id']}")
    table = []
    for team in r["tableData"][0]["table"]["all"]:
        table.append(
            {
                "team_id": team["id"],
                "name": team["name"],
                "games_played": team["played"],
                "win": team["wins"],
                "loss": team["losses"],
                "draw": team["draws"],
                "goals_scored": int(team["scoresStr"].split("-")[0]),
                "goals_conceded": int(team["scoresStr"].split("-")[1]),
                "goal_difference": team["goalConDiff"],
                "points": team["pts"]
            }
        )
    return (
        pd.DataFrame(table)
        .sort_values("points", ascending=False)
        .reset_index(drop=True)
    )