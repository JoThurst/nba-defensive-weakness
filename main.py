from def_weakness import scrape_defense_data
from get_todays_nba_games import get_nba_games
from weakness_eval import evaluate_csv_files
from generate_html import generate_html_table
from vizualize_weakness import visualize_team_data
from bs4 import BeautifulSoup
import json

#RUN DEF Weaknesses
#url = 'https://www.fantasypros.com/nba/defense-vs-position.php?year=2023'
#scrape_defense_data(url)

# Directory containing CSV files
csv_directory = './defense-data'

# Call the function to evaluate CSV files and store the textual outputs
weakness_data = evaluate_csv_files(csv_directory)

# Get the list of NBA games for today
api_key = '8473fbc8-8d5e-4124-a96b-abd4819dec3f'  # Replace with your actual API key
try:
    teams_playing_today = get_nba_games(api_key)
    print("Successfully fetched NBA games for today:", teams_playing_today)

    filtered_data = [obj for obj in weakness_data if obj['Team'] in teams_playing_today]
    # Call the function with the weakness data
    visualize_team_data(filtered_data)

    # Generate HTML table
    #html_table = generate_html_table(filtered_data)

    # Write HTML table to a file
    # with open('teams_data.html', 'w') as f:
    #     f.write(html_table)
    # Convert filtered data to JSON
    json_data = json.dumps(filtered_data, indent=2)  # Use indent=2 for pretty formatting

    # Write JSON data to file
    with open('nba_weakness_data.json', 'w') as f:
        f.write(json_data)

    print('Filtered data saved to nba_weakness_data.json')


except ValueError as ve:
    print(ve)



