#!/usr/bin/env python3
from rauth import OAuth1Session
import sys
import json
import os
import logging
import urllib.parse
from urllib.parse import urlparse,parse_qs
from common import API_ORIGIN, get_service, add_auth_params

#session = None

def session():
    return session

def logger():
    global logger
    return logger

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
    
    logger = logging.getLogger(filename)
    logger.setLevel(logging.DEBUG)

    # create file handler which logs even debug messages
    fh = logging.FileHandler(logger_dir(filename), mode='w')
    fh.setLevel(logging.DEBUG)

    # create console handler with a higher log level
    # ch = logger().StreamHandler(stream=sys.stdout)
    # ch.setLevel(logger().WARN)

    # create formatter and add it to the handlers
    formatter_fh = logging.Formatter('[%(asctime)s] ' +
                                     '%(levelname)s ' +
                                     '%(funcName)s ' +
                                     '(%(filename)s:%(lineno)s) ' +
                                     '%(message)s',
                                     datefmt='%Y-%m-%d %H:%M:%S')
    # formatter_ch = logger().Formatter('(%(filename)s:%(lineno)s) ' +
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

