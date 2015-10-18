#!/usr/bin/env python3

import logging

from smugmug_apiv2.utils import process_uri

from smugmug_apiv2.SmugMugBase import SmugMugBase

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

    def getUri(self,result = None): return self.GetGenericField('Uri',result)
    def getUriDescription(self,result = None): return self.GetGenericField('UriDescription',result)
    def getResponseLevel(self,result = None): return self.GetGenericField('ResponseLevel',result)
    def getName(self,result = None): return self.GetGenericField('Name',result)
    def getNickName(self,result = None): return self.GetGenericField('NickName',result)
    def getRefTag(self,result = None): return self.GetGenericField('RefTag',result)
    def getViewHint(self,result = None): return self.GetGenericField('ViewPassHint',result)
    def getWebUri(self,result = None): return self.GetGenericField('WebUri',result)
    def getUris(self,result = None): return self.GetGenericField('Uris',result)

    ###########################
    # Access URI functions of User
    ###########################

    def uriBioImage(self,result = None): return self.GetGenericUris('BioImage',result)
    def uriCoverImage(self,result = None): return self.GetGenericURI('CoverImage',result)
    def uriFolder(self,result = None): return self.GetGenericUris('Folder',result)
    def uriNode(self,result = None): return self.GetGenericUris('Node',result)
    def uriUrlPathLookup(self,result = None): return self.GetGenericUris('UrlPathLookup',result)
    def uriUserAlbums(self,result = None): return self.GetGenericUris('UserAlbums',result)
    def uriUserFeaturedAlbums(self,result = None): return self.GetGenericUris('UserFeaturedAlbums',result)
    def uriUserGeoMedia(self,result = None): return self.GetGenericUris('UserGeoMedia',result)
    def uriUserImageSearch(self,result = None): return self.GetGenericUris('UserImageSearch',result)
    def uriUserPopularMedia(self,result = None): return self.GetGenericUris('UserPopularMedia',result)
    def uriUserProfile(self,result = None): return self.GetGenericUris('UserProfile',result)
    def uriUserRecentImages(self,result = None): return self.GetGenericUris('UserRecentImages',result)
    def uriUserTopKeywords(self,result = None): return self.GetGenericUris('UserTopKeywords',result)

    ###########################
    # These methods return a dict of results
    
    def BioImage(self): return self.GetGenericUriObject("BioImage")
    def CoverImage(self): return self.GetGenericUriObject("CoverImage")
    # We might not need this (VVVVV)
    def Folder(self):
        return process_uri("/api/v2/folder/" + self.NICKNAME)
    # Node
    def UrlPathLookup(self): return self.GetGenericUriObject("UrlPathLookup")
    def Userlbums(self): return self.GetGenericUriObject("UserAlbums")
    def UserFeaturedAlbums(self): return self.GetGenericUriObject("NicknameFeaturedAlbums")
    def UserGeoMedia(self): return self.GetGenericUriObject("UserGeoMedia")
    def UserImageSearch(self): return self.GetGenericUriObject("UserImageSearch")
    def UserPopularMedia(self): return self.GetGenericUriObject("UserPopularMedia")
    def UserProfile(self): return self.GetGenericUriObject("UserProfile")
    def UserRecentImages(self): return self.GetGenericUriObject("UserRecentImages")
    def UserTopKeywords(self): return self.GetGenericUriObject("UserTopKeywords")

    
