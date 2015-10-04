#!/usr/bin/env python3
from rauth import OAuth1Session
import sys,json,os,logging

from common import API_ORIGIN, get_service, add_auth_params

def process_album(album_uri):
    logger.debug(album_uri)
    api_album = process(album_uri)
    logger.debug(json.dumps(api_album, sort_keys=True, indent=4, separators=(',', ': ')))
    
    albumimages_uri = api_album['Album']['Uris']['AlbumImages']['Uri']
    images = get_all_images(albumimages_uri)
    logger.debug(json.dumps(images, sort_keys=True, indent=4, separators=(',', ': ')))
    for image in images:
        try:
            logger.info("\t\t\t" + image['FileName'])
        except:
            logger.error(json.dumps(image, sort_keys=True, indent=4, separators=(',', ': ')))
            
    return 0
                    
def node_recurse(node_uri,depth):
    global logger
    
    # logger.info(node_uri + " " + str(depth))
    indent = '\t' * depth

    logger.debug(indent + API_ORIGIN + node_uri)
    api_node = session.get(
        API_ORIGIN + node_uri,
        headers={'Accept': 'application/json'}).json()
    logger.debug(json.dumps(api_node, sort_keys=True, indent=4, separators=(',', ': ')))

    # childnodes_uri = api_node['Response']['Node']['Uris']['ChildNodes']['Uri'] + "?count=999"
    childnodes_uri = api_node['Response']['Node']['Uris']['ChildNodes']['Uri']

    logger.debug(indent + API_ORIGIN + childnodes_uri)
    api_childnodes = session.get(
        API_ORIGIN + childnodes_uri,
        headers={'Accept': 'application/json'}).json()
    logger.debug(json.dumps(api_childnodes, sort_keys=True, indent=4, separators=(',', ': ')))

    all_nodes = get_all_nodes(childnodes_uri)
    for childnode in all_nodes:
        logger.debug(json.dumps(childnode, sort_keys=True, indent=4, separators=(',', ': ')))
        logger.info(indent + childnode['Type'] + " '" + childnode['Name'] + "'")
        
        if childnode['Type'] == "Album":
            process_album(childnode['Uris']['Album']['Uri'])
            
        if childnode['HasChildren']:
            node_recurse(childnode['Uri'],depth+1)

    return 1

def folder_recurse(albums_uri,folders_uri,depth):
    # logger.info(albums_uri + " " + folders_uri + " " + str(depth))
    indent = '\t' * depth
    logger.info(albums_uri);
    logger.info(folders_uri);
    
    api_folderalbums = session.get(
        API_ORIGIN + albums_uri,
        headers={'Accept': 'application/json'}).json()
    api_userfolders = session.get(
        API_ORIGIN + folders_uri,
        headers={'Accept': 'application/json'}).json()

    # 1) Dump the list of albums
    # 2) Traverse the sub folders
    
    # logger.info(albums_uri)
    #logger.info(json.dumps(api_folderalbums, sort_keys=True, indent=4, separators=(',', ': ')))
    try:
        for album in api_folderalbums['Response']['Album']:
            logger.info(indent + "'" + album["Name"] + "' "+ str(album["ImageCount"]))
            logger.info(json.dumps(album, sort_keys=True, indent=4, separators=(',', ': ')))
    except KeyError:
        logger.debug(indent + "No albums")
    
    # logger.info(indent + folders_uri)
    try:
        for folder in api_userfolders['Response']['Folder']:
            logger.info(indent + "Folder " + folder['Name'] + " (" + folder['UrlName'] + ")")
            logger.debug(json.dumps(folder, sort_keys=True, indent=4, separators=(',', ': ')))

            # Get the list of Albums and Folders in this folder
            uri_new_albums = folder['Uris']['FolderAlbums']['Uri'] 
            uri_new_folders = folder['Uris']['Folders']['Uri'] 
            
            # Recursively traverse the folder/album structure
            folder_recurse(uri_new_albums,uri_new_folders,depth+1)
    except KeyError:
        pass
        #logger.info("No sub-folders")
        #logger.info(json.dumps(api_userfolders, sort_keys=True, indent=4, separators=(',', ': ')))
        
    return 1
