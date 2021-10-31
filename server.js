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
  res.redirect("/main");
});

app.get("/main", function(req,res){
  res.sendFile(path.join(__dirname, "./views/main.html"));
});

// ---------------------------------------------------

app.get("/howto", function(req,res){
  res.sendFile(path.join(__dirname, "./views/howto.html"));
});

// ---------------------------------------------------

app.get("/exercise", function(req,res){
  res.sendFile(path.join(__dirname, "./views/exercise.html"));
});

app.get("/school", function(req,res){
  res.sendFile(path.join(__dirname, "./views/school.html"));
});

app.get("/restaurant", function(req,res){
  res.sendFile(path.join(__dirname, "./views/restaurant.html"));
});
app.get("/greetings", function(req,res){
  res.sendFile(path.join(__dirname, "./views/greetings.html"));
});

app.get("/travel", function(req,res){
  res.sendFile(path.join(__dirname, "./views/travel.html"));
});

app.get("/hospital", function(req,res){
  res.sendFile(path.join(__dirname, "./views/hospital.html"));
});

app.get("/shopping", function(req,res){
  res.sendFile(path.join(__dirname, "./views/shopping.html"));
});
// ---------------------------------------------------
app.get("/practice", function(req,res){
  res.sendFile(path.join(__dirname, "./views/practice.html"));
});

// ---------------------------------------------------
app.get("/tonguetwister", function(req,res){
  res.sendFile(path.join(__dirname, "./views/tonguetwister.html"));
});

// ---------------------------------------------------
app.get("/colloquial", function(req,res){
  res.sendFile(path.join(__dirname, "./views/colloquial.html"));
});

// ---------------------------------------------------
// setup http server to listen on HTTP_PORT
app.listen(HTTP_PORT, onHttpStart);


// bootstrap template
// https://themewagon.com/themes/free-bootstrap-4-html5-admin-dashboard-template-plus-admin/