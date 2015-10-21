#!/usr/bin/env python3

import os
import argparse

from smugmug_apiv2.utils import create_logger
from smugmug_apiv2.tools import node_recurse

from smugmug_apiv2.SmugMug import SmugMug
from smugmug_apiv2.Node import Node

def main():
    parser = argparse.ArgumentParser(description='Sync a SmugMug account to local disk')
    parser.add_argument("-d",'--download', default="/volume1/photo/smugmug/", help='SmugMug download dir')
    parser.add_argument("-l",'--logfile', default='~/smugmug.log', help='Logfile name')
    args = parser.parse_args()
    if args.download.endswith('/'):
        args.download = args.download[:-1]
    if not os.path.isdir(args.download):
        sys.exit(args.download + " is not a directory")
        
    logger = create_logger(args.logfile)

    # Initialize SmugMug object with credentials
    sm = SmugMug()

    # For convenience.  Could also use sm.User.BioImage(), etc
    user = sm.User
    
    # Just to see that we can...
    bio = user.getBioImage_dict()
    
    nickname = user.getNickName()
    uri = user.getUri()
    node_uri = user.getNode_uri()['Uri']
    node = Node(node_uri)

    logger.info("User=" + nickname)
    logger.info("Uri=" + uri)

    node_recurse(node, dirname=args.download )
    # node_recurse(node_uri, dirname=args.download )
    logger.info("Done!")
    
if __name__ == '__main__':
    main()
