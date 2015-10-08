#!/usr/bin/env python3

from rauth import OAuth1Session
import sys
import json
import os
import logging

from common import API_ORIGIN, get_service, add_auth_params
from smugmug_apiv2.utils import process_uri,session,logger

def process_album(album_uri,indent=0):
    logger = logger()
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
                    
def process_node_folder(node_folder,depth=0):
    l = logger()
    indent = '\t' * depth
    l.debug(node_folder['Node']['Type'] + " " + node_folder['Node']['UrlName'])
    # A folder can contain 0 or more other folders
    # A folder can contain 0 or more albums

    try:
        childnodes_uri = node_folder['Node']['Uris']['ChildNodes']['Uri']
    except:
        l.error(json.dumps(api_node, sort_keys=True, indent=4, separators=(',', ': ')))
        sys.exit("ugh - child nodes")

    # There may be alot of chold nodes.  Let's group them together    
    all_nodes = get_all_nodes(childnodes_uri)
        
    if all_nodes is None:
        return

    # Process Folders first
    l.debug("Processing " + str(len(all_nodes)) + " nodes")
    count = 0
    for childnode in all_nodes:
        count = count + 1
        type = childnode['Type']
        l.debug(count)
        l.debug(type)
        l.debug(childnode['Name'])
        
        if type == "Album":
            l.info(indent + childnode['Type'] + " '" + childnode['Name'] + "'")
            # We have a node and not an album
            #album_uri = process_uri(childnode['Uri']['Node']['Uris']['Album']['Uri'])
            #process_album(album_uri)
        else:
            l.debug(indent + type + " '" + childnode['Name'] + "' skip")
            
    count = 0
    for childnode in all_nodes:
        count = count + 1
        l.debug(count)

        if childnode['Type'] == "Folder":
            l.info(indent + childnode['Type'] + " '" + childnode['Name'] + "'")
            node_recurse(childnode['Uri'],depth+1)
        else:
            l.debug(indent + childnode['Type'] + " '" + childnode['Name'] + "' skip")
    
def process_node_album(node_album,depth=0):
    l = logger()
    indent = '\t' * depth
    l.debug(node_album['Node']['Type'] + " " + node_album['Node']['UrlName'])
    album_uri = process_uri(node_album['Uri'])['Node']['Uris']['Album']['Uri']
    process_album(album_uri)

def node_recurse(node_uri,depth=0):
    l = logger()

    l.debug(node_uri + " " + str(depth))
    indent = '\t' * depth
    
    api_node = process_uri(node_uri)
    if api_node['Node']['Type'] == "Folder":
        process_node_folder(api_node,depth)
    elif api_node['Node']['Type'] == "Album":
        process_node_album(api_node,depth)
    else:
        l.debug(api_node['Node']['Type'] + " " + api_node['Node']['UrlName'])
    
def get_all_nodes(node_uri):
    l = logger()

    api_nodes = process_uri(node_uri)
    if 'Node' in api_nodes:
        nodes = api_nodes['Node']
    else:
        return None

    try:
        while ('NextPage' in api_nodes['Pages']):
            node_uri = api_nodes['Pages']['NextPage']
            api_nodes = process_uri(node_uri)
            l.debug("Appending " + str(len(api_nodes['Node'])) + " to " + str(len(nodes)))
        nodes = nodes + api_nodes['Node']
    except:
        l.error(json.dumps(api_nodes, sort_keys=True, indent=4, separators=(',', ': ')))
        l.error(str(api_nodes['Code']) + " - " + api_nodes['Message'])
        
    #logger.warn(node_uri + " has " + str(len(nodes)) + " children")
    return nodes
