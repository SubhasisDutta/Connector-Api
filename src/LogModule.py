#!/usr/bin/env python
#
# Copyright 2014 @author Subhasis

import os.path
import couchdb
import ConfigParser

import logging

from tornado.options import options
from tornado.escape import json_encode

from src.BaseHandler import BaseHandler
from src.ValidateToken import validateStreamToken

logger= logging.getLogger('log.application')

class LogModule(BaseHandler):
    config = ConfigParser.ConfigParser()    
    def get(self):          
        configPath=os.path.dirname(os.path.realpath(__file__))+'/../config/masterConfig.cnf'
        self.config.read(configPath)
        logger.info(self.config.get('Logging', 'Logger.GetMessage1')+''+self.request.remote_ip)
        streamId=self.get_argument(self.config.get('AccessParameters', 'Access.Identifier'))
        token=self.get_argument(self.config.get('AccessParameters', 'Access.Token'))
        checkToken=validateStreamToken()
        validationResult=checkToken.validate(streamId, token)
        if validationResult["status"]==self.config.get('GeneralMsg', 'Status.success'):
            try:
                db = self.dbserver[options.couch_logs_database]
            except :  
                logger.info(self.config.get('Logging', 'Logger.GetMessage2'))          
                couch = couchdb.Server(options.couch_host)
                db = couch.create(options.couch_logs_database)
            viewPath=os.path.dirname(os.path.realpath(__file__))+'/../scripts/logGetQuery.js'
            with open (viewPath, "r") as myfile:
                map_all=myfile.read().replace('~accessToken~', token).replace('~streamId~',streamId)
            msg_all = []
            for row in db.query(map_all,descending=True,limit=options.getLogs_limit):
                msg_all.append(row.value)       
            self.write(json_encode(msg_all))
            logger.info(self.config.get('Logging', 'Logger.GetMessage3')+''+streamId+' '+token)
        else:
            self.write(json_encode(validationResult))
            logger.error(self.config.get('Logging', 'Logger.GetMessage4')+''+streamId+' '+token)
        self.set_header("Content-Type", "application/json")