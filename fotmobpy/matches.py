import pandas as pd
import requests

MATCH_URL = "https://www.fotmob.com/matches?date="

def get_all_matches(date: str) -> pd.DataFrame:
	r = requests.get(MATCH_URL + date).json()
	matches = []

	for league in r["leagues"]:
		for match in league["matches"]:
			home_score = match["home"]["score"] if match["status"]["finished"] else None
			away_score = match["away"]["score"] if match["status"]["finished"] else None
			matches.append(
				{
					"id": match["id"], 
					"country": league["ccode"],
					"league": league["name"],
					"home_id": match["home"]["id"],
					"home_name": match["home"]["longName"],
					"home_score": home_score,
					"away_id": match["away"]["id"],
					"away_name": match["away"]["longName"],
					"away_score": away_score
				}
			)
	
	return pd.DataFrame(matches)


def get_team_matches(date: str, team: str) -> pd.DataFrame:
	team = team.lower()
	r = requests.get(MATCH_URL + date).json()
	matches = []

	for league in r["leagues"]:
		for match in league["matches"]:
			if match["home"]["longName"].lower() == team or match["away"]["longName"].lower() == team:
				home_score = match["home"]["score"] if match["status"]["finished"] else None
				away_score = match["away"]["score"] if match["status"]["finished"] else None
				matches.append(
					{
						"id": match["id"], 
						"country": league["ccode"],
						"league": league["name"],
						"home_id": match["home"]["id"],
						"home_name": match["home"]["longName"],
						"home_score": home_score,
						"away_id": match["away"]["id"],
						"away_name": match["away"]["longName"],
						"away_score": away_score
					}
				)
	
	return pd.DataFrame(matches)


def get_league_matches(date: str, country: str, league_name: str=None) -> pd.DataFrame:
	country = country.lower()
	r = requests.get(MATCH_URL + date).json()
	matches = []

	for league in r["leagues"]:
		if league["ccode"].lower() == country:
			for match in league["matches"]:
				if league_name is not None and league["name"].lower() != league_name.lower():
					continue
				home_score = match["home"]["score"] if match["status"]["finished"] else None
				away_score = match["away"]["score"] if match["status"]["finished"] else None
				matches.append(
					{
						"id": match["id"],
						"country": league["ccode"],
						"league": league["name"],
						"home_id": match["home"]["id"],
						"home_name": match["home"]["longName"],
						"home_score": home_score,
						"away_id": match["away"]["id"],
						"away_name": match["away"]["longName"],
						"away_score": away_score
					}
				)

	return pd.DataFrame(matches)