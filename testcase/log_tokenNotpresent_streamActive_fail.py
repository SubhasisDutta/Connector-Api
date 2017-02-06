import httplib,json
conn = httplib.HTTPConnection("localhost", 8888)
print "Testing with incorrect token - Expected FAIL"
token="qwertyujm-32ddfd-dfdfm-fgfvv"
streamId="1321-1321"
conn.request("GET", "/log?accessToken="+token+"&streamId="+streamId )
r2 = conn.getresponse()
print 'Response Status: '+str(r2.status)
data = r2.read()
j=json.loads(data)
if r2.status == 200 and j['message']== 'Invalid Token.':
    print 'Json Message: '+j['message']
    print 'Test Pass'
else:
    print 'Test Fail'
print '====End==='