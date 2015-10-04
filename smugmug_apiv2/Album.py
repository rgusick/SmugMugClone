#!/usr/bin/env python3

from smugmug_apiv2.utils import process_uri
from smugmug_apiv2 import User
from smugmug_apiv2 import Node

# The album endpoint provides access to album settings and album contents. Albums are also known as galleries.
# For a simpler, unified view of folders, albums, and pages, use the Node endpoint instead.

def GenericAlbum(function, album): return process_uri("/api/v2/album/" + album + ("!" + function if function != None else ""))

def AlbumComments(album): return GenericAlbum("albumcomments",album)
def AlbumDownload(album): return GenericAlbum("",album)
def AlbumGeoMedia(album): return GenericAlbum("",album)
def AlbumHighlightImage(album): return GenericAlbum("",album)
def AlbumImages(album): return GenericAlbum("",album)
def AlbumPopularMedia(album): return GenericAlbum("",album)
def AlbumPrices(album): return GenericAlbum("",album)
# Folder
# HighlightImage
def Node(album):
    ret = GenericAlbum(None,album)
    return Node.GenericNode(None, ret['NodeId'])
# ParentFolder
def User(nickname = None): return User.Generic(None,nickname)
