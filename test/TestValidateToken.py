#!/usr/bin/env python
#
# Copyright 2013 @author Subhasis
#
# main Tornado file for testing

import httplib

from test.BaseHandler import BaseHandler
from tornado.options import options

class TestValidateToken(BaseHandler):
    def get(self):
        streamId=self.get_argument("streamId")
        accessToken=self.get_argument("accessToken")        
        conn = httplib.HTTPConnection(options.server, options.serverport)             
        headers = { "Content-type": "application/json",                   
                   }
        data=""
        params="?streamId="+streamId+"&accessToken="+accessToken
        conn.request("GET", "/validateToken"+params,data, headers)
        r2 = conn.getresponse()
        self.write(r2.read())