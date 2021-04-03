/* App frontend script */

function constructCorpus(){
  var connectDBUrl  = "http://127.0.0.1:5000/constructCorpus";
  AP.request(connectDBUrl, {
    success: function(responseText){
    alert("Construct Corpus");
    //alert(responseText);
    }
  });
}

var a_list=[];
var keyname="";

function formChanged(){
  
  document.getElementById("targetIssue").style.display = "block";

  keyname = document.getElementsByName("keyname")[0].value;
  //alert(keyname);
  var suggestionUrl  = "http://127.0.0.1:5000/suggested/";
  suggestionUrl=suggestionUrl+"?keyname=";
  suggestionUrl=suggestionUrl+keyname;
  
  //alert(suggestionUrl); 

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
      a_list = JSON.parse(responseText);
      alert(a_list);
      
      document.getElementById("ShowSuggestionList").style.display = "block";


      tempImage = "<img src='https://cdn.pixabay.com/photo/2016/08/08/09/17/avatar-1577909_960_720.png' width='20'>";

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
         
         nm1.innerHTML = a_list[0]["name"];
         nm2.innerHTML = a_list[1]["name"];
         nm3.innerHTML = a_list[2]["name"];
         nm4.innerHTML = a_list[3]["name"];
         nm5.innerHTML = a_list[4]["name"];


      }
  });  
}

function showIssue(){

}

function rowClicked(id){
  //var rowID = x.id;
  //alert(a_list);
  var idToAssign = "";
  //var rowValue = document.getElementById(id).innerHTML;
  alert("row clicked for rowID: "+id);
  if (String(id)=="r1"){
    alert("dhukse");
    //valueToSet = document.getElementById("name_r1").innerHTML;
    nameToSet = a_list[0]["name"];
    idToAssign = a_list[0]["account_id"];
    //alert(nameToSet);
  }

  else if (String(id)=="r2"){
    //alert("dhukse");
    //valueToSet = document.getElementById("name_r1").innerHTML;
    nameToSet = a_list[1]["name"];
    idToAssign = a_list[1]["account_id"];
    //alert(nameToSet);
  }

  else if (String(id)=="r3"){
    //alert("dhukse");
    //valueToSet = document.getElementById("name_r1").innerHTML;
    nameToSet = a_list[2]["name"];
    idToAssign = a_list[2]["account_id"];
    //alert(nameToSet);
  }

  else if (String(id)=="r4"){
    //alert("dhukse");
    //valueToSet = document.getElementById("name_r1").innerHTML;
    nameToSet = a_list[3]["name"];
    idToAssign = a_list[3]["account_id"];
    //alert(nameToSet);
  }

  else if (String(id)=="r5"){
    //alert("dhukse");
    //valueToSet = document.getElementById("name_r1").innerHTML;
    nameToSet = a_list[4]["name"];
    idToAssign = a_list[4]["account_id"];
    //alert(nameToSet);
  }

  //var idToAssign = "5e299526bf04010e70c42927";

  var changeAssigneeUrl  = "http://127.0.0.1:5000/change/";
  changeAssigneeUrl = changeAssigneeUrl + "?keyname=";
  changeAssigneeUrl = changeAssigneeUrl + keyname;
  changeAssigneeUrl = changeAssigneeUrl + "&idToAssign=";
  changeAssigneeUrl = changeAssigneeUrl + idToAssign;

  //alert(changeAssigneeUrl);

  AP.request(changeAssigneeUrl, {
    success: function(responseText){
    //alert("Change hoise to");
    //var rt = JSON.parse(responseText);
    //alert(responseText);
    }
  });

}

function fileUpload(){
  //file = document.getElementById("file").innerHTML;
  //var upload  = "http://127.0.0.1:5000/upload/?file=";
  //upload = upload + file;
  //alert("Successfully Uploaded");
}

function buttonClicked() {
  valueToSet = document.getElementById("r1").innerHTML;
  //alert(valueToSet);
  //alert("Assignee Changed")

  //document.getElementById("r1").innerHTML = "Assignee Changed!";
  var changeAssigneeUrl  = "http://127.0.0.1:5000/change/";
  changeAssigneeUrl = changeAssigneeUrl + "?keyname=";
  changeAssigneeUrl = changeAssigneeUrl + keyname;
  AP.request(changeAssigneeUrl, {
    success: function(responseText){
    var rt = JSON.parse(responseText);
    alert(rt);
    }
  });

}

function uploaded() {
  skills = document.getElementsByName("skills")[0].value;
  alert(skills);
  experience = document.getElementsByName("experience")[0].value;
  alert(experience);
  
  var uploadUrl  = "http://127.0.0.1:5000/uploaded/";
  uploadUrl=uploadUrl+"?skills=";
  uploadUrl=uploadUrl+skills;
  uploadUrl = uploadUrl + "&experience=";
  uploadUrl = uploadUrl + experience;
  
  alert(uploadUrl); 
  //document.getElementById("r1").innerHTML = "Assignee Changed!";
 
  AP.request(uploadUrl, {
    success: function(responseText){
    alert("Change hoise to");
    alert(responseText);
    }
  });

}

function formSubmitted(){
  document.getElementById("myAlert").style.display = "block";
  document.getElementById("myForm").style.display = "none";

  setTimeout(function(){ 
    document.getElementById("myAlert").style.display = "none";
    document.getElementById("myForm").style.display = "block";
    document.getElementById("myForm").reset();
  }, 2000);
}

function openTab(evt, tabName) {
  // Declare all variables
  var i, tabcontent, tablinks;

  // Get all elements with class="tablinks" and remove the class "active"
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace("w3-blue", "");
  }

  if(tabName=="Suggestion"){
  	document.getElementById(tabName).style.display = "block";
    //document.getElementById("ShowAllUnassigned").style.display = "none";
    document.getElementById("NewDev").style.display = "none";
  }

  /*if(tabName=="ShowAllUnassigned"){
  	document.getElementById(tabName).style.display = "block";
    document.getElementById("Suggestion").style.display = "none";
    document.getElementById("NewDev").style.display = "none";
  }*/

  if(tabName=="NewDev"){
  	document.getElementById(tabName).style.display = "block";
    document.getElementById("Suggestion").style.display = "none";
    //document.getElementById("ShowAllUnassigned").style.display = "none";
  }
  //evt.currentTarget.className += " active";
  evt.currentTarget.className += " w3-blue";
}