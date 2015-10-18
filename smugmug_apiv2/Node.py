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

    # def GenericNode(self,function,node): return process_uri(self.URI + node + ("!" + function if function != None else ""))

    def ChildNodes(self,node): return self.GenericField("children",node)
    # FolderById
    # HighlighImage
    def ParentNode(self,node): return self.GenericField("parent",node)
    def ParentNodes(self,node): return self.GenericField("parentnodes",node)
    def User(self,nickname = None): return self.User.Generic("",nickname)

    ###########################
    # Access elements of Node
    ###########################

    #def GetGenericNode(self,field,result = None):
    #    if result == None:
    #        result = self.OBJECT
    #    assert 'Node' in result
    #    assert field in result['Node']
    #    return result['Node'][field]
    
    def getUri(self,result = None): return self.GetGenericField('Uri',result)
    def getUriDescription(self,result = None): return self.GetGenericField('UriDescription',result)
    def getResponseLevel(self,result = None): return self.GetGenericField('ResponseLevel',result)
    def getDateAdded(self,result = None): return self.GetGenericField('DateAdded',result)
    def getDateModified(self,result = None): return self.GetGenericField('DateModified',result)
    def getDescription(self,result = None): return self.GetGenericField('Description',result)
    def getEffectiveSecurityType(self,result = None): return self.GetGenericField('EffectiveSecurityType',result)
    def getHasChildren(self,result = None): return self.GetGenericField('HasChildren',result)
    def getIsRoot(self,result = None): return self.GetGenericField('IsRoot',result)
    def getKeywords(self,result = None): return self.GetGenericField('Keywords',result)
    def getName(self,result = None): return self.GetGenericField('Name',result)
    def getNodeID(self,result = None): return self.GetGenericField('NodeID',result)
    def getPasswordHint(self,result = None): return self.GetGenericField('PasswordHint',result)
    def getSecurityType(self,result = None): return self.GetGenericField('SecurityType',result)
    def getSortDirection(self,result = None): return self.GetGenericField('SortDirection',result)
    def getSortIndex(self,result = None): return self.GetGenericField('SortIndex',result)
    def getSortMethod(self,result = None): return self.GetGenericField('SortMethod',result)
    def getType(self,result = None): return self.GetGenericField('Type',result)
    def getUrlName(self,result = None): return self.GetGenericField('UrlName',result)
    def getUrlPath(self,result = None): return self.GetGenericField('UrlPath',result)
    def getWebUri(self,result = None): return self.GetGenericField('WebUri',result)
    def getUris(self,result = None): return self.GetGenericField('Uris',result)
