import pandas as pd
import requests
from bs4 import BeautifulSoup

def scrape_defense_data(url):
    """
    Scrape defensive weakness data from the given URL and save each category to a separate CSV file.
    """
    # Sending a request to the URL
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError("Failed to fetch data from the website. Status code: {}".format(response.status_code))

    # Parsing the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Finding the data table
    table = soup.find('table', id='data-table')

    # Extracting the header (thead) to distinguish the statistics
    header = table.find('thead')
    stats = [stat.text.strip() for stat in header.find_all('th')]

    # Extracting rows based on class names and storing them in different CSV files
    for class_name in ['GC-30', 'GC-7', 'GC-15', 'GC-0']:
        for position in ["ALL", "C", "PF", "SF", "SG", "PG"]:
            rows = table.find_all('tr', class_=class_name + ' ' + position)
            if not rows:
                print("No rows found for class '{}' and position '{}'".format(class_name, position))
                continue
            csv_name = './defense-data/' + class_name + '-' + position + '.csv'  # Constructing CSV file name
            with open(csv_name, 'w') as f:
                # Writing the header row with statistics
                f.write(','.join(stats) + '\n')
                for row in rows:
                    # Extracting table data into a string
                    data = ','.join([cell.text.strip() for cell in row.find_all(['th', 'td'])])
                    # Writing the data to the CSV file
                    f.write(data + '\n')
            print("Data for class '{}' and position '{}' saved successfully to '{}'".format(class_name, position, csv_name))

# Let's fix the web scraping code to include the thead section and ensure correct storage of statistics.
scrape_defense_data('https://www.fantasypros.com/nba/defense-vs-position.php?year=2023')
