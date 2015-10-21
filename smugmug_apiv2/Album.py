#!/usr/bin/env python3

import logging

from smugmug_apiv2.utils import process_uri
from smugmug_apiv2.SmugMugBase import SmugMugBase
from smugmug_apiv2.User import User
from smugmug_apiv2.Node import Node

# The album endpoint provides access to album settings and album contents. Albums are also known as galleries.
# For a simpler, unified view of folders, albums, and pages, use the Node endpoint instead.

class Album(SmugMugBase):
    'Implement interface documented at https://api.smugmug.com/api/v2/doc/reference/album.html'

    def __init__(self, uri = None):
        SmugMugBase.__init__(self)

        # self.logger = logging.getLogger('SmugMugClone')

        self.TYPE = 'Album'
        self.URI = '/api/v2/album/'
        if not uri is None:
            self.OBJECT = process_uri(uri)
            
    ###########################
    # Access elements of Node
    ###########################

    def getUri(self,result = None): return self.getGenericField('Uri',result)
    def getUriDescription(self,result = None): return self.getGenericField('UriDescription',result)
    def getResponseLevel(self,result = None): return self.getGenericField('ResponseLevel',result)
    def getAllowDownloads(self,result = None): return self.getGenericField('AllowDownloads',result)
    def getCanShare(self,result = None): return self.getGenericField('CanShare',result)
    def getDescription(self,result = None): return self.getGenericField('Description',result)
    def getExternal(self,result = None): return self.getGenericField('External',result)
    def getImageCount(self,result = None): return self.getGenericField('ImageCount',result)
    def getImagesLastUpdated(self,result = None): return self.getGenericField('ImagesLastUpdated',result)
    def getKeywords(self,result = None): return self.getGenericField('Keywords',result)
    def getLastUpdated(self,result = None): return self.getGenericField('LastUpdated',result)
    def getName(self,result = None): return self.getGenericField('Name',result)
    def getNiceName(self,result = None): return self.getGenericField('NiceName',result)
    def getNodeID(self,result = None): return self.getGenericField('NodeID',result)
    def getPasswordHint(self,result = None): return self.getGenericField('PasswordHint',result)
    def getProtected(self,result = None): return self.getGenericField('Protected',result)
    def getSecurityType(self,result = None): return self.getGenericField('SecurityType',result)
    def getSortDirection(self,result = None): return self.getGenericField('SortDirection',result)
    def getSortMethod(self,result = None): return self.getGenericField('SortMethod',result)
    def getTitle(self,result = None): return self.getGenericField('Title',result)
    def getUrlName(self,result = None): return self.getGenericField('UrlName',result)
    def getUrlPath(self,result = None): return self.getGenericField('UrlPath',result)
    def getWebUri(self,result = None): return self.getGenericField('WebUri',result)
    def getUris(self,result = None): return self.getGenericField('Uris',result)

    ###########################
    # def GenericAlbum(self,function, album): return process_uri("/api/v2/album/" + album + ("!" + function if function != None else ""))

    def getAlbumComments_dict(self,album): return self.GenericField("albumcomments",album)
    def getAlbumDownload_dict(self,album): return self.GenericField("download",album)
    def getAlbumGeoMedia_dict(self,album): return self.GenericField("geomedia",album)
    def getAlbumHighlightImage_dict(self,album): return self.GenericField("highlightimage",album)
    def getAlbumImages_dict(self): return self.getGenericUriObject("images")
    def getAlbumPopularMedia_dict(self,album): return self.GenericField("popularmedia",album)
    def getAlbumPrices_dict(self,album): return self.GenericField("prices",album)
    # Folder
    # HighlightImage
    def getNode_dict(self,album):
        ret = self.GenericField(None,album)
        return Node(self.GenericNode(None, ret['NodeId']))
    # ParentFolder
    def getUser_dict(self,nickname = None): return User.getNickName()
