import pandas as pd
import numpy as np

## When adding new wrapper functions, the original function must point
## to the functions here after the extension classes are all loaded.  
## This is done in the custom_shortcuts script

pd.__pdwrapper_copy = pd.DataFrame.copy

class _pdwrapper_copy(object):
    """
    PP extension methods which override functions provided in the main
    pandas package

    Integrated into main pdwrapper namespace.
    """
    
    def copy(self, *args, **kwargs):
        """
        A wrapper around the standard dataframe copy() method
        to also copy across the meta data from self
        """
        df = getattr(pd, '__pdwrapper_copy')(self, *args, **kwargs)
        df.meta.add(self.meta.get_meta_dict())
        return df
        