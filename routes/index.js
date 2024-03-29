export default function routes(app, addon) {

    //const express = require('express')
    //const app = express()

    //app.use(express.urlencoded())

    // Redirect root path to /atlassian-connect.json,
    // which will be served by atlassian-connect-express.

    // This is an example route used by "generalPages" module (see atlassian-connect.json).
    // Verify that the incoming request is authenticated with Atlassian Connect.
    /*app.get('/hello-world', addon.authenticate(), (req, res) => {
        // Rendering a template is easy; the render method takes two params:
        // name of template and a json object to pass the context in.
        res.render('hello-world', {
            title: 'Atlassian Connect'
            //issueId: req.query['issueId']
        });
    });*/

    // Add additional route handlers here...
    app.use((req, res, next) => {
        res.header('Access-Control-Allow-Origin', '*');
        next();
    });

    app.get('/suggestion', addon.authenticate(), function(req, res) {
        const username = req.body.username;
        console.log(username);
        res.render('activity', { title: "Jira Assignee Suggestion" });
       
    });


    /*app.post('/submit-form', (req, res) => {
        const username = req.body.username
        console.log(username);
        //...
        res.end()
    })*/
}
