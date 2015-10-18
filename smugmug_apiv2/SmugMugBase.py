#!/usr/bin/env python3

import logging
import json

from smugmug_apiv2.utils import process_uri

class SmugMugBase:
    'Common base class for all SmugMug classes'
    
    def __init__(self):
        self.logger = logging.getLogger('SmugMugClone')

        self.OBJECT = None
        self.TYPE = 'SmugMugBase'

    def GetGenericField(self,field,result = None):
        #
        # Access the field passed in the result
        #
        if result == None:
            result = self.OBJECT
        if not self.TYPE in result:
            self.logger.critical(self.TYPE)
        assert self.TYPE in result;
        if not field in result[self.TYPE]:
            self.logger.critical(json.dumps(result, sort_keys=True, indent=4, separators=(',', ': ')))
            self.logger.critical(field)
        assert field in result[self.TYPE]
        return result[self.TYPE][field]

    def GetGenericUris(self,field,result = None):
        #
        # Access the 'Uris' field in the result
        # Return a dict object
        #
        uris = self.GetGenericField('Uris',result)
        assert field in uris;
        return uris[field]

    def GetGenericUriObject(self,field,result = None):
        uri = self.GetGenericUris(field,result)['Uri']
        self.logger.critical(uri)
        print (uri)
        result = process_uri(uri)
        if 'Code' in result:
            self.logger.critical(result['Code'])
            print (result['Code'])
        if 'Message' in result:
            self.logger.critical(result['Message'])
            print (result['Message'])
        return result

