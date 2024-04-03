def generate_html_table(teams_data):
    # Start building the HTML table
    html = '<table border="1">\n'
    
    # Add table headers
    html += '<tr>'
    html += '<th>Team</th>'
    html += '<th>Rank</th>'
    html += '<th>Statistic</th>'
    html += '<th>Value</th>'
    html += '<th>Time Split</th>'
    html += '<th>Position</th>'
    html += '</tr>\n'
    
    # Add table rows
    for data in teams_data:
        html += '<tr>'
        html += f'<td>{data["Team"]}</td>'
        html += f'<td>{data["Rank"]}</td>'
        html += f'<td>{data["Statistic"]}</td>'
        html += f'<td>{data["Value"]}</td>'
        html += f'<td>{data["Time Split"]}</td>'
        html += f'<td>{data["Position"]}</td>'
        html += '</tr>\n'
    
    # Close the HTML table
    html += '</table>'
    
    return html

