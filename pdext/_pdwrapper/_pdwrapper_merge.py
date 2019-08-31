import pandas as pd
import numpy as np

## When adding new wrapper functions, the original function must point
## to the functions here after the extension classes are all loaded.  
## This is done in the custom_shortcuts script

pd.__pdwrapper_merge = pd.DataFrame.merge

# Do the standard merge by default.  If the user sets this
# attribute, then safe merge is performed
pd.safe_merge = False

class _pdwrapper_merge(object):
    """
    PP extension methods which override functions provided in the main
    pandas package

    Integrated into main pdwrapper namespace.
    """
    
    def merge(self, *args, **kwargs):
        """
        A wrapper around the standard dataframe copy() method
        to also copy across the meta data from self
        """
        if pd.safe_merge and kwargs['how']=='left':
            kwargs['validate'] = 'm:1'
        
        return getattr(pd, '__pdwrapper_merge')(self, *args, **kwargs)
        
"""        
Need to turn these scripts into proper unit test


from pp import *
x=pd.DataFrame({'a':[1,2,3,4], 'b':[11,12,13,14]})
x.meta.add('api_key', 34)
y=x.copy()
y.meta.get_meta_dict()

y=pd.DataFrame({'a':[1,2,2,4], 'b':[21,22,23,24]})
x.merge(y, how='left', on='a')

pd.safe_merge = True

"""