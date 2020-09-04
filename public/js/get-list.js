const weatherUrl  = "http://127.0.0.1:5000/weatherReport/";
        
AP.request(weatherUrl, {
    success: function(responseText){
    var a_list = JSON.parse(responseText);
    //alert(responseText);
    /*var IssueTable = document.getElementById("issueTable");
    var newRow = IssueTable.insertRow(-1);
	var newCellType = newRow.insertCell(0)
	var newCellSummary = newRow.insertCell(1);
    var newCellDescription = newRow.insertCell(2);
    var newCellKey = newRow.insertCell(3);
    var newCellPriority = newRow.insertCell(4);
    var newCellCreator = newRow.insertCell(5);

    newCellType.innerHTML = responseText;
    newCellSummary.innerHTML =  responseText ;
    newCellDescription.innerHTML = responseText;
    newCellKey.innerHTML = responseText;
    newCellPriority.innerHTML = responseText;
    newCellCreator.innerHTML = responseText;

    IssueTable.deleteRow(1);*/

    var AssigneeTable = document.getElementById("assigneeTable");
    console.log(a_list[0][1]);
    console.log(a_list[0][2]);
    for(i=0;i<5;i++){
        var newRow = AssigneeTable.insertRow(-1);
        var newCellAssignee = newRow.insertCell(0);
        var newCellAssigneeName = newRow.insertCell(1);
        //story icon
        newCellAssignee.innerHTML = a_list[0][i];
        //newCellAssigneeName.innerHTML=formdata;

        //AssigneeTable.deleteRow(1);
    }


    }
});