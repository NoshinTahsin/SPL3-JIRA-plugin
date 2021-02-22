AP.request('/rest/api/3/issue/SAAJ-5', {
	success: function(responseText){
		//var projectTable = document.getElementById("projects");
    //var data = JSON.parse(responseText);
        //let {PythonShell} = require('python-shell');
        //window.alert(name);
        
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

        IssueTable.deleteRow(1);

    

       /* a=["lucille.hogan","isabel.richardson","marsha.cook","joshua.maples","jerome.johnson"];
        var AssigneeTable = document.getElementById("assigneeTable");
        for(i=0;i<5;i++){
        var newRow = AssigneeTable.insertRow(-1);
        var newCellAssignee = newRow.insertCell(0);
        var newCellAssigneeName = newRow.insertCell(1);
        //story icon
        newCellAssignee.innerHTML = "<img src='" + data["fields"]["assignee"]["avatarUrls"]["24x24"]+"' width='24'>";
        newCellAssigneeName.innerHTML=a[i];

        //AssigneeTable.deleteRow(1);
        }*/

        var showIssue = document.getElementById("issue");
        showIssue.innerHTML = "key: "+data["key"]+
                                "<br> priority: "+data["fields"]["priority"]["name"]+
                                "<br> status: "+ data["fields"]["status"]["name"]+
                                "<br> description: "+des["content"][0]["text"]+
                                "<br> summary: "+data["fields"]["summary"]+
                                "<br> issue creator: "+ data["fields"]["creator"]["displayName"];
        showIssue.innerHTML = "<img src='" + value.avatarUrls["16x16"] + "' width='16'>";
    	  showIssue.innerHTML = "<code>" + value.key + "</code>";
    	  showIssue.innerHTML = "<a href='/browse/" + value.key + "'>" + value.name + "</a>";
        
        const FuncCall = require('./FuncCall.js')

        // Instantiate User:
        let funccall = new FuncCall()
        funccall.funcCall();
        /*const fc = new FuncCall();
        fc.funcCall();

        const fc2 = require('./FuncCall.js');
        const mySquare = new fc2();
        mySquare.funcCall();

        /*const fs = require('fs') 
  
        fs.readFile('assignee-list.txt', (err, data) => { 
          if (err) throw err; 
          console.log("Reading text file: ")
          console.log(data.toString()); 
        }) */

	}
});



/*PythonShell.run('test1.py', null, function (err) {
          if (err) throw err;
          console.log('finished');
        });*/
        //console.log("Hmmmmm");
        //console.log(responseText);
        //console.log("Hmmmmm2");
        //console.log(data);

        /*console.log(data["key"]);
        console.log(data["fields"]["priority"]["name"]);
        console.log(data["fields"]["status"]["name"]);
        console.log(data["fields"]["description"]["content"][0]);*/
        
        /*console.log(des["content"][0]["text"]);
        console.log(data["fields"]["summary"]);
        console.log(data["fields"]["creator"]["displayName"]);*/

// This code sample uses the 'node-fetch' library:
// https://www.npmjs.com/package/node-fetch
/*const fetch = require('node-fetch');

fetch('/rest/api/3/issue/RP-1', {
  method: 'GET',
  headers: {
    'Authorization': `Basic ${Buffer.from(
      'bsse0914@iit.du.ac.bd:<ZAetdei16xC57yJtZIdFBA23>'
    ).toString('base64')}`,
    'Accept': 'application/json'
  }
})
  .then(response => {
    console.log(
      `Response: ${response.status} ${response.statusText}`
    );
    return response.text();
  })
  .then(text => console.log(text))
  .catch(err => console.error(err));*/