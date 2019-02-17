const express = require('express');
const request = require('request');
const spawn = require('child_process').spawn;
const bodyParser = require('body-parser');
const fs = require('fs');

var arr = fs.readFileSync('image-links.csv').toString().split(/\n/g);
images = arr.map(i => i.split(/, /g)).map(v => [v[0].split(' ')[1], v[1]]);
image_dict = {};
for (let x of images)
    image_dict[x[0]] = x[1];

var keys = JSON.parse(fs.readFileSync('api-keys.json', 'utf8'));

//App setup
var app = express();

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: true}));

var server = app.listen(4000, function () {
    console.log('listening to requests on port 4000');
});

app.use(express.static(__dirname + '/public'));

app.get('/congress/', function(req, res) {
    let result = image_dict[req.query.name];
    console.log(result);
    res.send({name: req.query.name, url: result});
});

app.post('/knn/', function(req, res) {
    console.log(req.body);
    args = ['knn_get.py'];
    for (let i of req.body.vector) {
        args.push(i);
    }
    proc = spawn('python', args, {cwd: 'pyscripts'});
    proc.stdout.on('data', names => {
        names = names.toString();
        output = {};
        for (let name of names.split(/\n/g)) {
            if (name) {
                let url = image_dict[name.split(/ /g)[0].toLowerCase()];
                output[name] = url ? url : 'congress.png';
            }
        }
        console.log(output);
        res.send(output);
    });
});

app.post('/leg-api', function (req, res) {

    var output = {};

    console.log(req.body);

    var rootURL = "https://q4ktfaysw3.execute-api.us-east-1.amazonaws.com/treehacks/legislators?address="
    rootURL += req.body.street;
    rootURL += "," + req.body.city;
    rootURL += "," + req.body.state;
    rootURL += "+" + req.body.zip;
    var finalURL = rootURL + "&level=NATIONAL_UPPER"	//senate

    console.log(finalURL);

    var api_query = {
        url: finalURL,
        headers: {
            'x-api-key': keys["legislator-lookup-key"]
        }
    };

    request(api_query, function (error, response, body) {
        if (!error && response.statusCode == 200) {
            const data = JSON.parse(body);
            output['senate'] = data;

            finalURL = rootURL + "&level=NATIONAL_LOWER"	//house

            console.log(finalURL);

            var api_query = {
                url: finalURL,
                headers: {
                    'x-api-key': keys["legislator-lookup-key"]
                }
            };

            request(api_query, function (error, response, body) {
                if (!error && response.statusCode == 200) {
                    const data = JSON.parse(body);
                    output['house'] = data;

                    res.send(output);
                }
            });
        }
    });

});
