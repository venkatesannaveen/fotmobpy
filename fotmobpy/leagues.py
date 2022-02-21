import requests
import pkg_resources
import pandas as pd

def get_league_ids(country: str=None, league: str=None) -> pd.DataFrame:
    data_path = pkg_resources.resource_filename("fotmobpy.assets", "leagues.csv")
    df = pd.read_csv(data_path)
    if country is not None:
        df = df[df["country"] == country].copy()
    if league is not None:
        df = df[df["league"] == league].copy()

    return df
