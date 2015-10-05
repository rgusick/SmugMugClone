#!/usr/bin/env python3

from smugmug_apiv2.utils import process_uri
from smugmug_apiv2 import Album

# The album endpoint provides access to album settings and album contents. Albums are also known as galleries.
# For a simpler, unified view of folders, albums, and pages, use the Node endpoint instead.

def GenericAlbumImage(function, image): return process_uri("/api/v2/image/" + imafe + ("!" + function if function != None else ""))

def Album(album): return Album.GenericAlbum("",album)
def Image(image): return GenericAlbumImage("",image)
# ImageAlbum
def ImageComments(image): return GenericAlbumImage("comments",image)
def ImageDownload(image): return GenericAlbumImage("download",image)
def ImageMetadata(image): return GenericAlbumImage("metadata",image)
# ImageOwner
def ImagePrices(image): return GenericAlbumImage("prices",image)
def ImageSizeDetails(image): return GenericAlbumImage("sizedetails",image)
def ImageSizes(image): return GenericAlbumImage("sizes",image)
def LargestImage(image): return GenericAlbumImage("largestimage",image)

