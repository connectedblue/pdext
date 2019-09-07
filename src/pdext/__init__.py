"""
Expose pdext functionality to users

Standard way to access extensions is by
    from pdext import *

and extensions can then be accessed through a dataframe df by
    df.ext.some_extension(...)

A new extension function func can be added via
    pd.add_extension(func)
"""

# Import libraries as standard shortcuts
import pandas as pd
import numpy as np

# get module constants
from .symbols import __pd_ext__, __df_ext__, __version__, __git_version__

# Configure the repository at the pandas level
from .extension_repository import extension_repository
setattr(pd, __pd_ext__, extension_repository())

# configure extensions on dataframes
from .register_extensions import *

# The recommended way to call the package is 
#    from pdext import *
# Expose the following symbols when called this way
__all__ =  ['pd', 'np',
            '__pd_ext__', '__df_ext__', 
            '__version__', '__git_version__']