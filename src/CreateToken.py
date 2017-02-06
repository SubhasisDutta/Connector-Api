#!/usr/bin/env python
#
# Copyright 2014 @author Subhasis
# 

import os.path
import re
import couchdb
import datetime
import ConfigParser

from tornado.options import options

from src.BaseHandler import BaseHandler

class CreateToken(BaseHandler):
    config = ConfigParser.ConfigParser()
    def post(self):
        configPath=os.path.dirname(os.path.realpath(__file__))+'/../config/masterConfig.cnf'
        self.config.read(configPath)
        streamId=self.get_argument(self.config.get('AccessParameters', 'Access.Identifier'))
        accessToken=self.get_argument(self.config.get('AccessParameters', 'Access.Token'))
        matchObj = re.match(self.config.get('IdentifierFormat', 'Identifier.Format'), streamId)
        self.set_header("Content-Type", "application/json")
        if matchObj is None:
            self.write({"error":self.config.get('ErrorMsg', 'Invalid.Identifier')})
            return
        try:
            db = self.dbserver[options.api_tokens_database]
        except :            
            couch = couchdb.Server(options.couch_host)
            db = couch.create(options.api_tokens_database)
        viewPath=os.path.dirname(os.path.realpath(__file__))+'/../scripts/checkAPIToken.js'
        with open (viewPath, "r") as myfile:
            map_all=myfile.read().replace('~accessToken~', accessToken)        
        records=db.query(map_all)
        a=[]
        for r in records:
            a.append(r)        
        if len(a) == 0:
            newRecord={}
            streams=[]
            stream={}
            stream["streamId"]=streamId
            stream["status"]=self.get_argument("status")
            stream["createdTime"]=datetime.datetime.now().isoformat()
            stream["lastUpdatedTime"]=datetime.datetime.now().isoformat()
            streams.append(stream)
            newRecord["token"]=accessToken
            newRecord["streams"]=streams
            db.save(newRecord)            
        else:            
            for row in records:
                stream={}
                stream["streamId"]=streamId
                stream["status"]=self.get_argument("status")
                stream["createdTime"]=datetime.datetime.now().isoformat()
                stream["lastUpdatedTime"]=datetime.datetime.now().isoformat()
                row.value["streams"].append(stream)
                db[row.id]=row.value                          
        self.write({"Success":"New Token added."})    
        self.set_header("Content-Type", "application/json")