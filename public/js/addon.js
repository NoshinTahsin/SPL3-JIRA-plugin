/* App frontend script */

function formChanged(){
  var keyname = document.getElementsByName("keyname")[0].value;
  alert(keyname);
  var suggestionUrl  = "http://127.0.0.1:5000/suggested/";
  suggestionUrl=suggestionUrl+"?keyname=";
  suggestionUrl=suggestionUrl+keyname;
  
  alert(suggestionUrl); 

  var tempImage ="";
  //a=["lucille.hogan","isabel.richardson","marsha.cook","joshua.maples","jerome.johnson"];
  //works

  //need to get image
  /*AP.request('/rest/api/3/users/search',{
    success: function(responseText){
      var allUserData = JSON.parse(responseText);
      var len=allUserData.length();
      alert(allUserData);
    }
  });*/

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

          //tempImage = "<img src='" + data["fields"]["assignee"]["avatarUrls"]["24x24"]+"' width='24'>";
          //need to return the list here from flask
      }
  });

  //need to run flask
  //working
  AP.request(suggestionUrl, {
      success: function(responseText){
      var a_list = JSON.parse(responseText);
      alert(a_list);

      tempImage = "<img src='https://cdn.pixabay.com/photo/2016/08/08/09/17/avatar-1577909_960_720.png' width='24'>";

      var AssigneeTable = document.getElementById("assigneeTable");
      
        /*for(i=0;i<5;i++)
          {
            var newRow = AssigneeTable.insertRow(-1);
            var newCellAssignee = newRow.insertCell(0);
            //var newCellAssigneeID = newRow.insertCell(1);
            var newCellAssigneeName = newRow.insertCell(1);
            //story icon
            newCellAssignee.innerHTML = tempImage;
           // newCellAssigneeID.innerHTML=a_list[0][i+5];
            newCellAssigneeName.innerHTML=a_list[0][i];
    
            //AssigneeTable.deleteRow(1);
         }*/

         var av1 = document.getElementById("avatar_r1");
         var av2 = document.getElementById("avatar_r2");
         var av3 = document.getElementById("avatar_r3");
         var av4 = document.getElementById("avatar_r4");
         var av5 = document.getElementById("avatar_r5");

         var nm1 = document.getElementById("name_r1");
         var nm2 = document.getElementById("name_r2");
         var nm3 = document.getElementById("name_r3");
         var nm4 = document.getElementById("name_r4");
         var nm5 = document.getElementById("name_r5");

         av1.innerHTML = tempImage;
         av2.innerHTML = tempImage;
         av3.innerHTML = tempImage;
         av4.innerHTML = tempImage;
         av5.innerHTML = tempImage;
         
         nm1.innerHTML = a_list[0][0];
         nm2.innerHTML = a_list[0][1];
         nm3.innerHTML = a_list[0][2];
         nm4.innerHTML = a_list[0][3];
         nm5.innerHTML = a_list[0][4];


      }
  });  


  
}

function showIssue(){

}

function rowClicked(){
  alert("row clicked");
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