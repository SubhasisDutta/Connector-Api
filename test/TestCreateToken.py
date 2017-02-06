#!/usr/bin/env python
#
# Copyright 2013 @author Subhasis
#
# main Tornado file for testing

import httplib

from test.BaseHandler import BaseHandler
from tornado.options import options

class TestCreateToken(BaseHandler):
    def get(self):
        streamId=self.get_argument("streamId")
        accessToken=self.get_argument("accessToken")
        status=self.get_argument("status")
        conn = httplib.HTTPConnection(options.server, options.serverport)             
        headers = { "Content-type": "application/json",                   
                   }
        data=""
        params="?streamId="+streamId+"&accessToken="+accessToken+"&status="+status
        conn.request("POST", "/createToken"+params,data, headers)
        r2 = conn.getresponse()
        self.write(r2.read())