"""
A container object to manage a group of extensions under the
same namespace (called a collection) for a particular dataframe
"""
from functools import wraps
import inspect

import pandas as pd


class ExtensionCollection(object):
    def __init__(self, df, extensions):
        """
        This class is instantiated with a particular dataframe and
        a set of extension functions
        Input:
            df -- the dataframe object that the extensions will operate
                  on
            extensions -- a dictionary of the form:L
                            {extension_name: extension_func_object}
        """
        # Save the dataframe that the collection was instantiated with
        self.df = df
        self.extensions = extensions
       
    def __getattr__(self, func):
        """
        Any attribute call to this object is to retrieve an extension
        """
        if func in self.extensions:
            func = self.extensions[func]
            @wraps(func)
            def extension(*args, **kwargs):
                result = func(self.df, *args, **kwargs)
                return result
            self._update_func_doc(extension)
            return extension
        else:
            raise AttributeError('{} is not a valid extension'.format(func))
    
    @staticmethod
    def _update_func_doc(func):
        func_name = func.__name__
        sig = inspect.signature(func)
        doc = func.__doc__
        params = list(sig.parameters)
        first_arg = params[0]
        other_args = ', '.join(params[1:])
        args = first_arg + other_args
        doc += '\nUSAGE: {first_arg}.ext.{func_name}({other_args})'\
                .format(first_arg=first_arg,
                        func_name=func_name,
                        other_args=other_args)
        func.__doc__ = doc
