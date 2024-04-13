import html

def generate_html_table(teams_data):
    # Input validation and handling
    if not isinstance(teams_data, list) or not all(isinstance(item, dict) for item in teams_data):
        raise ValueError("Input should be a list of dictionaries.")
    
    if not teams_data:
        return "<p>No data available.</p>"
    
    required_keys = {'Team', 'Rank', 'Statistic', 'Value', 'Time Split', 'Position'}
    if not all(required_keys.issubset(set(item.keys())) for item in teams_data):
        raise ValueError("Each item must contain all required keys: Team, Rank, Statistic, Value, Time Split, Position.")
    
    # Start building the HTML table with some basic CSS for styling
    html_output = '<style>table {width: 100%; border-collapse: collapse;} th, td {border: 1px solid black; padding: 8px; text-align: left;} th {background-color: #f2f2f2;}</style>'
    html_output += '<table>\n'
    
    # Add table headers
    html_output += '<tr>'
    html_output += '<th>Team</th>'
    html_output += '<th>Rank</th>'
    html_output += '<th>Statistic</th>'
    html_output += '<th>Value</th>'
    html_output += '<th>Time Split</th>'
    html_output += '<th>Position</th>'
    html_output += '</tr>\n'
    
    # Add table rows
    for data in teams_data:
        html_output += '<tr>'
        html_output += f'<td>{html.escape(str(data["Team"]))}</td>'
        html_output += f'<td>{html.escape(str(data["Rank"]))}</td>'
        html_output += f'<td>{html.escape(str(data["Statistic"]))}</td>'
        html_output += f'<td>{html.escape(str(data["Value"]))}</td>'
        html_output += f'<td>{html.escape(str(data["Time Split"]))}</td>'
        html_output += f'<td>{html.escape(str(data["Position"]))}</td>'
        html_output += '</tr>\n'
    
    # Close the HTML table
    html_output += '</table>'
    
    return html_output

# Example usage:
# data = [{'Team': 'Lakers', 'Rank': 1, 'Statistic': 'Points Per Game', 'Value': '112.5', 'Time Split': '2020', 'Position': 'Guard'}]
# print(generate_html_table(data))
