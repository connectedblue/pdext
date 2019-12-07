"""
Set up extension namespace and create shortcts
"""
from functools import wraps, reduce
import inspect

import pandas as pd

from ..symbols import __df_ext__, repository, __default_collection__
from .collection import ExtensionCollection

@pd.api.extensions.register_dataframe_accessor(__df_ext__)
class ExtensionManager(object):
    def __init__(self, pandas_obj):
        self._obj = pandas_obj
       
    def __getattr__(self, collection):
        if collection not in repository().extension_collections:
            extensions = ExtensionCollection(self._obj, 
                        repository().extension_collections[__default_collection__])
            return getattr(extensions, collection)
        
        return ExtensionCollection(self._obj, 
                        repository().extension_collections[collection])
    