#!/usr/bin/env python3

class Uri:
    'Implement interface documented at https://api.smugmug.com/api/v2/doc/reference/user.html'

    def __init__(self, dictionary):
        self.Uri = dictionary['Uri'] if 'Uri' in dictionary else None
        self.UriDescription = dictionary['UriDescription'] if 'UriDescription' in dictionary else None
        self.EndpointType = dictionary['EndpointType'] if 'EndpointType' in dictionary else None
        self.Locator = dictionary['Locator'] if 'Locator' in dictionary  else None
        self.LocatorType = dictionary['LocatorType'] if 'LocatorType' in dictionary else None

    def getUri(self): return self.Uri
    def getUriDescription(self): return self.UriDescription
    def getEndpointType(self): return self.EndpointType
    def getLocator(self): return self.Locator
    def getLocatorType(self): return self.LocatorType
