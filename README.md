# Atheni.us

## Description

## Features

* Quick 16 question questionaire on 'Represent Me' determines users political views
* User's political views are matched to three legislators with most similar views
* User can find his/her legislators based on input location
* User can compare his/her political views to their legislator's views
* Email subscription service to send user notification when legislator votes on bill in a way that user doesn't agree with

### Use source code (run locally):

Make sure you have NodeJS, NPM, and python3 installed. The Web-app will use the Legislator Lookup API to get find legislators based on a location. In order to use this API you must have an API key. In the 'TreeHacks2019' folder add a file titled 'api-keys.json'. Add the following to this file, replacing "X" with the private key:

```
    {
        "legislator-lookup-key" : "XXXXXXXXXXXXXXXXXXXXX"
    }
```


```console
$ git clone https://github.com/vivekmyers/Treehacks2019.git
$ npm install
```

To run the NodeJS webapp:
```console
$ sudo npm start 				# starts web-server on port 80
OR:
$ npm test						# starts web-server on port 4000
