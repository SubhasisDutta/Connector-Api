#!/usr/bin/env python
#
# Copyright 2013 @author Subhasis
#
# main Tornado file for testing

import httplib
import os.path

from test.BaseHandler import BaseHandler
from tornado.options import options

class PushJson(BaseHandler):
    def get(self):
        streamId=self.get_argument("streamId")
        accessToken=self.get_argument("accessToken")
        conn = httplib.HTTPConnection(options.server, options.serverport)  
        package_directory = os.path.dirname(os.path.abspath(__file__))
        localPath= os.path.join(package_directory, 'data', 'sample_json_100_docs.txt')
        with open (localPath, "r") as myfile:
            data=myfile.read().replace('"streamId":""', '"streamId":"'+streamId+'"').replace('"accessToken":""','"accessToken":"'+accessToken+'"')        
        headers = { "Content-type": "application/json",                   
                   "Content-Length": "%d" % len(data)}
        conn.request("POST", "/push", data, headers)
        r2 = conn.getresponse()
        self.write(r2.read())
#         self.write(data)