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
    # def GenericAlbum(self,function, album): return process_uri("/api/v2/album/" + album + ("!" + function if function != None else ""))

    def AlbumComments(self,album): return self.GenericField("albumcomments",album)
    def AlbumDownload(self,album): return self.GenericField("download",album)
    def AlbumGeoMedia(self,album): return self.GenericField("geomedia",album)
    def AlbumHighlightImage(self,album): return self.GenericField("highlightimage",album)
    def AlbumImages(self,album): return self.GetGenericUriObject("images",album)
    def AlbumPopularMedia(self,album): return self.GenericField("popularmedia",album)
    def AlbumPrices(self,album): return self.GenericField("prices",album)
    # Folder
    # HighlightImage
    def Node(self,album):
        ret = self.GenericField(None,album)
        return Node(self.GenericNode(None, ret['NodeId']))
    # ParentFolder
    def User(self,nickname = None): return User.getNickName()

    ###########################
    # Access elements of Node
    ###########################

    #def GetGenericAlbum(self,field,result = None):
    #    if result == None:
    #        result = self.ALBUM
    #    assert 'Album' in result
    #    assert field in result['Album']
    #    return result['Album'][field]
    
    def getUri(self,result = None): return self.GetGenericField('Uri',result)
    def getUriDescription(self,result = None): return self.GetGenericField('UriDescription',result)
    def getResponseLevel(self,result = None): return self.GetGenericField('ResponseLevel',result)
    def getAllowDownloads(self,result = None): return self.GetGenericField('AllowDownloads',result)
    def getCanShare(self,result = None): return self.GetGenericField('CanShare',result)
    def getDescription(self,result = None): return self.GetGenericField('Description',result)
    def getExternal(self,result = None): return self.GetGenericField('External',result)
    def getImageCount(self,result = None): return self.GetGenericField('ImageCount',result)
    def getImagesLastUpdated(self,result = None): return self.GetGenericField('ImagesLastUpdated',result)
    def getKeywords(self,result = None): return self.GetGenericField('Keywords',result)
    def getLastUpdated(self,result = None): return self.GetGenericField('LastUpdated',result)
    def getName(self,result = None): return self.GetGenericField('Name',result)
    def getNiceName(self,result = None): return self.GetGenericField('NiceName',result)
    def getNodeID(self,result = None): return self.GetGenericField('NodeID',result)
    def getPasswordHint(self,result = None): return self.GetGenericField('PasswordHint',result)
    def getProtected(self,result = None): return self.GetGenericField('Protected',result)
    def getSecurityType(self,result = None): return self.GetGenericField('SecurityType',result)
    def getSortDirection(self,result = None): return self.GetGenericField('SortDirection',result)
    def getSortMethod(self,result = None): return self.GetGenericField('SortMethod',result)
    def getTitle(self,result = None): return self.GetGenericField('Title',result)
    def getUrlName(self,result = None): return self.GetGenericField('UrlName',result)
    def getUrlPath(self,result = None): return self.GetGenericField('UrlPath',result)
    def getWebUri(self,result = None): return self.GetGenericField('WebUri',result)
    def getUris(self,result = None): return self.GetGenericField('Uris',result)
