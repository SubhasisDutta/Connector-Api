import httplib,json
conn = httplib.HTTPConnection("localhost", 8888)
print "Testing with correct token and Active Stream Id - Expected PASS"
token="e19dedf7-d9c4-475d-bd64-77898c5d7dd1"
streamId="1321-1321"
conn.request("GET", "/log?accessToken="+token+"&streamId="+streamId )
r2 = conn.getresponse()
print 'Response Status: '+str(r2.status)
data = r2.read()
if r2.status == 200 :
    print 'Json Message: '+data
    print 'Test Pass'
else:
    print 'Test Fail'
print '====End==='