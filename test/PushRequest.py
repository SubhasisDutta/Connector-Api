#!/usr/bin/env python
#
# Copyright 2013 @author Subhasis
#
# main Tornado file for testing

import httplib

from test.BaseHandler import BaseHandler
from tornado.options import options

class PushRequest(BaseHandler):
    def post(self):
        request = self.request        
        bodyString=str(request.body)
        conn = httplib.HTTPConnection(options.server, options.serverport)
        headers = { "Content-type": "application/json",                   
                   "Content-Length": "%d" % len(bodyString)}
        conn.request("POST", "/push", bodyString, headers)
        r2 = conn.getresponse()
        self.write(r2.read())