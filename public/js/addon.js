/* App frontend script */

function formChanged(){
    var keyname = document.getElementsByName("keyname")[0].value;
    //alert(keyname);
    //var suggestionUrl  = "http://127.0.0.1:5000/suggested/";
    var suggestionUrl = "https://my-subdomain.herokuapp.com/suggested"
    suggestionUrl=suggestionUrl+"?keyname=";
    suggestionUrl=suggestionUrl+keyname;
    //alert(suggestionUrl);
    AP.request(suggestionUrl, {
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


    
        //var AssigneeTable = document.getElementById("assigneeTable");
        var row1 = document.getElementById("r1");
        var row2 = document.getElementById("r2");
        var row3 = document.getElementById("r3");
        var row4 = document.getElementById("r4");
        var row5 = document.getElementById("r5");
        //console.log(a_list[0][1]);
        //console.log(a_list[0][2]);
        row1.innerHTML = a_list[0][0];
        row2.innerHTML = a_list[0][1];
        row3.innerHTML = a_list[0][2];
        row4.innerHTML = a_list[0][3];
        row5.innerHTML = a_list[0][4];
        
        /*for(i=0;i<5;i++){
            var newRow = AssigneeTable.insertRow(-1);
            var newCellAssignee = newRow.insertCell(0);
            var newCellAssigneeName = newRow.insertCell(1);
            //story icon
            newCellAssignee.innerHTML = a_list[0][i];
            //newCellAssigneeName.innerHTML=formdata;
    
            //AssigneeTable.deleteRow(1);
        }*/
    
    
        }
    });
}
