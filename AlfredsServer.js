var http = require('http');
var fs = require('fs');
var url = require('url');
var mysql = require('mysql');

var con = mysql.createConnection({
  host: "localhost",
  user: "root",
  password: "123456"
});
con.connect(function(err) {
  if (err) throw err;
  console.log("Connected!");
});

http.createServer(function (req, res) {
  var q = url.parse(req.url, true);
  console.log(q);
  if(q['path']=='/unnamed.png'){
    fs.readFile('unnamed.png', function(err, data) {
      res.writeHead(200, {'Content-Type': 'img/html'});
      res.write(data);
      res.end();
    });
  } else if (q['path']=='/index.html') {
      var obj = "{";
      con.query("select count(day_of_week) from alfredsDb.user_activities where day_of_week='MON'",
      function (err, result, fields) {
        if (err) throw err;
        console.log(result[0]['count(day_of_week)']);
        obj = obj +"\"MON\":"+ result[0]['count(day_of_week)']+",\n";
        con.query("select count(day_of_week) from alfredsDb.user_activities where day_of_week='TUE'",
        function (err, result, fields) {
          if (err) throw err;
          console.log(result[0]['count(day_of_week)']);
          obj = obj +"\"TUE\":"+ result[0]['count(day_of_week)']+",\n";
          con.query("select count(day_of_week) from alfredsDb.user_activities where day_of_week='WED'",
          function (err, result, fields) {
            if (err) throw err;
            console.log(result[0]['count(day_of_week)']);
            obj = obj +"\"WED\":"+ result[0]['count(day_of_week)']+",\n";
            con.query("select count(day_of_week) from alfredsDb.user_activities where day_of_week='THU'",
            function (err, result, fields) {
              if (err) throw err;
              console.log(result[0]['count(day_of_week)']);
              obj = obj +"\"THU\":"+ result[0]['count(day_of_week)']+",\n";
              con.query("select count(day_of_week) from alfredsDb.user_activities where day_of_week='FRI'",
              function (err, result, fields) {
                if (err) throw err;
                console.log(result[0]['count(day_of_week)']);
                obj = obj +"\"FRI\":"+ result[0]['count(day_of_week)']+",\n";
                con.query("select count(day_of_week) from alfredsDb.user_activities where day_of_week='SAT'",
                function (err, result, fields) {
                  if (err) throw err;
                  console.log(result[0]['count(day_of_week)']);
                  obj = obj +"\"SAT\":"+ result[0]['count(day_of_week)']+",\n";
                  con.query("select count(day_of_week) from alfredsDb.user_activities where day_of_week='SUN'",
                  function (err, result, fields) {
                    if (err) throw err;
                    console.log(result[0]['count(day_of_week)']);
                    obj = obj +"\"SUN\":"+ result[0]['count(day_of_week)']+"\n}";
                    res.writeHead(200, {'Content-Type': 'text/html'});
                    res.write(obj);
                    res.end();
                  });
                });
              });
            });
          });
        });
      });
  } else if (q['pathname']=='/Activities'){
    var obj;
    con.query("select * from alfredsDb.user_activities where day_of_week='"+q['query']['t']+"' order by hour",
      function (err, result, fields) {
        if (err) throw err;
        obj = JSON.stringify(result);
        console.log(obj);
        res.writeHead(200, {'Content-Type': 'text/html'});
        res.write(obj);
        res.end();
    });
  } else if (q['pathname']=='/Insert'){
    console.log(q['query']['t']);
    con.query("INSERT INTO alfredsDb.user_activities (description, tag, priority, day_of_week, hour) VALUES ('"+
    q['query']['desc']+"', '"+q['query']['t']+"', '"+q['query']['p']+"', '"+q['query']['d']+"', '"+q['query']['h']+"')",
      function (err, result, fields) {
        if (err) throw err;
        obj = JSON.stringify(result);
        console.log(obj);
        res.writeHead(200, {'Content-Type': 'text/html'});
        res.write(obj);
        res.end();
    });
  } else{
    fs.readFile('index.html', function(err, data) {
      res.writeHead(200, {'Content-Type': 'text/html'});
      res.write(data);
      res.end();
    });
  }
}).listen(8080);
