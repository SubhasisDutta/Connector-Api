#!/usr/bin/env python
#
# Copyright 2014 @author Subhasis

import os.path
import re
import couchdb
import ConfigParser

from tornado.options import options
from tornado.escape import json_encode

from src.BaseHandler import BaseHandler

class ValidateToken(BaseHandler):    
    config = ConfigParser.ConfigParser()
    def get(self):        
        configPath=os.path.dirname(os.path.realpath(__file__))+'/../config/masterConfig.cnf'
        self.config.read(configPath)
        streamId=self.get_argument(self.config.get('AccessParameters', 'Access.Identifier'))
        accessToken=self.get_argument(self.config.get('AccessParameters', 'Access.Token'))
        self.set_header("Content-Type", "application/json")
        validate=validateStreamToken()
        return self.write(json_encode(validate.validate(streamId,accessToken)))

class validateStreamToken(BaseHandler):
    config = ConfigParser.ConfigParser()
    def __init__(self):
        configPath=os.path.dirname(os.path.realpath(__file__))+'/../config/masterConfig.cnf'
        self.config.read(configPath)
      
    def validate(self,streamId,token):
        msgObj={}
        matchObj = re.match(self.config.get('IdentifierFormat', 'Identifier.Format'), streamId)        
        if matchObj is None:
            msgObj["status"]=self.config.get('GeneralMsg', 'Status.fail')
            msgObj["message"]=self.config.get('ErrorMsg', 'Identifier.InvalidFormat')
            return msgObj
        try:            
            db = self.dbserver[options.api_tokens_database]
        except :            
            couch = couchdb.Server(options.couch_host)
            db = couch.create(options.api_tokens_database)
        viewPath=os.path.dirname(os.path.realpath(__file__))+'/../scripts/checkAPIToken.js'
        with open (viewPath, "r") as myfile:
            map_all=myfile.read().replace('~accessToken~', token)      
        records=db.query(map_all)
        a=[]
        for r in records:
            a.append(r)        
        if len(a) == 0:
            msgObj["status"]=self.config.get('GeneralMsg', 'Status.fail')
            msgObj["message"]=self.config.get('ErrorMsg', 'Token.Invalid')            
        else:            
            for row in records:                
                for stream in row.value["streams"]:
                    if stream[self.config.get('AccessParameters', 'Access.Identifier')]==streamId and stream["status"]==self.config.get('GeneralMsg', 'Identifier.Active'):
                        msgObj["status"]=self.config.get('GeneralMsg', 'Status.success')
                        msgObj["message"]=self.config.get('GeneralMsg', 'Valid.Token.Identifier')
                        break
                    msgObj["status"]=self.config.get('GeneralMsg', 'Status.fail')
                    msgObj["message"]=self.config.get('ErrorMsg', 'Invalid.Token.Identifier')
        return msgObj
                