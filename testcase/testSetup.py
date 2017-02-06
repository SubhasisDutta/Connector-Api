import couchdb,os,json
import httplib
couch = couchdb.Server('http://localhost:5984/')
#delete all test databases
try:
    couch.delete('api_logs')
except:
    pass
try:
    couch.delete('api_tokens')
except:
    pass
try:
    couch.delete('z_1321-1321_api_docs')
except:
    pass
try:
    couch.delete('z_333-333_api_docs')
except:
    pass
print 'Drop old database'
#create and upload api_tokens
db = couch.create('api_tokens')
package_directory = os.path.dirname(os.path.abspath(__file__))
localPath= os.path.join(package_directory, 'data', 'api_tokens_testdata.json')
with open (localPath, "r") as myfile:
    data=myfile.read()
db.save(json.loads(data))
print 'api_tokens created'
print 'Sarting Test....'
