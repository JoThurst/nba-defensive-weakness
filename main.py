from def_weakness import scrape_defense_data
from get_todays_nba_games import get_nba_games
from weakness_eval import evaluate_csv_files
from generate_html import generate_html_table
from vizualize_weakness import visualize_team_data
from bs4 import BeautifulSoup

#RUN DEF Weaknesses
url = 'https://www.fantasypros.com/nba/defense-vs-position.php?year=2023'
scrape_defense_data(url)

# Directory containing CSV files
csv_directory = './defense-data'

# Call the function to evaluate CSV files and store the textual outputs
weakness_data = evaluate_csv_files(csv_directory)
# Call the function with the weakness data
visualize_team_data(weakness_data)

# Generate HTML table
html_table = generate_html_table(weakness_data)

# Write HTML table to a file
with open('teams_data.html', 'w') as f:
    f.write(html_table)
