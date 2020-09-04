AP.request('GET /rest/api/2/search?jql=project="Juicy Island"', {
	success: function(responseText){
        console.log("hbe na re vai");
        var data = JSON.stringify(responseText);
        console.log(data);

        'use strict';

        const fs = require('fs');
 
        fs.writeFileSync('juicy-island-issues.json', data);
	}
});