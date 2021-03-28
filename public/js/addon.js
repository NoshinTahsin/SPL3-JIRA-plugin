/* App frontend script */
function formChanged(){
    var keyname = document.getElementsByName("keyname")[0].value;
    alert(keyname);
    var suggestionUrl  = "http://127.0.0.1:5000/suggested/";
    //var suggestionUrl  = "http://127.0.0.1:5000/hello/";
    //var suggestionUrl = "https://thingproxy.freeboard.io/fetch/https://my-subdomain.herokuapp.com/suggested/"
    //suggestionUrl=suggestionUrl+"?keyname=";
    //suggestionUrl=suggestionUrl+keyname;
    alert(suggestionUrl); 

    /*fetch(suggestionUrl)
    .then(function (response) {
      alert(response.json());
      return response.json(); // But parse it as JSON this time
    })
    .then(function (json) {
        console.log('GET response as JSON:');
        console.log(json); // Here’s our JSON object
        alert(response.json());
    })*/

    var tempImage ="";
    //a=["lucille.hogan","isabel.richardson","marsha.cook","joshua.maples","jerome.johnson"];
    //works
    AP.request('/rest/api/3/issue/'+keyname, {
        success: function(responseText){
          
            var data = JSON.parse(responseText);
            des=data["fields"]["description"]["content"][0];
            var IssueTable = document.getElementById("issueTable");
            var newRow = IssueTable.insertRow(-1);
            var newCellType = newRow.insertCell(0)
            var newCellSummary = newRow.insertCell(1);
            var newCellDescription = newRow.insertCell(2);
            var newCellKey = newRow.insertCell(3);
            var newCellPriority = newRow.insertCell(4);
            var newCellCreator = newRow.insertCell(5);
    
            //story icon
            newCellType.innerHTML = "<img src='" + data["fields"]["issuetype"]["iconUrl"] + "' width='16'>";
            newCellSummary.innerHTML =  data["fields"]["summary"] ;
            newCellDescription.innerHTML = des["content"][0]["text"];
            newCellKey.innerHTML = data["key"];
            newCellPriority.innerHTML = "<img src='"+data["fields"]["priority"]["iconUrl"]+"' width='16'>";
            newCellCreator.innerHTML = data["fields"]["creator"]["displayName"];
    
            IssueTable.deleteRow(1); //works

            tempImage = "<img src='" + data["fields"]["assignee"]["avatarUrls"]["24x24"]+"' width='24'>";
            //need to return the list here from flask
    
           /* var showIssue = document.getElementById("issue");
            showIssue.innerHTML = "key: "+data["key"]+
                                    "<br> priority: "+data["fields"]["priority"]["name"]+
                                    "<br> status: "+ data["fields"]["status"]["name"]+
                                    "<br> description: "+des["content"][0]["text"]+
                                    "<br> summary: "+data["fields"]["summary"]+
                                    "<br> issue creator: "+ data["fields"]["creator"]["displayName"];
            showIssue.innerHTML = "<img src='" + value.avatarUrls["16x16"] + "' width='16'>";
            showIssue.innerHTML = "<code>" + value.key + "</code>";
            showIssue.innerHTML = "<a href='/browse/" + value.key + "'>" + value.name + "</a>";*/
        }
    });

    //need to run flask
    //working
    AP.request(suggestionUrl, {
        success: function(responseText){
        var a_list = JSON.parse(responseText);
        alert(a_list);

        var AssigneeTable = document.getElementById("assigneeTable");
            for(i=0;i<5;i++)
            {
              var newRow = AssigneeTable.insertRow(-1);
              var newCellAssignee = newRow.insertCell(0);
              var newCellAssigneeID = newRow.insertCell(1);
              var newCellAssigneeName = newRow.insertCell(2);
              //story icon
              newCellAssignee.innerHTML = tempImage;
              newCellAssigneeID.innerHTML=a_list[0][i+5];
              newCellAssigneeName.innerHTML=a_list[0][i];
      
              //AssigneeTable.deleteRow(1);
           }
        

        /*var row1 = document.getElementById("r1");
        var row2 = document.getElementById("r2");
        var row3 = document.getElementById("r3");
        var row4 = document.getElementById("r4");
        var row5 = document.getElementById("r5");
       
        row1.innerHTML = a_list[0][0];
        row2.innerHTML = a_list[0][1];
        row3.innerHTML = a_list[0][2];
        row4.innerHTML = a_list[0][3];
        row5.innerHTML = a_list[0][4];*/

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

function showIssue(){

}


function buttonClicked() {
  valueToSet = document.getElementById("r1").innerHTML;
  //alert(valueToSet);
  alert("Assignee Changed")

  //document.getElementById("r1").innerHTML = "Assignee Changed!";
  var changeAssigneeUrl  = "http://127.0.0.1:5000/change/";
  AP.request(changeAssigneeUrl, {
    success: function(responseText){
    var rt = JSON.parse(responseText);

    }
  });



  
}

