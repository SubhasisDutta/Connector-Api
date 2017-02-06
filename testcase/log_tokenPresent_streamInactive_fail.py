import httplib,json
conn = httplib.HTTPConnection("localhost", 8888)
print "Testing with correct token and Inactive Stream Id - Expected FAIL"
token="e19dedf7-d9c4-475d-bd64-77898c5d7dd1"
streamId="444-444"
conn.request("GET", "/log?accessToken="+token+"&streamId="+streamId )
r2 = conn.getresponse()
print 'Response Status: '+str(r2.status)
data = r2.read()
j=json.loads(data)
if r2.status == 200 and j['message']== 'Stream ID is InValid or is INACTIVE.':
    print 'Json Message: '+j['message']
    print 'Test Pass'
else:
    print 'Test Fail'
print '====End==='