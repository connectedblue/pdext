"""
A container object to manage a group of extensions under the
same namespace (called a collection) for a particular dataframe
"""
from functools import wraps

import pandas as pd


class ExtensionCollection(object):
    def __init__(self, df, extensions):
        """
        This class is instantiated with a particular dataframe and
        a set of extension functions
        Input:
            df -- the dataframe object that the extensions will operate
                  on
            extensions -- a dictionary of the form:
                            {extension_name: Extension instance}
        """
        # Save the dataframe that the collection was instantiated with
        self.df = df
        self.extensions = extensions
       
    def __getattr__(self, func):
        """
        Any attribute call to this object is to retrieve an extension
        """
        if func in self.extensions:
            func = self.extensions[func].get_extension()
            @wraps(func)
            def extension(*args, **kwargs):
                result = func(self.df, *args, **kwargs)
                return result
            return extension
        else:
            raise AttributeError('{} is not a valid extension'.format(func))