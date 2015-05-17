var express = require('express');
var app = express();
var lines = require('../Scripts/lines.json');
var linesKeys = Object.keys(lines);
console.log(linesKeys)

app.get('/question/beginning', function(req, res) {
    var line = linesKeys[Math.floor(Math.random() * linesKeys.length)];
    console.log(line)
    var directions = lines[line];
    var station = Object.keys(directions)[0];
    var question = {};
    console.log(station) 
    question["question"] = "Czy " + line + ' zaczyna kurs od przystanku "' + directions[station][0][1] + '"?';
    question["answer"]   = "1"
    
    res.json({"result": question});
});

app.listen(process.env.PORT || 3412);
