#!/usr/bin/env python3

from smugmug_apiv2.utils import process_uri
from smugmug_apiv2 import User

# A node is a folder, album, or page. Folders contain albums, pages, and other folders, and albums contain images.
# To browse a user's node hierarchy, you will typically start at the root by following the Node link from the User endpoint.

def GenericNode(function, node): return process_uri("/api/v2/node/" + node + ("!" + function if function != None else ""))

def ChildNodes(node): return GenericNode("children",node)
# FolderById
# HighlighImage
def ParentNode(node): return GenericNode("parent",node)
def ParentNodes(node): return GenericNode("parentnodes",node)
def User(nickname = None): return User.Generic("",nickname)
