import pandas as pd
import matplotlib.pyplot as plt

def visualize_team_data(team_data):
    # Convert data to DataFrame
    df = pd.DataFrame(team_data)

    # Group data by team
    grouped_data = df.groupby('Team')

    # Iterate through each team and display statistics
    for team, group in grouped_data:
        print("Team:", team)
        for index, row in group.iterrows():
            print("Statistic:", row['Statistic'])
            print("Rank:", row['Rank'])
            print("Value:", row['Value'])
            print("Time Split:", row['Time Split'])
            print("Position:", row['Position'])
            print()  # Add a newline for better readability
        print()  # Add an extra newline between teams


