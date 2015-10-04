#!/usr/bin/env python3

from smugmug_apiv2.utils import process_uri
from smugmug_apiv2 import User

# Implement interface documented at https://api.smugmug.com/api/v2/doc/reference/user-profile.html
#
# A user profile is the data provided by a user to establish that user's public presence.
# This may include social networking links, biographical text, and bio and cover images.

def profile(user = None):
    # https://api.smugmug.com/api/v2/user/cmac!profile
    return process_uri("/api/v2/" + (User.NICKNAME if user == None else user) + "!profile")
    
def BioImage(nickname = None): return User.BioImage(nickname)
def CoverImage(nickname = None): return User.CoverImage(nickname)
def User(nickname = None): return User.Generic("",nickname)
