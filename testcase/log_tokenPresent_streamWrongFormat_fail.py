import httplib,json
conn = httplib.HTTPConnection("localhost", 8888)
print "Testing with correct token and Invalid Fomat Stream Id - Expected FAIL"
token="e19dedf7-d9c4-475d-bd64-77898c5d7dd1"
streamId="d56567dfdf-ddf343"
conn.request("GET", "/log?accessToken="+token+"&streamId="+streamId )
r2 = conn.getresponse()
print 'Response Status: '+str(r2.status)
data = r2.read()
j=json.loads(data)
if r2.status == 200 and j['message']== 'Invalid Stream ID Format.':
    print 'Json Message: '+j['message']
    print 'Test Pass'
else:
    print 'Test Fail'
print '====End==='