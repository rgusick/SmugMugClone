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

from smugmug_apiv2.User import User
from smugmug_apiv2.Node import Node
from smugmug_apiv2.Album import Album

logger = logging.getLogger('SmugMugClone')

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
            # l = logger()
            logger.warning("Could not download " + url + " to " + file_name)
            msg = e.read().decode("utf8", 'ignore')
            logger.error(e + " " + msg)
        except:
            # l = logger()
            logger.warning("Could not download " + url + " to " + file_name)
            logger.error(sys.exc_info()[0])
        count -= 1
        finished = (count == 0)
            
    if count != 0:
        raise("Could not download " + url + " to " + file_name)
    
    # Set the file date to the date from SmugMug
    forcetime(file_name,datetime_string)

def mkdir(dir_name,datetime_string):
    # l = logger()
    if (os.path.isdir(dir_name)):
        logger.debug('EXISTS - ' + dir_name)
    else:
        logger.info("mkdir " + dir_name)
        try:
            os.makedirs(dir_name)
            forcetime(dir_name,datetime_string)
        except OSError as exc: # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(dir_name):
                pass
            else:
                raise
        
def process_album(album,dirname=''):
    # l = logger()
    logger.debug(album.getUri())

    assert 'Album' in album.TYPE;

    #albumimages_uri = album.AlbumImages()['Uri']
    albumimages_uri = album.getUris()['AlbumImages']['Uri']
    images = process_uri(albumimages_uri)
    # l.debug(json.dumps(images, sort_keys=True, indent=4, separators=(',', ': ')))
    if 'AlbumImage' in images:
        for image in images['AlbumImage']:
            if image['FileName'] != '':
                filename = dirname + image['FileName']
            else:
                calcname = image['ArchivedUri'].rsplit('/',1)[1]
                filename = dirname + calcname
                logger.warning('No filename for ' + image['Uri'] + '; using ' + calcname)
            if image['Hidden']:
                logger.warning('Skipping HIDDEN image ' + filename)
                continue
            exists = os.path.isfile(filename)
            if exists:
                logger.debug("EXISTS - " + filename)
            else:
                try:
                    smdownload ( image['ArchivedUri'],
                                 filename,
                                 image['Date'])
                    logger.info('Downloaded ' + filename)
                except:
                    logger.warning(image['Uri'])
                    logger.critical(json.dumps(image, sort_keys=True, indent=4, separators=(',', ': ')))
                    sys.exit(filename)
    return 0
                    
def process_node_folder(node_folder,depth=0,dirname=''):
    #
    # A SmugMug Folder can contain other Folders or Albums, which are retrived as a list of ChildNodes
    #
    basedir = dirname

    # l = logger()
    indent = '\t' * depth

    # Check that this is a Node and that the Node contains a Folder
    assert 'Node' in node_folder.OBJECT;
    node_type = node_folder.getType()
    assert node_type == "Folder"
    
    try:
        childnodes_uri = node_folder.getUris()['ChildNodes']['Uri']
    except:
        logger.error(json.dumps(node_folder.NODE, sort_keys=True, indent=4, separators=(',', ': ')))
        sys.exit("ugh - child nodes")

    # There may be alot of child nodes.  Let's group them together    
    all_nodes = get_all_nodes(childnodes_uri)
        
    if all_nodes is None:
        return

    #l.debug(json.dumps(all_nodes, sort_keys=True, indent=4, separators=(',', ': ')))
    num_children = len(all_nodes)
    logger.debug("Processing " + str(num_children) + " child nodes")
    count = 0
    for childnode in all_nodes:
        count = count + 1
        type = childnode['Type']
        
        if type == "Album":
            #dirname = basedir + childnode['UrlName'] + "/"
            albumname = re.sub('[/]', '', childnode['Name'])
            dirname = basedir + albumname + "/"
            logger.info(type + " " + dirname)
            mkdir(dirname,childnode['DateAdded'])
            # We have a node and not an album
            album_uri = childnode['Uris']['Album']['Uri']
            album = Album(album_uri)
            #l.info(album_uri)
            process_album(album,dirname)
        elif type == "Node":
            # dirname = basedir + childnode['UrlName'] + "/"
            dirname = basedir + childnode['Name'] + "/"
            #l.info(type + " " + dirname)
            if not os.path.isdir(dirname):
                mkdir(dirname,childnode['DateAdded'])
            node = Node(childnode['Uri'])
            node_recurse(node,depth+1,dirname)
        elif type == "Folder":
            folder = Node(childnode['Uri'])
            dirname = basedir + childnode['UrlName'] + "/"
            #l.info(type + " " + dirname)
            # dirname = basedir + childnode['Name'] + "/"
            if not os.path.isdir(dirname):
                mkdir(dirname,folder.getDateAdded())
            process_node_folder(folder,depth+1,dirname)
        else:
            logger.warning(indent + type + " '" + childnode['Name'] + "' (UNKNOWN)")
            
def process_node_album(node_album,depth=0,dirname=''):
    # l = logger()
    indent = '\t' * depth

    assert 'Node' in node_album.NODE;
    node_type = node_album.getType()
    assert node_type == "Album"

    logger.debug(dirname + " " + node_album.getType() + " " + node_album.getUrlName())
    album = process_uri(node_album.getUris()['Album']['Uri'])
    process_album(album,dirname)

def node_recurse(node,depth=0,dirname=''):
    # l = logger()

    node_uri = node.getUri()
    
    logger.debug(dirname + " " + node_uri + " " + str(depth))
    indent = '\t' * depth
    
    if node.getType() == "Folder":
        dirname = dirname + node.getUrlName() + "/"
        if not os.path.isdir(dirname):
            mkdir(dirname,node.getDateAdded())
        process_node_folder(node,depth,dirname)
    elif node.getType() == "Album":
        if not os.path.isdir(dirname):
            mkdir(dirname,node.getDateAdded())
        process_node_album(node,depth,dirname)
    else:
        logger.warning(node.getType() + " " + node.getUrlName())
    
def get_all_nodes(node_uri):
    #l = logger()

    api_nodes = process_uri(node_uri)
    if not 'Node' in api_nodes:
        return None

    nodes = api_nodes['Node']
    try:
        while ('NextPage' in api_nodes['Pages']):
            node_uri = api_nodes['Pages']['NextPage']
            api_nodes = process_uri(node_uri)
            logger.debug("Appending " + str(len(api_nodes['Node'])) + " to " + str(len(nodes)))
            nodes = nodes + api_nodes['Node']
    except:
        logger.error(json.dumps(api_nodes, sort_keys=True, indent=4, separators=(',', ': ')))
        logger.error(str(api_nodes['Code']) + " - " + api_nodes['Message'])
        
    #logger.warn(node_uri + " has " + str(len(nodes)) + " children")
    return nodes
