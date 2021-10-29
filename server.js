var HTTP_PORT = process.env.PORT || 8080;
var express = require("express");
var path = require("path");
var app = express();

function onHttpStart() {
    console.log("Express http server listening on " + HTTP_PORT);
  }

app.use(express.static("./assets/"));

// setup a 'route' to listen on the default url path
app.get("/", function(req,res){
    res.sendFile(path.join(__dirname, "./views/main.html"));
});

app.get("/howto", function(req,res){
  res.sendFile(path.join(__dirname, "./views/howto.html"));
});


// setup http server to listen on HTTP_PORT
app.listen(HTTP_PORT, onHttpStart);


// bootstrap template
// https://themewagon.com/themes/free-bootstrap-4-html5-admin-dashboard-template-plus-admin/