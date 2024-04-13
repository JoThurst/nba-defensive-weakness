function create_teams_data() {
    return new Promise((resolve, reject) => {
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

                resolve(teamsData);
            })
            .catch(error => {
                console.error('Error fetching JSON data:', error);
                reject(error);
            });
    });
}

function generateTablesHtml(teamsData) {
    const tablesByTeam = {};
    for (const [teamName, positions] of Object.entries(teamsData)) {
        tablesByTeam[teamName] = '';
        for (const [position, timeSplits] of Object.entries(positions)) {
            tablesByTeam[teamName] += `
                <div class="table-responsive">
                    <h3 class="mt-4">${teamName} - ${position}</h3>
                    <table class="table table-dark">
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
    return tablesByTeam;
}

// // Function to display tables side by side
// function displayTablesSideBySide(matchups, tablesByTeam) {
//     const matchupContainer = document.getElementById('matchup-container');
//     matchups.forEach(matchup => {
//         const teams = matchup.split(' vs ');
//         const matchupDiv = document.createElement('div');
//         matchupDiv.classList.add('matchup');
//         matchupDiv.innerHTML = `<h2>${matchup}</h2>`;
//         teams.forEach(team => {
//             matchupDiv.innerHTML += tablesByTeam[team];
//         });
//         matchupContainer.appendChild(matchupDiv);
//     });
// }

function generateTablesByTeamAndPosition(teamsData) {
    const tablesByTeam = {};

    // Loop through teamsData to organize tables by team and position
    for (const [teamName, positions] of Object.entries(teamsData)) {
        for (const [position, timeSplits] of Object.entries(positions)) {
            const tableHtml = `
                <div class="">
                    <h3 class="mt-4 fw-bold text-center">${teamName} - ${position}</h3>
                    <table class="table table-hover table-responsive table-bordered table-sm">
                        <caption> Defensive Strength/Weaknessess for ${teamName} at ${position} </caption>
                        <thead class="thead-dark">
                            <tr>
                                <th scope="col">Statistic</th>
                                <th scope="col">Season</th>
                                <th scope="col">Last 7</th>
                                <th scope="col">Last 15</th>
                                <th scope="col">Last 30</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${generateTableRows(timeSplits)}
                        </tbody>
                    </table>
                </div>
            `;
            if (!tablesByTeam[teamName]) {
                tablesByTeam[teamName] = {};
            }
            if (!tablesByTeam[teamName][position]) {
                tablesByTeam[teamName][position] = [];
            }
            tablesByTeam[teamName][position].push(tableHtml);
        }
    }

    return tablesByTeam;
}


function displayTablesSideBySide(matchups, tablesByTeam) {
    const container = document.getElementById('tables-container');

    matchups.forEach(matchup => {
        const matchupDiv = document.createElement('div');
        matchupDiv.classList.add('row', 'matchup' );

        // Centered title for the matchup
        const title = document.createElement('h3');
        title.classList.add('matchup-title', 'text-white');
        title.textContent = matchup;
        matchupDiv.appendChild(title);

        const containerFluid = document.createElement('div');
        containerFluid.classList.add('container-fluid');

        let positionCount = 0;
        let containerRow;

        const teams = matchup.split(' vs ');

        // Create an object to store tables for each team in the matchup
        const tablesInMatchup = {};

        teams.forEach(team => {
            tablesInMatchup[team] = [];
        });

        // Group tables by team for this matchup
        for (const team in tablesByTeam) {
            if (teams.includes(team)) {
                const positions = tablesByTeam[team];

                for (const position in positions) {
                    tablesInMatchup[team].push(positions[position][0]); // Assuming there's only one table per position
                }
            }
        }

        // Create rows and columns for each position in the matchup
        for (const position in tablesInMatchup[teams[0]]) {
            // Create a new row for each position
            containerRow = document.createElement('div');
            containerRow.classList.add('row' , 'nba-table-row' , 'bg-white');
            containerFluid.appendChild(containerRow);

            // Create a column for each team
            teams.forEach(team => {
                const colDiv = document.createElement('div');
                colDiv.classList.add('col');
                colDiv.innerHTML = tablesInMatchup[team][position] || ''; // Get the table HTML for the current position and team
                colDiv.querySelectorAll('td').forEach(td => {
                    const content = td.textContent.trim();
                    if (content.includes('Bottom')) {
                        const bottomLevel = parseInt(content.split(' ')[1]);
                        const opacity = bottomLevel / 5;
                        td.style.backgroundColor = `rgba(0, 255, 0, ${opacity})`;
                    } else if (content.includes('Top')) {
                        const topLevel = parseInt(content.split(' ')[1]);
                        const opacity = topLevel / 5;
                        td.style.backgroundColor = `rgba(255, 0, 0, ${opacity})`;
                    }
                });
                containerRow.appendChild(colDiv);
            });

            positionCount++;
        }

        // Create a div to contain all toggle buttons
        const toggleButtonsContainer = document.createElement('div');
        toggleButtonsContainer.classList.add('toggle-buttons-container', 'd-flex', 'justify-content-center', 'my-3');

        // Create a button for toggling each row
        const rowToggles = containerFluid.querySelectorAll('.row');
        rowToggles.forEach((row, index) => {
            const position = Object.keys(tablesInMatchup[teams[0]])[index];
            const toggleButton = document.createElement('button');
            toggleButton.textContent = position;
            toggleButton.classList.add('toggle-button', 'w-auto', 'btn', 'btn-secondary', 'mx-1');
            toggleButton.addEventListener('click', () => {
                row.classList.toggle('d-none');
            });
            toggleButtonsContainer.appendChild(toggleButton);
        });

        // Create a button for toggling the entire matchup
        const toggleMatchupButton = document.createElement('button');
        toggleMatchupButton.textContent = 'Toggle Matchup';
        toggleMatchupButton.classList.add('toggle-button', 'btn', 'btn-secondary', 'mx-1');
        toggleMatchupButton.addEventListener('click', () => {
            containerFluid.classList.toggle('d-none');
        });
        toggleButtonsContainer.appendChild(toggleMatchupButton);

        // Append the toggle buttons container to the matchup div
        matchupDiv.appendChild(toggleButtonsContainer);
        matchupDiv.appendChild(containerFluid);
        container.appendChild(matchupDiv);
    });
}



function containsStatRowObj(arrayObj, string){
    for (let i = 0; i < arrayObj.length; i++) {
        //console.log(arrayObj[i][0], " " , string)
        if (arrayObj[i][0] === string) {
            console.log("Match Found");
            return i; // Match found
        }
    }
    return false;
}

function generateTableRows(timeSplits) {
    let tableRowsObj = [];
    let tableRows = '';
    Object.keys(timeSplits).forEach(timeSplit => {
        Object.keys(timeSplits[timeSplit]).forEach(statistic => {
            let statrow = [statistic, null, null, null, null, null]
            index = containsStatRowObj(tableRowsObj,statistic)
            if(index === false){
                console.log("False Contains Keeping New Statrow", statrow)
                
            }else{
                console.log("True Grabbing Stored Statrow", index)
                statrow = tableRowsObj[index]
                console.log(statrow)
            }
            
           
            if(tableRowsObj.includes)
            
            timeSplitArray = ["GC-0","GC-7","GC-15","GC-30"];
            for (let index = 0; index < timeSplitArray.length; index++) {
                if(typeof timeSplits[timeSplitArray[index]] === 'undefined' || typeof timeSplits[timeSplitArray[index]] === undefined){
                    console.log('Undefined.. SKIP');

                }else{
                    if(timeSplits[timeSplitArray[index]] !== timeSplits[timeSplit]){

                    }else{
                        //console.log("Defined Statistic ", timeSplits[timeSplitArray[index]][statistic], statistic)

                        statrow[index+1] = timeSplits[timeSplitArray[index]][statistic]
                    }

                }
                
            }
            console.log("Statrow After Loop", statrow)
            if(index === false){
                tableRowsObj.push(statrow);
            }else{
                tableRowsObj[index] = statrow
            }
            

        });
    });

    //console.log(tableRowsObj);
    

    for (let index = 0; index < tableRowsObj.length; index++) {
        tableRows += '<tr> <th scope="row">' + tableRowsObj[index][0] +'</th>' ;
        tableRows += `                
                <td>${tableRowsObj[index][1] || ''}</td>
                <td>${tableRowsObj[index][2] || ''}</td>
                <td>${tableRowsObj[index][3] || ''}</td>
                <td>${tableRowsObj[index][4] || ''}</td>
            </tr>
        `;
        
    }
    
    return tableRows;
}

// Call the function to fetch data and generate tables
async function fetchDataAndGenerateTables() {
    try {
        // Fetch and process data
        const teamsData = await create_teams_data();
        const matchups = ["New York Knicks vs Brooklyn Nets", "Sacramento Kings vs Phoenix Suns", "Dallas Mavericks vs Detroit Pistons", "Miami Heat vs Toronto Raptors", "Boston Celtics vs Charlotte Hornets", "San Antonio Spurs vs Denver Nuggets", "Portland Trail Blazers vs Houston Rockets", "Philadelphia 76ers vs Orlando Magic", "Oklahoma City Thunder vs Milwaukee Bucks", "Cleveland Cavaliers vs Indiana Pacers", "Golden State Warriors vs New Orleans Pelicans", "Washington Wizards vs Chicago Bulls", "LA Clippers vs Utah Jazz", "Memphis Grizzlies vs Los Angeles Lakers", "Minnesota Timberwolves vs Atlanta Hawks"]
        // Generate tables HTML
        const tablesHtml = generateTablesByTeamAndPosition(teamsData);
        console.log(tablesHtml);

        // Display tables side by side
        displayTablesSideBySide(matchups, tablesHtml);
    } catch (error) {
        console.error('Error:', error);
    }
}

// Call the async function
fetchDataAndGenerateTables();