#!/usr/bin/env python3

import logging

from smugmug_apiv2.utils import process_uri

from smugmug_apiv2.SmugMugBase import SmugMugBase
from smugmug_apiv2.Uri import Uri

# Implement interface documented at https://api.smugmug.com/api/v2/doc/reference/user.html
# A user is a SmugMug user account.

class User(SmugMugBase):
    'Implement interface documented at https://api.smugmug.com/api/v2/doc/reference/user.html'

    def __init__(self):
        SmugMugBase.__init__(self)

        self.NICKNAME = None
        self.OBJECT = None

        self.TYPE = 'User'
        self.URI = '/api/v2/user/'

        self.authuser()

    # Special users
    #   Two special endpoints return a user relative to the current session:
    #    /api/v2!authuser   The authenticated user
    #    /api/v2!siteuser   The user whose domain you are on
        
    def authuser(self):
        # https://api.smugmug.com/api/v2!authuser
        
        self.OBJECT = process_uri('/api/v2!authuser')
        self.NICKNAME = self.getNickName()
        
        return self.OBJECT

    def siteuser(self):
        # https://api.smugmug.com/api/v2!siteuser
    
        self.OBJECT = process_uri('/api/v2!siteuser')
        self.NICKNAME = self.getNickName()

        return self.OBJECT

    ###########################
    # Access elements of User
    ###########################

    def getUri(self,result = None): return self.getGenericField('Uri',result)
    def getUriDescription(self,result = None): return self.getGenericField('UriDescription',result)
    def getResponseLevel(self,result = None): return self.getGenericField('ResponseLevel',result)
    def getName(self,result = None): return self.getGenericField('Name',result)
    def getNickName(self,result = None): return self.getGenericField('NickName',result)
    def getRefTag(self,result = None): return self.getGenericField('RefTag',result)
    def getViewHint(self,result = None): return self.getGenericField('ViewPassHint',result)
    def getWebUri(self,result = None): return self.getGenericField('WebUri',result)
    def getUris(self,result = None): return self.getGenericField('Uris',result)

    ###########################
    # Access URI functions of User
    ###########################

    def getBioImage_uri(self,result = None): return self.getGenericUris('BioImage',result)
    def getCoverImage_uri(self,result = None): return self.getGenericURI('CoverImage',result)
    def getFolder_uri(self,result = None): return self.getGenericUris('Folder',result)
    def getNode_uri(self,result = None): return self.getGenericUris('Node',result)
    def getUrlPathLookup_uri(self,result = None): return self.getGenericUris('UrlPathLookup',result)
    def getUserAlbums_uri(self,result = None): return self.getGenericUris('UserAlbums',result)
    def getUserFeaturedAlbums_uri(self,result = None): return self.getGenericUris('UserFeaturedAlbums',result)
    def getUserGeoMedia_uri(self,result = None): return self.getGenericUris('UserGeoMedia',result)
    def getUserImageSearch_uri(self,result = None): return self.getGenericUris('UserImageSearch',result)
    def getUserPopularMedia_uri(self,result = None): return self.getGenericUris('UserPopularMedia',result)
    def getUserProfile_uri(self,result = None): return self.getGenericUris('UserProfile',result)
    def getUserRecentImages_uri(self,result = None): return self.getGenericUris('UserRecentImages',result)
    def getUserTopKeywords_uri(self,result = None): return self.getGenericUris('UserTopKeywords',result)

    ###########################
    # These methods return a dict of results
    
    def getBioImage_dict(self): return self.getGenericUriObject("BioImage")
    def getCoverImage_dict(self): return self.getGenericUriObject("CoverImage")
    # We might not need this (VVVVV)
    def getFolder_dict(self):
        return process_uri("/api/v2/folder/" + self.NICKNAME)
    # Node
    def getUrlPathLookup_dict(self): return self.getGenericUriObject("UrlPathLookup")
    def getUserlbums_dict(self): return self.getGenericUriObject("UserAlbums")
    def getUserFeaturedAlbums_dict(self): return self.getGenericUriObject("NicknameFeaturedAlbums")
    def getUserGeoMedia_dict(self): return self.getGenericUriObject("UserGeoMedia")
    def getUserImageSearch_dict(self): return self.getGenericUriObject("UserImageSearch")
    def getUserPopularMedia_dict(self): return self.getGenericUriObject("UserPopularMedia")
    def getUserProfile_dict(self): return self.getGenericUriObject("UserProfile")
    def getUserRecentImages_dict(self): return self.getGenericUriObject("UserRecentImages")
    def getUserTopKeywords_dict(self): return self.getGenericUriObject("UserTopKeywords")

    
