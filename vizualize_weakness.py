import pandas as pd
import matplotlib.pyplot as plt

def visualize_team_data(team_data, teams=None, stats=None):
    # Check input is a DataFrame
    if not isinstance(team_data, pd.DataFrame):
        try:
            df = pd.DataFrame(team_data)
        except Exception as e:
            raise ValueError("Failed to convert input data to DataFrame: " + str(e))
    else:
        df = team_data.copy()

    # Check for necessary columns
    required_columns = {'Team', 'Statistic', 'Time Split', 'Value'}
    if not required_columns.issubset(df.columns):
        missing_cols = required_columns - set(df.columns)
        raise ValueError(f"Missing required columns: {missing_cols}")

    # Filter teams if specified
    if teams is not None:
        df = df[df['Team'].isin(teams)]
        if df.empty:
            raise ValueError("No data found for the specified teams.")

    # Filter statistics if specified
    if stats is not None:
        df = df[df['Statistic'].isin(stats)]
        if df.empty:
            raise ValueError("No data found for the specified statistics.")
    
    # Group data by team
    grouped_data = df.groupby('Team')

    # Prepare the plot
    fig, ax = plt.subplots(figsize=(10, 5))  # Adjust the size as necessary

    # Plot data for each team
    for team, group in grouped_data:
        for statistic in group['Statistic'].unique():
            sub_data = group[group['Statistic'] == statistic]
            ax.plot(sub_data['Time Split'], sub_data['Value'], label=f"{team} {statistic}")
    
    ax.set_xlabel('Time Split')
    ax.set_ylabel('Value')
    ax.set_title('Team Statistics Over Time')
    ax.legend(title='Team Statistic')
    plt.show()

# Example usage:
# visualize_team_data(data, teams=['Lakers', 'Heat'], stats=['Points Per Game', 'Rebounds'])
