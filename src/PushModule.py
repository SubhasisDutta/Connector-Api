#!/usr/bin/env python
#
# Copyright 2014 @author Subhasis

from time import time
import json
import datetime
import couchdb
import ConfigParser
import os.path

import logging

from tornado.options import options


from lib.XmlToDict import parse
from src.BaseHandler import BaseHandler
from src.ValidateToken import validateStreamToken

logger= logging.getLogger('log.application')

class PushModule(BaseHandler):
    logData={}    
    config = ConfigParser.ConfigParser()
    def post(self):
        request = self.request    
        self.logData={}
        configPath=os.path.dirname(os.path.realpath(__file__))+'/../config/masterConfig.cnf'
        self.config.read(configPath)
        logger.info(self.config.get('Logging', 'Logger.PostMessage1')+''+request.remote_ip)
        self.logData["referralIPAddress"]=request.remote_ip
        self.logData["Content-Type"]=request.headers["Content-Type"]
        self.logData["datetime"]= datetime.datetime.now().isoformat()
        bodyString=str(request.body)
        responseStr=""        
        if "/json" in self.logData["Content-Type"]:            
            logger.info(self.config.get('Logging', 'Logger.PostMessage2'))
            responseStr=self.logSaveData(self.parseJsonData(bodyString))
        elif "/xml" in self.logData["Content-Type"]:
            logger.info(self.config.get('Logging', 'Logger.PostMessage3'))
            responseStr=self.logSaveData(self.paseXmlData(bodyString))
        elif "/csv" in self.logData["Content-Type"]:
            logger.info(self.config.get('Logging', 'Logger.PostMessage4'))
            responseStr=self.logSaveData(self.parseCsvData(bodyString))
        else:            
            responseStr='{"status":"'+self.config.get('ErrorMsg', 'ContentType.Unsupported')+'"}'
            logger.error(self.config.get('Logging', 'Logger.PostMessage5')+''+request.remote_ip)
        self.set_header("Content-Type", "application/json")
        self.logPushRequest()
        self.write(responseStr)
    
    def logSaveData(self,data):
        if data is not None:              
            start_time = time()
            self.logData["docIDs"],self.logData["state"]=self.saveDocs(data,self.logData[self.config.get('AccessParameters', 'Access.Identifier')])
            end_time = time()             
            time_taken = end_time - start_time
            self.logData["responseTimeMS"]=time_taken*1000
            logger.info(self.config.get('Logging', 'Logger.PostMessage6')+' '+str(self.logData["docIDs"]))                
        else:
            self.logData["state"]=self.config.get('ErrorMsg', 'Invalid.Push')
            logger.error(self.config.get('Logging', 'Logger.PostMessage7')+' '+self.logData["state"])
        return json.dumps(self.logData)
    
    def parseJsonData(self,bodyString):
        try:
            requestObj=json.loads(bodyString)
        except ValueError:
            ustr_to_load = unicode(bodyString, 'latin-1')
            requestObj=json.loads(ustr_to_load)
            logger.info(self.config.get('Logging', 'Logger.PostMessage8'))
        except:
            logger.error(self.config.get('Logging', 'Logger.PostMessage9'))
            return None
        self.logData[self.config.get('AccessParameters', 'Access.Identifier')]=requestObj["Message"]["Header"][self.config.get('AccessParameters', 'Access.Identifier')]
        self.logData[self.config.get('AccessParameters', 'Access.Token')]=requestObj["Message"]["Header"][self.config.get('AccessParameters', 'Access.Token')]
        self.logData["totalDocs"]=len(requestObj["Message"]["Body"]["docs"])
        if self.validTokens(self.logData["streamId"],self.logData["accessToken"]):
            return requestObj["Message"]["Body"]["docs"]
        else:
            logger.error(self.config.get('Logging', 'Logger.PostMessage10')+' '+self.logData["streamId"]+' '+self.logData["accessToken"])
            return None
    
    def paseXmlData(self,bodyString):
        try:
            requestObj=parse(bodyString)
        except:
            logger.error(self.config.get('Logging', 'Logger.PostMessage11'))
            return None      
        self.logData["streamId"]=requestObj["Message"]["Header"]["streamId"]
        self.logData["accessToken"]=requestObj["Message"]["Header"]["accessToken"]
        self.logData["totalDocs"]=len(requestObj["Message"]["Body"]["docs"])        
        if self.validTokens(self.logData["streamId"],self.logData["accessToken"]):
            return requestObj["Message"]["Body"]["docs"]
        else:
            logger.error(self.config.get('Logging', 'Logger.PostMessage12')+' '+self.logData["streamId"]+' '+self.logData["accessToken"])
            return None
    
    def parseCsvData(self,bodyString):
        self.logData[self.config.get('AccessParameters', 'Access.Identifier')]=self.get_argument(self.config.get('AccessParameters', 'Access.Identifier'))
        self.logData[self.config.get('AccessParameters', 'Access.Token')]=self.get_argument(self.config.get('AccessParameters', 'Access.Token'))
        if self.validTokens(self.logData["streamId"],self.logData["accessToken"]):
            requestObj=[]
            docs=bodyString.splitlines()
            keys=docs[0].split(',')
            for doc in docs[1:]:
                values=doc.split(',')
                docObject={}
                i=0
                for key in keys: 
                    docObject[key]=values[i]
                    i=i+1
                requestObj.append(docObject)        
            self.logData["totalDocs"]=len(requestObj)
            return requestObj
        else:
            logger.error(self.config.get('Logging', 'Logger.PostMessage13')+' '+self.logData["streamId"]+' '+self.logData["accessToken"])
            return None
        
    
    def validTokens(self,streamId,token):    
        checkToken=validateStreamToken()
        validationResult=checkToken.validate(streamId, token)
        if validationResult["status"]=="success":
            return True
        return False
    
    def saveDocs(self,docs,streamId):
        docIDs=[]        
        databaseName=options.couch_docs_database.replace("~streamId~",streamId)
        try:
            db = self.dbserver[databaseName]
        except :            
            couch = couchdb.Server(options.couch_host)
            db = couch.create(databaseName)
        docSave="Valid Docs"
        for doc in docs:
            try:
                doc_id, doc_rev =db.save(doc)
                docIDs.append(doc_id)                
            except couchdb.http.ResourceConflict:
                docIDs.append(0)
                docSave="Invalid Docs"
                logger.error(self.config.get('Logging', 'Logger.PostMessage14'))
        logger.info(self.config.get('Logging', 'Logger.PostMessage15')+' '+str(len(docIDs)))
        return docIDs,docSave
    
    def logPushRequest(self):
        try:
            db = self.dbserver[options.couch_logs_database]            
        except :            
            couch = couchdb.Server(options.couch_host)
            db = couch.create(options.couch_logs_database)        
        db.save(self.logData)
