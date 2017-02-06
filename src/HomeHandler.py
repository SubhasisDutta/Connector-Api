#!/usr/bin/env python
#
# Copyright 2014 @author Subhasis

import os.path
import logging
import ConfigParser
from src.BaseHandler import BaseHandler

logger= logging.getLogger('log.application')

class HomeHandler(BaseHandler):
    config = ConfigParser.ConfigParser()
    def get(self):
        configPath=os.path.dirname(os.path.realpath(__file__))+'/../config/masterConfig.cnf'
        self.config.read(configPath)
        logger.info(self.config.get('Logging', 'Logger.HomeMessage1')+''+self.request.remote_ip)
        self.write({"ConnectorAPI":"Welcome","Status":"Server Running"})
        self.set_header("Content-Type", "application/json")
        