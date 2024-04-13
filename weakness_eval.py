import pandas as pd
import os

def evaluate_csv_files(csv_directory):
    teams_data = []
    errors = []

    for csv_file in os.listdir(csv_directory):
        if not csv_file.endswith('.csv'):
            continue
        
        file_path = os.path.join(csv_directory, csv_file)
        try:
            df = pd.read_csv(file_path)
            if 'Team' not in df.columns:
                raise ValueError("Expected 'Team' column not found.")
        except Exception as e:
            errors.append(f"Error reading {csv_file}: {e}")
            continue
        
        csv_name = csv_file[:-4]
        parts = csv_name.split('-', 2)
        if len(parts) != 3:
            errors.append(f"Error: File name '{csv_file}' does not match expected format.")
            continue
        
        gc, time, position = parts
        time_split = f"{gc}-{time}"
        
        for stat in df.columns[1:]:
            try:
                df_sorted = df.sort_values(by=stat)
            except KeyError:
                errors.append(f"Key error: '{stat}' not found in {csv_file}.")
                continue
            
            if df_sorted.empty:
                continue
            
            top_5 = df_sorted.tail(5)
            bottom_5 = df_sorted.head(5)
            
            for rank, row in enumerate(top_5.itertuples(index=False), 1):
                teams_data.append({
                    'Team': row.Team,
                    'Rank': f'Top {rank}',
                    'Statistic': stat,
                    'Value': getattr(row, stat),
                    'Time Split': time_split,
                    'Position': position
                })
            for rank, row in enumerate(bottom_5.itertuples(index=False), 1):
                teams_data.append({
                    'Team': row.Team,
                    'Rank': f'Bottom {rank}',
                    'Statistic': stat,
                    'Value': getattr(row, stat),
                    'Time Split': time_split,
                    'Position': position
                })

    return teams_data, errors

# Example usage
directory = 'path/to/your/csv/files'
teams_data, errors = evaluate_csv_files(directory)
if errors:
    print("Errors encountered:", errors)
else:
    print(pd.DataFrame(teams_data))
