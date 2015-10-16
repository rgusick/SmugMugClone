#!/usr/bin/env python3

from rauth import OAuth1Session
import sys
import json
import os
import logging
import re
import urllib.request
import shutil
import time
import datetime

from smugmug_apiv2.utils import process_uri,session,logger

def forcetime(file_or_dir,datetime_string):
    t = time.strptime(datetime_string, '%Y-%m-%dT%H:%M:%S+00:00')
    dt = int(time.mktime(t))
    # Set the file date to the date from SmugMug
    os.utime(file_or_dir,(dt, dt))    

def smdownload(url,file_name,datetime_string):
    # Download the file from `url` and save it locally under `file_name`:

    finished = False
    count = 3
    while not finished:
        try:
            with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
                shutil.copyfileobj(response, out_file)
            finished = True
        except IOError as e:
            l = logger()
            l.warning("Could not download " + url + " to " + file_name)
            msg = e.read().decode("utf8", 'ignore')
            l.error(e + " " + msg)
        except:
            l = logger()
            l.warning("Could not download " + url + " to " + file_name)
            l.error(sys.exc_info()[0])
        count -= 1
        finished = (count == 0)
            
    if count != 0:
        raise("Could not download " + url + " to " + file_name)
    
    # Set the file date to the date from SmugMug
    forcetime(file_name,datetime_string)

def mkdir(dir_name,datetime_string):
    l = logger()
    if (os.path.isdir(dir_name)):
        l.debug('EXISTS - ' + dir_name)
    else:
        l.info("mkdir " + dir_name)
        try:
            os.makedirs(dir_name)
            fakedir(dir_name,datetime_string)
        except OSError as exc: # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(dir_name):
                pass
            else:
                raise
        
def process_album(album_uri,dirname=''):
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
            if image['FileName'] != '':
                filename = dirname + image['FileName']
            else:
                calcname = image['ArchivedUri'].rsplit('/',1)[1]
                filename = dirname + calcname
                l.warning('No filename for ' + image['Uri'] + '; using ' + calcname)
            if image['Hidden']:
                l.warning('Skipping HIDDEN image ' + filename)
                continue
            exists = os.path.isfile(filename)
            if exists:
                l.debug("EXISTS - " + filename)
            else:
                try:
                    smdownload ( image['ArchivedUri'],
                                 filename,
                                 image['Date'])
                    l.info('Downloaded ' + filename)
                except:
                    l.warning(image['Uri'])
                    l.critical(json.dumps(image, sort_keys=True, indent=4, separators=(',', ': ')))
                    sys.exit(filename)
    return 0
                    
def process_node_folder(node_folder,depth=0,dirname=''):
    #
    # A SmugMug Folder can contain other Folders or Albums, which are retrived as a list of ChildNodes
    #
    basedir = dirname

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
            #dirname = basedir + childnode['UrlName'] + "/"
            albumname = re.sub('[/]', '', childnode['Name'])
            dirname = basedir + albumname + "/"
            l.info(type + " " + dirname)
            mkdir(dirname,childnode['DateAdded'])
            # We have a node and not an album
            album_uri = childnode['Uris']['Album']['Uri']
            #l.info(album_uri)
            process_album(album_uri,dirname)
        elif type == "Node":
            # dirname = basedir + childnode['UrlName'] + "/"
            dirname = basedir + childnode['Name'] + "/"
            #l.info(type + " " + dirname)
            mkdir(dirname,childnode['DateAdded'])
            node_recurse(childnode['Uri'],depth+1,dirname)
        elif type == "Folder":
            folder = process_uri(childnode['Uri'])
            dirname = basedir + childnode['UrlName'] + "/"
            #l.info(type + " " + dirname)
            # dirname = basedir + childnode['Name'] + "/"
            mkdir(dirname,childnode['DateAdded'])
            process_node_folder(folder,depth+1,dirname)
        else:
            l.warning(indent + type + " '" + childnode['Name'] + "' (UNKNOWN)")
            
def process_node_album(node_album,depth=0,dirname=''):
    l = logger()
    indent = '\t' * depth
    mkdir(dirname,node_album['Date'])
    l.debug(dirname + " " + node_album['Node']['Type'] + " " + node_album['Node']['UrlName'])
    album_uri = process_uri(node_album['Uri'])['Node']['Uris']['Album']['Uri']
    process_album(album_uri,dirname)

def node_recurse(node_uri,depth=0,dirname=''):
    l = logger()

    l.debug(dirname + " " + node_uri + " " + str(depth))
    indent = '\t' * depth
    
    api_node = process_uri(node_uri)
    if api_node['Node']['Type'] == "Folder":
        dirname = dirname + api_node['Node']['UrlName'] + "/"
        mkdir(dirname,api_node['Node']['DateAdded'])
        process_node_folder(api_node,depth,dirname)
    elif api_node['Node']['Type'] == "Album":
        mkdir(dirname,api_node['Node']['DateAdded'])
        process_node_album(api_node,depth,dirname)
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
