import os

from .symbols import __default_collection__,\
                     __installed_extensions__

class extension(object):

    def __init__(self, name, collection=__default_collection__):
        """
        Create an extension container that mirrors how the user
        invokes the extension
        example:
            The user might call:
                df.ext.name(arg1, arg2 etc)
            or
                df.ext.collection.name(arg1, arg2 etc)
        
        Input:
            name -- string name of the extension
            collection -- optional namespace to prevent 
                          extension namespace clash
        """
        self.name = name
        self.collection = collection
        self._set_location()

    def add_files(self, *files):
        """
        Install files
        """
        pass

    def _set_location(self):
        """
        location is a sub directory structure underneath the
        __installed_extensions__ directory of the form
        __installed_extensions__/collection/extension

        If a directory doesn't already exist, make one
        """
        self.location = os.path.join(__installed_extensions__,
                                     self.collection,
                                     self.name)
        if not os.path.exists(self.location):
            os.makedirs(self.location)