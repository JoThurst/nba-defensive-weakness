import requests
from datetime import datetime
import json
import os

def fetch_nba_games(api_key):
    today = datetime.now().strftime('%Y-%m-%d')
    url = f'http://api.balldontlie.io/v1/games?start_date={today}&end_date={today}&per_page=100'
    headers = {'Authorization': api_key}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Will raise an exception for HTTP error codes
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
    except requests.exceptions.Timeout:
        print("Request timed out")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
    return None

def process_nba_games(data):
    games = data.get('data', [])
    matchups = []
    teams_playing = set()
    for game in games:
        home_team = game['home_team']['full_name']
        visitor_team = game['visitor_team']['full_name']
        teams_playing.add(home_team)
        teams_playing.add(visitor_team)
        matchups.append(f"{home_team} vs {visitor_team}")
    return teams_playing, matchups

def write_nba_matchups_to_file(matchups, filename='nba_matchups.json'):
    with open(filename, 'w') as f:
        json.dump(matchups, f, indent=2)

# Example usage:
api_key = os.getenv('NBA_API_KEY')  # Assuming you have your API key set in an environment variable
data = fetch_nba_games(api_key)
if data:
    teams_playing, matchups = process_nba_games(data)
    write_nba_matchups_to_file(matchups)
    print("Teams playing today:", teams_playing)
