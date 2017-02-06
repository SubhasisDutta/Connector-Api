#!/usr/bin/env python
#
# Copyright 2013 @author Subhasis
#
# main Tornado file for starting server

import os.path
import ConfigParser
import logging

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options

from src.HomeHandler import HomeHandler
from src.PushModule import PushModule
from src.LogModule import LogModule

config = ConfigParser.ConfigParser()
configPath=os.path.dirname(os.path.realpath(__file__))+'/config/masterConfig.cnf'
config.read(configPath)

logger= logging.getLogger('log.application')
hdlr = logging.FileHandler(config.get('Logging', 'Logger.File'))
formatter = logging.Formatter('[%(levelname)s %(asctime)s -- %(module)s:%(lineno)d] %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging._levelNames[config.get('Logging', 'Logger.Level')])


define("port", default=config.get('ServerConnection', 'Server.Port'), help="run on the given port", type=int)

define("couch_host", default=config.get('CouchDBConnection', 'Couch.ServerURL'), help="ConnectoAPI CouchDB database host")
define("api_tokens_database", default=config.get('CouchDBConnection', 'Couch.TokenStreamDatabase'), help="API Tokens database name")
define("couch_docs_database", default=config.get('CouchDBConnection', 'Couch.DocumentDatabaseNameFormat'), help="Documents database name")
define("couch_logs_database", default=config.get('CouchDBConnection', 'Couch.LogsDatabase'), help="Logs database name")
define("getLogs_limit", default=config.get('ServerConnection', 'GetLogs.Limit'), help="Latest Logs Limit")

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", HomeHandler),
            (r"/"+config.get('ServerConnection', 'Webservice.Push'), PushModule),
            (r"/"+config.get('ServerConnection', 'Webservice.Log'), LogModule),
#             (r"/"+config.get('ServerConnection', 'Webservice.CreateToken'), CreateToken),
#             (r"/"+config.get('ServerConnection', 'Webservice.ValidateToken'), ValidateToken),
        ]
        logger.info('Handlers Set.')
        settings = dict(
            app_title=u""+config.get('ServerConnection', 'WebApp.title'),
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=False,    
            debug=config.get('ServerConnection', 'Server.Debug'),
        )
        logger.info('Settings Variables Set.')
        tornado.web.Application.__init__(self, handlers, **settings)

def main():
    logger.info('Starting Server ....')
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    logger.info('Server Started.')
    tornado.ioloop.IOLoop.instance().start()
    

if __name__ == "__main__":
    main()