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
import sys
import pandas as pd

# get module constants
from .symbols import __pd_ext__, __df_ext__, __version__, __git_version__

# Configure the repository at the pandas level
from .repository import ExtensionRepository
setattr(pd, __pd_ext__, ExtensionRepository())

# configure extensions on dataframes
from .extensions import ExtensionManager

# configure the extension importer
from .extensions import ExtensionImporter
sys.meta_path.append(ExtensionImporter())

# The recommended way to call the package is 
#    from pdext import pd
# Expose the following symbols when called using *
__all__ =  ['pd',]
