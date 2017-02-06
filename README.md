#Introduction

This project is implemented using Python Tornado. The objective of this project was to enable ingression of data from different sources using a Push API and Log all access requests into Couch DB.
###Start Server:
1.	Initiate Couch DB and make sure it is working.
2.	Go to the folder in which the Connector API code is present and start the server by 
$ python main.ph
This will start the server in port 8888.
3.	Check the server status by curl or in browser by http://localhost:8888
4.	The response should be a JSON
{“Status”:”Server Running”, “ConnectorAPI”:”Welcome”}

###PUSH API:
The Push API can ingest CSV, XML and JSON data and convert it to standard JSON data and store it in datastore. Before ingesting the data the request is authenticated with two access codes(access token and provider Id) and only after authentication the data is ingested into the system.

###LOG API: 
The log API currently returns the recent 25 push for a provider after authentication of access token and provider id.

The details of the api are in the document BMDataConnectorAPI.docx.  

#Test Data:

All test data are present in test case folder. Once the tornado server is running, to execute the test cases simply execute the python test files.

##Dependencies:

Install Tornado
pip install tornado

Install Couch Db
sudo apt-get install couchdb
Or
Python CouchDB
$ wget http://peak.telecommunity.com/dist/ez_setup.py
$ sudo python ez_setup.py
$ wget http://pypi.python.org/packages/2.6/C/CouchDB/CouchDB-0.8-py2.6.egg
$ sudo easy_install CouchDB-0.8-py2.6.egg

Install curl if not present
sudo apt-get install curl

check if Couch db working properly
curl localhost:5984
Response:
{"couchdb":"Welcome","version":"1.0.1"}

Create a new database for connectorAPI
curl -X PUT localhost:5984/connectorapi
Response:{"ok":true}

Access Couchdb UI
http://localhost:5984/_utils/

#Modules:

1. Config - 
   masterConfig.cnf - This is a key value property that contains all the user defined messages required for the project.
2. BaseHandler – This is the Common module for all the other modules. That takes care of common functionality like connection to data store.
3. CreateToken – This is to enable the administrator to create vaild access tokens to be used to push data.
4. HomeHandler – Just a welcome module. To verify is server is running.
5. LogModule – Enables the provider to access the latest 25 push request meta data.
6. PushModule – Enables the user to push XML, CSV and JSON into the data store where it is stored in standard JSON.
7. ValidateToken – used to validate a request before responding to a push or get request.
