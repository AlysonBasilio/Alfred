var http = require('http');
var fs = require('fs');
var url = require('url');

http.createServer(function (req, res) {
  var q = url.parse(req.url, true);
  console.log(q['path']);
  if(q['path']=='/unnamed.png'){
    fs.readFile('unnamed.png', function(err, data) {
      res.writeHead(200, {'Content-Type': 'img/html'});
      res.write(data);
      res.end();
    });
  } else if (q['path']=='/Numbers.txt') {
      var obj;
      obj = fs.readFileSync('Numbers.txt', 'utf8');
      console.log(obj);
      res.writeHead(200, {'Content-Type': 'text/html'});
      res.write(obj);
      res.end();
  } else{
    fs.readFile('index.html', function(err, data) {
      res.writeHead(200, {'Content-Type': 'text/html'});
      res.write(data);
      res.end();
    });
  }
}).listen(8080);
