"""
Set up extension namespace and create shortcts
"""
from functools import wraps
import inspect

import pandas as pd

from ._extension_factory import create_shortcuts
from .symbols import __df_ext__, repository

@pd.api.extensions.register_dataframe_accessor(__df_ext__)
class ExtensionManager(object):
    def __init__(self, pandas_obj):
        self._obj = pandas_obj
       
    def __getattr__(self, func):
        if repository().is_extension(func):
            func = repository().get_extension_function(func)
            if hasattr(func, '__call__'):
                @wraps(func)
                def extension(*args, **kwargs):
                    result = func(self._obj, *args, **kwargs)
                    return result
                self._update_func_doc(extension)
                return extension
        else:
            return self.__getattribute__(func)
    
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
