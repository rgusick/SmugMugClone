#!/usr/bin/env python3
from rauth import OAuth1Session
import sys,json,os,logging,urllib.parse
from urllib.parse import urlparse,parse_qs
from common import API_ORIGIN, get_service, add_auth_params

session = None

def authorize(consumer_key,consumer_secret,access_token,access_token_secret):
    global session
    session = OAuth1Session(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token=access_token,
            access_token_secret=access_token_secret)
    return session

def logger_dir(logfilename):
    # Reverse order of priority
    candidates = [ "/var/log" , "/usr/local/log" , os.environ["HOME"] , "." , "/tmp" ]
    ret = logfilename
    for logdir in reversed(candidates):
        # W_OK is for writing, R_OK for reading, etc.
        logfile = logdir + "/" + logfilename
        if (os.access(logdir, os.W_OK)):
            ret = logfile
            
    print("Logging to " + ret)
    return ret
    
def create_logger(filename):
    # create logger
    global logger

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # create file handler which logs even debug messages
    fh = logging.FileHandler(logger_dir(filename), mode='w')
    fh.setLevel(logging.DEBUG)

    # create console handler with a higher log level
    # ch = logging.StreamHandler(stream=sys.stdout)
    # ch.setLevel(logging.WARN)

    # create formatter and add it to the handlers
    formatter_fh = logging.Formatter('[%(asctime)s] ' +
                                     '%(levelname)s ' +
                                     '(%(filename)s:%(lineno)s) ' +
                                     '%(message)s',
                                     datefmt='%Y-%m-%d %H:%M:%S')
    # formatter_ch = logging.Formatter('(%(filename)s:%(lineno)s) ' +
    #				  '%(message)s')
    fh.setFormatter(formatter_fh)
    # ch.setFormatter(formatter_ch)

    # add the handlers to the logger
    # logger.addHandler(ch)
    logger.addHandler(fh)

    return logger

def get_tokens(filename):
    try:
        with open(filename) as data_file:
            at, ats = json.load(data_file)
    except:
        """This example interacts with its user through the console, but it is
        similar in principle to the way any non-web-based application can obtain an
        OAuth authorization from a user."""
        service = get_service()
        
        # First, we need a request token and secret, which SmugMug will give us.
        # We are specifying "oob" (out-of-band) as the callback because we don't
        # have a website for SmugMug to call back to.
        rt, rts = service.get_request_token(params={'oauth_callback': 'oob'})

        # Second, we need to give the user the web URL where they can authorize our
        # application.
        auth_url = add_auth_params(
            service.get_authorize_url(rt), access='Full', permissions='Modify')
        print('Go to %s in a web browser.' % auth_url)

        # Once the user has authorized our application, they will be given a
        # six-digit verifier code. Our third step is to ask the user to enter that
        # code:
        sys.stdout.write('Enter the six-digit code: ')
        sys.stdout.flush()
        verifier = sys.stdin.readline().strip()
        
        # Finally, we can use the verifier code, along with the request token and
        # secret, to sign a request for an access token.
        at, ats = service.get_access_token(rt, rts, params={'oauth_verifier': verifier})

        with open(filename, 'w') as outfile:
            json.dump([at, ats], outfile, sort_keys=True,indent=4, separators=(',', ': '))
        
    return at, ats

def split_uri(uri):
    # Convert querystring in URI to a parameter
    logger.debug(uri)
    o = urlparse(uri)
    qs = o.query
    q = parse_qs(qs)
    return(o.path,q)

def process_uri(uri):
    base_uri,querystring = split_uri(uri)

    data = session.get(
        API_ORIGIN + base_uri,
        params=querystring,
        headers={'Accept': 'application/json'}).json()

    # Check the results
    for key in ['Code','Message','Response']:
        if not key in data:
            logger.error(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))
            raise ValueError("Result of " + uri + " didn't contain a '" + key + "'")

    if data['Code'] != 200:
        logger.error(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))
        raise ValueError("Result of " + uri + " is code " + data['Code'])
        
    return data['Response']

def get_all_nodes(node_uri):
    api_nodes = process_uri(node_uri)
    if 'Node' in api_nodes:
        nodes = api_nodes['Node']
    else:
        logger.fatal(json.dumps(api_nodes, sort_keys=True, indent=4, separators=(',', ': ')))
        sys.exit(node_uri)
    try:
        while ('NextPage' in api_nodes['Pages']):
            node_uri = api_nodes['Pages']['NextPage']
            api_nodes = process_uri(node_uri)
            logger.debug("Appending " + str(len(api_nodes['Node'])) + " to " + str(len(nodes)))
            nodes = nodes + api_nodes['Node']
    except:
        logger.error(str(api_nodes['Code']) + " - " + api_nodes['Message'])

    #logger.warn(node_uri + " has " + str(len(nodes)) + " children")
    return nodes

