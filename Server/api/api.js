var https          = require('https'),
    express        = require('express');

var router = express.Router();
var lines = require('../scripts/lines.json');
var linesKeys = Object.keys(lines);
console.log(linesKeys)

router.get('/question/beginning', function(req, res) {
    var line = linesKeys[Math.floor(Math.random() * linesKeys.length)];
    var directions = lines[line];
    var station = Object.keys(directions)[0];
    var question = {};
    console.log(station)
    question["question"] = "Czy " + line + ' zaczyna kurs od przystanku "' + directions[station][0][1] + '"?';
    question["answer"]   = "1"
    res.send({"result": question});
});

router.post('/auth', function (req, res){
    var access_token = String(req.body.access_token)

    var options = {
        host: 'graph.facebook.com',
        port: 443,
        path: '/me' + '?access_token=' + access_token,
        method: 'GET'
    };
    var buffer = '';
    https.get(options, function(result){
        result.setEncoding('utf8');
        result.on('data', function(chunk){
            buffer += chunk;
        });

        result.on('end', function(){
            console.log(buffer);
            res.send({"id": JSON.parse(buffer)['id'], "access_token": access_token});
        });
    });

});


module.exports = router;