import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import time
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, filename='scrape_log.log', filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s')

def scrape_defense_data(url):
    """
    Scrape defensive weakness data from the given URL and save each category to a separate CSV file.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Failed to fetch data from the website: {e}")
        raise SystemExit(e)

    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', id='data-table')
    if not table:
        logging.error("No table found with the specified id.")
        raise ValueError("No table found with the specified id.")

    # Creating a directory with date
    date_str = datetime.now().strftime('%Y-%m-%d')
    directory = f'./defense-data/{date_str}/'
    if not os.path.exists(directory):
        os.makedirs(directory)

    header = table.find('thead')
    if not header:
        logging.error("No table header found, cannot determine columns.")
        raise ValueError("No table header found, cannot determine columns.")
    stats = [stat.text.strip() for stat in header.find_all('th')]

    # Extracting rows based on class names and storing them in different CSV files
    for class_name in ['GC-30', 'GC-7', 'GC-15', 'GC-0']:
        for position in ["ALL", "C", "PF", "SF", "SG", "PG"]:
            class_position = class_name + ' ' + position
            rows = table.find_all('tr', class_=class_position)
            if not rows:
                logging.info(f"No rows found for class '{class_name}' and position '{position}'")
                continue

            data = [[cell.text.strip() for cell in row.find_all(['th', 'td'])] for row in rows]
            df = pd.DataFrame(data, columns=stats)
            if df.isnull().values.any():
                logging.warning(f"Data integrity issue found in '{class_name}-{position}'. Missing data present.")

            csv_name = os.path.join(directory, f'{class_name}-{position}.csv')
            df.to_csv(csv_name, index=False)
            logging.info(f"Data for class '{class_name}' and position '{position}' saved successfully to '{csv_name}'")

            # Throttling requests to respect server load
            time.sleep(1)

# Example usage
url = 'https://www.fantasypros.com/nba/defense-vs-position.php?year=2023'
scrape_defense_data(url)
