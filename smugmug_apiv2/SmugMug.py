#!/usr/bin/env python3

import os
import sys
import json
import logging

from smugmug_apiv2.utils import create_logger, get_service, get_tokens, authorize, process_uri

from smugmug_apiv2.User import User
from smugmug_apiv2.Node import Node

class SmugMug:
    'Common base class for all SmugMug classes'
    
    def __init__(self):
        # print ("Logging to " + args.logfile)
        logger = logging.getLogger('SmugMugClone')

        service = get_service()
        at, ats = get_tokens(os.environ["HOME"] + '/.smugmug')

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

        self.User = User()
