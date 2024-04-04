function create_teams_data() {
    const teamsData = {};
    fetch('nba_weakness_data.json')
        .then(response => response.json())
        .then(data => {
            // Group data by team and position
            data.forEach(team => {
                const teamName = team.Team;
                const position = team.Position;
                if (!teamsData[teamName]) {
                    teamsData[teamName] = {};
                }
                if (!teamsData[teamName][position]) {
                    teamsData[teamName][position] = {};
                }
                // Store data by time split and statistic
                if (!teamsData[teamName][position][team["Time Split"]]) {
                    teamsData[teamName][position][team["Time Split"]] = {};
                }
                teamsData[teamName][position][team["Time Split"]][team.Statistic] = team.Rank;
            });

            console.log(teamsData);

            // Generate HTML tables
            generateTablesHtml(teamsData);
        })
        .catch(error => {
            console.error('Error fetching JSON data:', error);
        });
}

function generateTablesHtml(teamsData) {
    let tablesHtml = '';
    for (const [teamName, positions] of Object.entries(teamsData)) {
        for (const [position, timeSplits] of Object.entries(positions)) {
            tablesHtml += `
                <div class="table-responsive">
                    <h3 class="mt-4">${teamName} - ${position}</h3>
                    <table class="table table-bordered">
                        <thead>
                            <tr>
                                <th>Statistic</th>
                                <th>GC-0</th>
                                <th>GC-7</th>
                                <th>GC-15</th>
                                <th>GC-30</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${generateTableRows(timeSplits)}
                        </tbody>
                    </table>
                </div>
            `;
        }
    }
    document.getElementById('tables-container').innerHTML = tablesHtml;
}

function generateTableRows(timeSplits) {
    let tableRows = '';
    Object.keys(timeSplits).forEach(timeSplit => {
        Object.keys(timeSplits[timeSplit]).forEach(statistic => {
            tableRows += `
                <tr>
                    <td>${statistic}</td>
                    <td>${timeSplits[timeSplit][statistic]['GC-0'] || ''}</td>
                    <td>${timeSplits[timeSplit][statistic]['GC-7'] || ''}</td>
                    <td>${timeSplits[timeSplit][statistic]['GC-15'] || ''}</td>
                    <td>${timeSplits[timeSplit][statistic]['GC-30'] || ''}</td>
                </tr>
            `;
        });
    });
    return tableRows;
}


// Call the function to fetch and process data
create_teams_data();
