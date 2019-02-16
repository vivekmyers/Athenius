const express = require('express');
const request = require('request');
const fs = require('fs');

var keys = JSON.parse(fs.readFileSync('api-keys.json', 'utf8'));

//App setup
var app = express();
var server = app.listen(4000,function(){
	console.log('listening to requests on port 4000');
});

app.use(express.static(__dirname +'/public'));

app.get('/leg-api', function(req, res){

	var api_query = {
		url: "https://q4ktfaysw3.execute-api.us-east-1.amazonaws.com/treehacks/legislators?address=450+Serra+Mall,+Stanford,+CA+94305&level=NATIONAL_LOWER",
		headers:{
			'x-api-key': keys["legislator-lookup-key"]
		}
	};

	request(api_query, function(error, response, body){
		if(!error && response.statusCode == 200){
			const data = JSON.parse(body);
			//console.log(data);
			res.send(data);
		}
	});
});