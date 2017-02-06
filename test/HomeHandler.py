#!/usr/bin/env python
#
# Copyright 2013 @author Subhasis
#
# main Tornado file for testing

from test.BaseHandler import BaseHandler

class HomeHandler(BaseHandler):
    def get(self):
        self.render("home.html")