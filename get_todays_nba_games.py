import requests
from datetime import datetime
import json

# Function to get the list of NBA games for today
def get_nba_games(api_key):
    # Get today's date
    today = datetime.now().strftime('%Y-%m-%d')
    
    # API endpoint for NBA games
    url = f'http://api.balldontlie.io/v1/games?start_date={today}&end_date={today}&per_page=100'

    # Set the request headers with the API key
    headers = {'Authorization': api_key}

    # Send a GET request to the API with the headers
    response = requests.get(url, headers=headers)

    # Check if the response status code is not 200 (OK)
    if response.status_code != 200:
        raise ValueError(f"Failed to fetch NBA games for today. Status code: {response.status_code}")

    try:
        # Parse response as JSON
        data = response.json()
        # Extract the list of games
        games = data['data']
        # Extract the teams playing in each game
        teams_playing = set()
        matchups = set()
        for game in games:
            teams_playing.add(game['home_team']['full_name'])
            teams_playing.add(game['visitor_team']['full_name'])
            matchups.add(game['home_team']['full_name'] + ' vs ' + game['visitor_team']['full_name'])
        
        matchup_list= list(matchups)
          # Use indent=2 for pretty formatting

        # Write JSON data to file
        with open('nba_matchups.json', 'w') as f:
            json.dump(matchup_list, f)
            
        return teams_playing
    except Exception as e:
        print("Error parsing JSON response:", e)
        return set()

# # Get the list of NBA games for today
# api_key = '8473fbc8-8d5e-4124-a96b-abd4819dec3f'  # Replace with your actual API key
# try:
#     teams_playing_today = get_nba_games(api_key)
#     print("Successfully fetched NBA games for today:", teams_playing_today)
# except ValueError as ve:
#     print(ve)

