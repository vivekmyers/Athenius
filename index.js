const express = require('express');
const request = require('request');
var bodyParser = require('body-parser');
const fs = require('fs');

var keys = JSON.parse(fs.readFileSync('api-keys.json', 'utf8'));

//App setup
var app = express();

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: true}));

var server = app.listen(4000,function(){
	console.log('listening to requests on port 4000');
});

app.use(express.static(__dirname +'/public'));

app.post('/leg-api', function(req, res){

	var output = {};

	console.log(req.body);

	var rootURL = "https://q4ktfaysw3.execute-api.us-east-1.amazonaws.com/treehacks/legislators?address="
	rootURL += "," + req.body.city;
	rootURL += "," + req.body.state;
	rootURL += "+" + req.body.zip; 
	var finalURL = rootURL + "&level=NATIONAL_UPPER"	//senate

	console.log(finalURL);

	var api_query = {
		url: finalURL,
		headers:{
			'x-api-key': keys["legislator-lookup-key"]
		}
	};

	request(api_query, function(error, response, body){
		if(!error && response.statusCode == 200){
			const data = JSON.parse(body);
			output['senate'] = data;

			finalURL = rootURL + "&level=NATIONAL_LOWER"	//house

			console.log(finalURL);

			var api_query = {
				url: finalURL,
				headers:{
					'x-api-key': keys["legislator-lookup-key"]
				}
			};

			request(api_query, function(error, response, body){
				if(!error && response.statusCode == 200){
					const data = JSON.parse(body);
					output['house'] = data;

					res.send(output);
				}
			});
		}
	});

});