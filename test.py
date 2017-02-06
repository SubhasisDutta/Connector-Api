#!/usr/bin/env python
#
# Copyright 2013 @author Subhasis
#
# main Tornado file for testing

import tornado.httpserver
import tornado.ioloop
import tornado.web

import os.path

from tornado.options import define, options

from test.HomeHandler import HomeHandler
from test.PushRequest import PushRequest
from test.PushJson import PushJson
from test.PushJson1 import PushJson1
from test.TestCreateToken import TestCreateToken
from test.TestValidateToken import TestValidateToken


define("port", default=9999, help="run on the given port", type=int)
define("server", default="localhost", help="server Domain Name", type=int)
define("serverport", default=8888, help="server Port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", HomeHandler),
            (r"/push", PushRequest),
            (r"/push100", PushJson),
            (r"/push1000", PushJson1),
            (r"/createToken",TestCreateToken),
            (r"/validateToken",TestValidateToken),
        ]
        settings = dict(
            app_title=u"Connector API Test",
            template_path=os.path.join(os.path.dirname(__file__), "test/templates"),
            static_path=os.path.join(os.path.dirname(__file__), "test/static"),
            xsrf_cookies=False,
            cookie_secret="__dsds:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",          
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
