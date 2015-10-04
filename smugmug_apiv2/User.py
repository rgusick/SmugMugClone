#!/usr/bin/env python3

from smugmug_apiv2.utils import process_uri

# Implement interface documented at https://api.smugmug.com/api/v2/doc/reference/user.html
# A user is a SmugMug user account.

NICKNAME = None
USER = None

def authuser():
    # https://api.smugmug.com/api/v2!authuser
    global USER,NICKNAME

    USER = process_uri('/api/v2!authuser')
    NICKNAME = USER['User']['NickName']

    return USER

def siteuser():
    # https://api.smugmug.com/api/v2!siteuser
    global USER,NICKNAME

    USER = process_uri('/api/v2!siteuser')
    NICKNAME = USER['User']['NickName']

    return USER

def GenericUser(function, nickname = None):
    global NICKNAME

    return process_uri("/api/v2/user/" + (NICKNAME if nickname == None else nickname) + ("!" + function if function != None else ""))
    
def BioImage(nickname = None): return GenericUser("bioimage",nickname)
def CoverImage(nickname = None): return GenericUser("coverimage",nickname)
# We might not need this (VVVVV)
def Folder(nickname = None):
    global NICKNAME
    return process_uri("/api/v2/folder/" + (NICKNAME if nickname == None else nickname))
# Node
def UrlPathLookup(nickname = None): return GenericUser("urlpathlookup",nickname)
def Userlbums(nickname = None): return GenericUser("useralbums",nickname)
def UserFeaturedAlbums(nickname = None): return GenericUser("nicknamefeaturedalbums",nickname)
def UserGeoMedia(nickname = None): return GenericUser("usergeomedia",nickname)
def UserImageSearch(nickname = None): return GenericUser("userimagesearch",nickname)
def UserPopularMedia(nickname = None): return GenericUser("userpopularmedia",nickname)
def UserProfile(nickname = None): return GenericUser("userprofile",nickname)
def UserRecentImages(nickname = None): return GenericUser("userrecentimages",nickname)
def UserTopKeywords(nickname = None): return GenericUser("usertopkeywords",nickname)
