#!/usr/bin/env python3

import sys
import json
import os
import logging

from smugmug_apiv2.utils import create_logger, get_service, get_tokens, authorize, process_uri
from smugmug_apiv2.tools import node_recurse

from smugmug_apiv2 import User
from smugmug_apiv2 import UserProfile
from smugmug_apiv2 import Node
from smugmug_apiv2 import Album

def main():
    logger = create_logger("smugmug.log")

    service = get_service()
    at, ats = get_tokens(os.environ["HOME"] + '/.smugmug.json')

    # The access token we have received is valid forever, unless the user
    # revokes it.  Let's make one example API request to show that the access
    # token works.
    logger.info('Access token: %s' % at)
    logger.info('Access token secret: %s' % ats)

    authorize(
        service.consumer_key,
        service.consumer_secret,
        access_token=at,
        access_token_secret=ats)
    
    api_authuser = User.authuser()
    bio = User.BioImage()
    
    user = api_authuser['User']['NickName']
    uri = api_authuser['User']['Uri']
    node_uri = api_authuser['User']['Uris']['Node']['Uri']

    logger.info("User=" + user)
    logger.info("Uri=" + uri)

    node_recurse(node_uri)
    
if __name__ == '__main__':
    main()
