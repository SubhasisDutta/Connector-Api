#!/usr/bin/env python
#
# Copyright 2014 @author Subhasis

import tornado.web
import couchdb

from tornado.options import options

class BaseHandler(tornado.web.RequestHandler):
    @property
    def dbserver(self):
        return couchdb.client.Server(options.couch_host)  