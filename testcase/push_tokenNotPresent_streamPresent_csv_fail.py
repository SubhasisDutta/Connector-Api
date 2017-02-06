import httplib,json,os
conn = httplib.HTTPConnection("localhost", 8888)
print "Testing Push invalid token- Expected FAIL"
token="fdgfdgfd-5v63536bb563v3vb34gv43-v43y57565ghgfh6546b"
streamId="1321-1321"
package_directory = os.path.dirname(os.path.abspath(__file__))
localPath= os.path.join(package_directory, 'data', 'LebronJames_sample_docs.csv')
with open (localPath, "r") as myfile:
    data=myfile.read()
headers = { "Content-type": "text/csv", "Host:" : "localhost", "Content-Length": "%d" % len(data)}
conn.request("POST", "/push?accessToken="+token+"&streamId="+streamId, data, headers)
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