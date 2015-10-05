#!/usr/bin/env python3

from smugmug_apiv2.utils import process_uri
from smugmug_apiv2 import User

def GenericImage(function, image): return process_uri("/api/v2/image/" + node + ("!" + function if function != None else ""))


