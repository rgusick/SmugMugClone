#!/usr/bin/env python3

from smugmug_apiv2.utils import process_uri
from smugmug_apiv2 import User
from smugmug_apiv2 import Node

#You should only use this endpoint if you need to support older accounts that have not migrated to New SmugMug.
# If you only need New SmugMug support, use the Node endpoint instead.

# A folder can contain albums, pages, and other folders. The API URI for a folder contains the full path to that folder.

def GenericFolder(function, folder): return process_uri("/api/v2/folder/" + User.NICKNAME + "/" + folder + ("!" + function if function != None else ""))