def get_all_images(albumimage_uri):
    api_albumimage = process_uri(albumimage_uri)
    try:
        images = api_albumimage['AlbumImage']
    except:
        logger.debug(json.dumps(api_albumimage, sort_keys=True, indent=4, separators=(',', ': ')))
        images = []
        
    try:
        while ('NextPage' in api_albumimage['Pages']):
            albumimage_uri = api_albumimage['Pages']['NextPage']
            api_albumimage = process_uri(albumimage_uri)
            images = images + api_albumimage['AlbumImage']
    except:
        logger.error("No Images " + API_ORIGIN + albumimage_uri)
        # logger.error(json.dumps(api_albumimage, sort_keys=True, indent=4, separators=(',', ': ')))
        
    return images

def process_album(album_uri):
    api_album = process_uri(album_uri)
    
    
    try:
        albumimages_uri = api_album['Album']['Uris']['AlbumImages']['Uri']
    except:
        logger.error(json.dumps(api_album, sort_keys=True, indent=4, separators=(',', ': ')))
        sys.exit("Oh no")
        
    images = get_all_images(albumimages_uri)
    for image in images:
        try:
            logger.info("\t\t\t" + image['FileName'])
        except:
            logger.warn(len(images))
            logger.error(json.dumps(image, sort_keys=True, indent=4, separators=(',', ': ')))
            
    return 0
                    
def node_recurse(node_uri,depth):
    global logger
    
    logger.debug(node_uri + " " + str(depth))
    indent = '\t' * depth

    api_node = process_uri(node_uri)

    try:
        childnodes_uri = api_node['Node']['Uris']['ChildNodes']['Uri']
    except:
        logger.error(json.dumps(api_node, sort_keys=True, indent=4, separators=(',', ': ')))
        sys.exit("ugh")
        
    all_nodes = get_all_nodes(childnodes_uri)

    # Process Albums first
    logger.debug("Processing " + str(len(all_nodes)) + " nodes")
    count = 0
    for childnode in all_nodes:
        try:
            count = count + 1
            #logger.info(str(count) + " " + childnode['Type'] + " '" + childnode['Name'] + "' " + childnode['Uri'])
            if childnode['Type'] == "Album":
                logger.info(indent + childnode['Type'] + " '" + childnode['Name'] + "'")
                # We have a node and not an album
                album_uri = process_uri(childnode['Uri'])['Node']['Uris']['Album']['Uri']
                process_album(album_uri)
            else:
                logger.debug(indent + childnode['Type'] + " '" + childnode['Name'] + "' skip")
        except:
            logger.error(json.dumps(childnode, sort_keys=True, indent=4, separators=(',', ': ')))
            sys.exit("WTF")
            
    count = 0
    for childnode in all_nodes:
        #try:
            count = count + 1
            logger.debug(count)
            #logger.info(json.dumps(childnode, sort_keys=True, indent=4, separators=(',', ': ')))
            if childnode['Type'] == "Folder":
                logger.info(indent + childnode['Type'] + " '" + childnode['Name'] + "'")
                node_recurse(childnode['Uri'],depth+1)
            else:
                logger.debug(indent + childnode['Type'] + " '" + childnode['Name'] + "' skip")
        #except:
        #    logger.error(node_uri)
        #    logger.error(json.dumps(all_nodes, sort_keys=True, indent=4, separators=(',', ': ')))
        #    logger.error(json.dumps(childnode, sort_keys=True, indent=4, separators=(',', ': ')))
        #    sys.exit("WTF")
            
def folder_recurse(albums_uri,folders_uri,depth):
    # Deprecated
    # logger.info(albums_uri + " " + folders_uri + " " + str(depth))
    indent = '\t' * depth
    logger.info(albums_uri);
    logger.info(folders_uri);
    
    api_folderalbums = process_uri(albums_uri)
    api_userfolders = process_uri(folders_uri)

    # 1) Dump the list of albums
    # 2) Traverse the sub folders
    
    # logger.info(albums_uri)
    #logger.info(json.dumps(api_folderalbums, sort_keys=True, indent=4, separators=(',', ': ')))
    try:
        for album in api_folderalbums['Album']:
            logger.info(indent + "'" + album["Name"] + "' "+ str(album["ImageCount"]))
            logger.info(json.dumps(album, sort_keys=True, indent=4, separators=(',', ': ')))
    except KeyError:
        logger.debug(indent + "No albums")
    
    # logger.info(indent + folders_uri)
    try:
        for folder in api_userfolders['Folder']:
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
