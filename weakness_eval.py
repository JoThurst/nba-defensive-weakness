import pandas as pd
import os

def evaluate_csv_files(csv_directory):
    # List to store top and bottom 5 ranking teams for each statistic
    teams_data = []

    # Iterate through each CSV file in the directory
    for csv_file in os.listdir(csv_directory):
        # Skip any non-CSV files
        if not csv_file.endswith('.csv'):
            continue

        # Read the CSV file
        df = pd.read_csv(os.path.join(csv_directory, csv_file))

        # Remove the '.csv' extension from the file name
        csv_name = csv_file[:-4]

        # Split the remaining string at the first occurrence of '-' to extract Time Split and Position
        parts = csv_name.split('-', 2)
        if len(parts) != 3:
            print(f"Error: File name '{csv_file}' does not match expected format. Skipping...")
            continue

        gc,time, position = parts
        time_split = gc+'-'+time

        # Iterate through each statistic column
        for stat in df.columns[1:]:
            # Sort the DataFrame by the statistic column in ascending order
            sorted_df = df.sort_values(by=stat)

            # Extract the top and bottom 5 ranking teams for the statistic
            top_5 = sorted_df.tail(5)
            bottom_5 = sorted_df.head(5)

            # Append top and bottom 5 ranking teams to the list
            for rank, (index, row) in enumerate(top_5.iterrows(), 1):
                teams_data.append({
                    'Team': row['Team'],
                    'Rank': f'Top {rank}',
                    'Statistic': stat,
                    'Value': row[stat],
                    'Time Split': time_split,
                    'Position': position  # Get the Position value if it exists, else None
                })
            for rank, (index, row) in enumerate(bottom_5.iterrows(), 1):
                teams_data.append({
                    'Team': row['Team'],
                    'Rank': f'Bottom {rank}',
                    'Statistic': stat,
                    'Value': row[stat],
                    'Time Split': time_split,
                    'Position': position  # Get the Position value if it exists, else None
                })

    return teams_data
