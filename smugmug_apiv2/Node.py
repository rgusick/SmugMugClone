#!/usr/bin/env python3

import logging

from smugmug_apiv2.utils import process_uri

from smugmug_apiv2.SmugMugBase import SmugMugBase
from smugmug_apiv2.User import User

# A node is a folder, album, or page. Folders contain albums, pages, and other folders, and albums contain images.
# To browse a user's node hierarchy, you will typically start at the root by following the Node link from the User endpoint.

class Node(SmugMugBase):
    'Implement interface documented at https://api.smugmug.com/api/v2/doc/reference/node.html'

    def __init__(self, obj = None):
        SmugMugBase.__init__(self)

        # self.logger = logging.getLogger('SmugMugClone')

        self.TYPE = 'Node'
        self.URI = '/api/v2/node/'
        # self.logger.debug(uri)
        if isinstance(obj,str):
            self.OBJECT = process_uri(obj)
        elif isinstance(uri,dict):
            self.OBJECT = obj
        else:
            sys.exit('Bad initialization object')

            
    ###########################

    ###########################
    # Access elements of Node
    ###########################

    def getUri(self,result = None): return self.getGenericField('Uri',result)
    def getUriDescription(self,result = None): return self.getGenericField('UriDescription',result)
    def getResponseLevel(self,result = None): return self.getGenericField('ResponseLevel',result)
    def getDateAdded(self,result = None): return self.getGenericField('DateAdded',result)
    def getDateModified(self,result = None): return self.getGenericField('DateModified',result)
    def getDescription(self,result = None): return self.getGenericField('Description',result)
    def getEffectiveSecurityType(self,result = None): return self.getGenericField('EffectiveSecurityType',result)
    def getHasChildren(self,result = None): return self.getGenericField('HasChildren',result)
    def getIsRoot(self,result = None): return self.getGenericField('IsRoot',result)
    def getKeywords(self,result = None): return self.getGenericField('Keywords',result)
    def getName(self,result = None): return self.getGenericField('Name',result)
    def getNodeID(self,result = None): return self.getGenericField('NodeID',result)
    def getPasswordHint(self,result = None): return self.getGenericField('PasswordHint',result)
    def getSecurityType(self,result = None): return self.getGenericField('SecurityType',result)
    def getSortDirection(self,result = None): return self.getGenericField('SortDirection',result)
    def getSortIndex(self,result = None): return self.getGenericField('SortIndex',result)
    def getSortMethod(self,result = None): return self.getGenericField('SortMethod',result)
    def getType(self,result = None): return self.getGenericField('Type',result)
    def getUrlName(self,result = None): return self.getGenericField('UrlName',result)
    def getUrlPath(self,result = None): return self.getGenericField('UrlPath',result)
    def getWebUri(self,result = None): return self.getGenericField('WebUri',result)
    def getUris(self,result = None): return self.getGenericField('Uris',result)

    # Uri Funtions
    
    def getChildNodes_uri(self): return self.getGenericUris("ChildNodes")
    # FolderById
    # HighlighImage
    def getParentNode_uri(self): return self.getGenericUris("ParentNode")
    def getParentNodes_uri(self): return self.getGenericUris("ParentNoded")
    def getUser_uri(self): return self.getGenericUris("User")

    def getChildNodes_dict(self): return self.getGenericUriObject("ChildNodes")
    # FolderById
    # HighlighImage
    def getParentNode_dict(self): return self.getGenericUriObject("ParentNode")
    def getParentNodes_dict(self): return self.getGenericUriObject("ParentNoded")
    def getUser_dict(self): return self.getGenericUriObject("User")
