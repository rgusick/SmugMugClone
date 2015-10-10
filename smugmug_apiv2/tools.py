#!/usr/bin/env python3

from rauth import OAuth1Session
import sys
import json
import os
import logging

from common import API_ORIGIN, get_service, add_auth_params
from smugmug_apiv2.utils import process_uri,session,logger

def process_album(album_uri):
    l = logger()
    l.debug(album_uri)

    # Verify that this is the uri of an album
    api_album = process_uri(album_uri)
    #l.debug(json.dumps(api_album, sort_keys=True, indent=4, separators=(',', ': ')))
    
    albumimages_uri = api_album['Album']['Uris']['AlbumImages']['Uri']
    images = process_uri(albumimages_uri)
    # l.debug(json.dumps(images, sort_keys=True, indent=4, separators=(',', ': ')))
    if 'AlbumImage' in images:
        for image in images['AlbumImage']:
            try:
                l.info("\t\t" + image['FileName'])
            except:
                l.error(json.dumps(image, sort_keys=True, indent=4, separators=(',', ': ')))
            
    return 0
                    
def process_node_folder(node_folder,depth=0):
    #
    # A SmugMug Folder can contain other Folders or Albums, which are retrived as a list of ChildNodes
    #

    l = logger()
    indent = '\t' * depth

    # Check that this is a Node and that the Node contains a Folder
    assert 'Node' in node_folder;
    node_type = node_folder['Node']['Type']
    assert node_type == "Folder"
    
    try:
        childnodes_uri = node_folder['Node']['Uris']['ChildNodes']['Uri']
    except:
        l.error(json.dumps(api_node, sort_keys=True, indent=4, separators=(',', ': ')))
        sys.exit("ugh - child nodes")

    # There may be alot of child nodes.  Let's group them together    
    all_nodes = get_all_nodes(childnodes_uri)
        
    if all_nodes is None:
        return

    #l.debug(json.dumps(all_nodes, sort_keys=True, indent=4, separators=(',', ': ')))
    num_children = len(all_nodes)
    l.debug("Processing " + str(num_children) + " child nodes")
    count = 0
    for childnode in all_nodes:
        count = count + 1
        type = childnode['Type']
        
        if type == "Album":
            l.info(indent + type  + " '" + childnode['Name'] + "'")
            # We have a node and not an album
            album_uri = childnode['Uris']['Album']['Uri']
            l.info(album_uri)
            process_album(album_uri)
        elif type == "Node":
            l.info(indent + type  + " '" + childnode['Name'] + "'")
            node_recurse(childnode['Uri'],depth+1)
        elif type == "Folder":
            l.info(indent + type  + " '" + childnode['Name'] + "'")
            folder = process_uri(childnode['Uri'])
            process_node_folder(folder,depth+1)
        else:
            l.warning(indent + type + " '" + childnode['Name'] + "' (UNKNOWN)")
            
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
    if not 'Node' in api_nodes:
        return None

    nodes = api_nodes['Node']
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
