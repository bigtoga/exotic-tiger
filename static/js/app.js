// Step 1: Get the data 
// Retrieve data from the CSV file and execute everything below


// Step 3: Define an arrow function that builds the HTML table
// OMG my brain hurts w javascript arrow functions syntax
var loadTableRows = (whichData) => { // Parameter "whichData" is the data to loop through; makes this re-usable
	// Step 1: Delete the previously loaded table rows (if there were any)
    tbody.html("");
	
	// Step 2: Loop through "whichData" and add new table row for each row 
	whichData.forEach(dataRow => { // Loop through each row:
		// 2.1: Add a new row
		var tblRow = tbody.append("tr");  
		
		// 2.2: Loop through each column and add it as a new table cell
		tblColumns.forEach(column => tblRow.append("td").text(dataRow[column]))
	});

	//console.log(tableData);
}

var tableData = [];
d3.csv("/static/data/final_Chicago_data_total_crime_by_date_and_type.csv").then(function(crimeData, err) {
	if (err) {
		//throw err;
		console.log("")
	}
  
	// parse data
	// date,primary_type,crimes_committed
	crimeData.forEach(function(csvdata) {
		//csvdata.date = parseTime(csvdata.date),
		csvdata.date = csvdata.date;
		csvdata.primary_type = csvdata.primary_type;
		csvdata.crimes_committed = +csvdata.crimes_committed;
	});

	tableData = crimeData;
	// console.log(tableData);

	// Step 4: call the function (default / first page load only)
	loadTableRows(tableData);
});

tblColumns = ["date", "primary_type", "crimes_committed"];	

// Step 2: Create HTML object references
var tbody = d3.select("tbody");
var btnSearch = d3.select("#btnSearch");
var btnReset = d3.select("#btnReset");

var searchDate = d3.select("#searchDate");
var searchCrime = d3.select("#searchCrime");


/**********************************
 Event Listeners 
**********************************/

// Search button - click event
btnSearch.on("click", () => {
	// Setup: Prevent the page from refreshing on events
	d3.event.preventDefault();
	
	// Business rule: use the first text box w a value as only search term:
	
	// 1. Get what the user searched for:
    var searchedDate = searchDate.property("value");
    var searchedCrime = searchCrime.property("value");
		
	if(searchedDate){
3		// console.log(searchedDate)
		// 2. Filter the data
		var tableData_Filtered = tableData.filter(tableData => tableData.date === searchedDate);
	
		// 3. Load the new data
		if(tableData_Filtered.length !== 0) {
			loadTableRows(tableData_Filtered);
		}
		else {
			// Clear out the previously loaded HTML:
			tbody.html("");
			
			// Tell them "No rows match"
			tbody.append("tr").append("td").text("You are unlucky - no crimes on this date");
		}
	}
	else if(searchedCrime) {
		// 2. Filter the data
		var tableData_Filtered = tableData.filter(tableData => tableData.primary_type === searchedCrime);
	
		// 3. Load the new data
		if(tableData_Filtered.length !== 0) {
			loadTableRows(tableData_Filtered);
		}
		else {
			// Clear out the previously loaded HTML:
			tbody.html("");
			
			// Tell them "No rows match"
			tbody.append("tr").append("td").text("You are unlucky - no sightings for this city");
		}
	}
})

// Reset button - click 
btnReset.on("click", () => {
	// window.location.href = "index.html";
	document.getElementById("searchDate").value='';
	document.getElementById("searchCrime").value='';
	
	// Load original dataset
	loadTableRows(tableData);
})