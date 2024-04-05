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
            tableRows += '<tr> <td>' + statistic + '</td>';
            timeSplitArray = ["GC-0","GC-7","GC-15","GC-30"];
            for (let index = 0; index < timeSplitArray.length; index++) {
                if(typeof timeSplits[timeSplitArray[index]] === 'undefined' || typeof timeSplits[timeSplitArray[index]] === undefined){
                    console.log('Undefined.. SKIP');

                }else{
                    if(timeSplits[timeSplitArray[index]] !== timeSplits[timeSplit]){

                    }else{
                        console.log("Defined Statistic ", timeSplits[timeSplitArray[index]][statistic], statistic)

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
            

            // tableRows += `
            //     <tr>
            //         <td>${statistic}</td>
            //         <td>${timeSplits['GC-0'][statistic] || ''}</td>
            //         <td>${timeSplits['GC-7'][statistic] || ''}</td>
            //         <td>${timeSplits['GC-15'][statistic] || ''}</td>
            //         <td>${timeSplits['GC-30'][statistic] || ''}</td>
            //     </tr>
            // `;
        });
    });

    console.log(tableRowsObj);
    return tableRows;
}


// Call the function to fetch and process data
create_teams_data();
