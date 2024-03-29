// Entry point for the app

// Express is the underlying that atlassian-connect-express uses:
// https://expressjs.com
import express from 'express';
//import cors from 'cors';
// https://expressjs.com/en/guide/using-middleware.html
import bodyParser from 'body-parser'; //Parse HTTP request body. third-party middleware
import compression from 'compression'; //Compress HTTP responses. third-party middleware
import cookieParser from 'cookie-parser'; //Parse cookie header and populate req.cookies. third-party middleware
import errorHandler from 'errorhandler'; //Development error-handling/debugging. third-party middleware
import morgan from 'morgan'; //HTTP request logger. third-party middleware

// atlassian-connect-express also provides a middleware
import ace from 'atlassian-connect-express';
//import {PythonShell} from 'python-shell';


// Use Handlebars as view engine:
// https://npmjs.org/package/express-hbs
// http://handlebarsjs.com
import hbs from 'express-hbs';

// We also need a few stock Node modules
import http from 'http';
import path from 'path';
import os from 'os';
import helmet from 'helmet';
// Routes live here; this is the C in MVC
import routes from './routes';
//var cors_proxy = require('cors-anywhere');
// Bootstrap Express and atlassian-connect-express
const app = express();
//app.use(cors())

//app.use(cors());
const addon = ace(app);

// See config.json
const port = addon.config.port();

//if (port == null || port == "") {  port = 8000;
//}
app.set('port', port);

// Configure Handlebars
const viewsDir = __dirname + '/views';
app.engine('hbs', hbs.express4({partialsDir: viewsDir}));
app.set('view engine', 'hbs'); ////Sets our app to use the handlebars engine.  Handlebars takes a static template file you give it .
app.set('views', viewsDir);

// Log requests, using an appropriate formatter by env
const devEnv = app.get('env') == 'development';
app.use(morgan(devEnv ? 'dev' : 'combined'));

// Atlassian security policy requirements
// http://go.atlassian.com/security-requirements-for-cloud-apps
// HSTS must be enabled with a minimum age of at least one year
app.use(helmet.hsts({
  maxAge: 31536000,
  includeSubDomains: false
}));
app.use(helmet.referrerPolicy({
  policy: ['origin-when-cross-origin']
  //policy: ['no-referrer']
}));

// Include request parsers
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: false}));
app.use(cookieParser());

// Gzip responses when appropriate
app.use(compression());

// Include atlassian-connect-express middleware
app.use(addon.middleware());

// Mount the static files directory
const staticDir = path.join(__dirname, 'public');
app.use(express.static(staticDir));

// Atlassian security policy requirements
// http://go.atlassian.com/security-requirements-for-cloud-apps
app.use(helmet.noCache());

// Show nicer errors in dev mode
if (devEnv) app.use(errorHandler());

// Wire up routes
routes(app, addon);

function myFunc(vars) {
  return vars
}

// Boot the HTTP server
http.createServer(app).listen(port, () => {
  console.log('App server running at http://' + os.hostname() + ':' + port);

  // Enables auto registration/de-registration of app into a host in dev mode
  //what happens in prod mode?
  if (devEnv) addon.register();
});





