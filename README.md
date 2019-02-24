# Atheni.us

Rohan Deshpande, Vinjai Vale, Vivek Myers, Nikhil Sardana for TreeHacks 2019

## Description

Athenius (www.atheni.us) is a novel solution applying data science techniques to address some of the greatest inefficiencies plaguing modern politics: uninformed voters and poor turnouts.  Most voters, let alone most citizens, are not aware of the inner workings of Congress.  In particular, it is difficult to keep tabs on the very representatives that one votes to office.  Bills are complicated, and we cannot expect everyday citizens to personally evaluate how their representatives vote on each bill.  So how can voters evaluate how well they are *truly* being represented in Congress?

To the best of our knowledge, Athenius is the first modern technology to address this question, making national politics accessible and easy-to-follow for all citizens.  We use unsupervised clustering and dimensionality reduction algorithms to understand the key issues being addressed in recent Congress bills, 

## Features

* Quick 16 question questionaire on 'Represent Me' determines users political views
* User's political views are matched to three legislators with most similar views
* User can find his/her legislators based on input location (using Legislator Lookup API)
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
```

## Development challenges

It turns out that the underlying analytics problem here was a lot more nontrivial than we originally thought.  In particular, k-Means is not perfect.
