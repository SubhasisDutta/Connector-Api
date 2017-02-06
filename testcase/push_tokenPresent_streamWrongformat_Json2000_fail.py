import httplib,json,os
conn = httplib.HTTPConnection("localhost", 8888)
print "Testing Push with stream ID wrong format- Expected FAIL"
token="e19dedf7-d9c4-475d-bd64-77898c5d7dd1"
streamId="45jhjjkkjjjun"
package_directory = os.path.dirname(os.path.abspath(__file__))
localPath= os.path.join(package_directory, 'data', 'sample_json_2000_docs.json')
with open (localPath, "r") as myfile:
    data=myfile.read().replace('"streamId":""', '"streamId":"'+streamId+'"').replace('"accessToken":""','"accessToken":"'+token+'"')
headers = { "Content-type": "application/json", "Host:" : "localhost", "Content-Length": "%d" % len(data)}
conn.request("POST", "/push", data, headers)
r2 = conn.getresponse()
print 'Response Status: '+str(r2.status)
data = r2.read()
j=json.loads(data)
if r2.status == 200 and j['state']== 'Invalid Request':
    print 'Json Message: '+j['state']
    print 'Test Pass'
else:
    print 'Test Fail'
print '====End==='