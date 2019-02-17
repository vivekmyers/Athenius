# Athenius

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
