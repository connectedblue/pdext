import pandas as pd
import numpy as np

class meta_main(object):
    """
    Integrated into main metaext extension class.
    """
    def _initialise(self):
        self.clear()
    
    def clear(self):
        self._meta = {}
    
    
    def add(self, key, value=None):
        if type(key)==dict:
            for k,v in key.items():
                self._meta[k] = v
        else:
            self._meta[key] = value
            
    def get(self, key):
        return self._meta[key]
    
    def get_meta_dict(self):
        return self._meta
        
    def add_key(self, column):
        if column not in self._obj.columns:
            raise Exception('Column {} not present'.format(column))
        self.add_meta('key', column)
        
        