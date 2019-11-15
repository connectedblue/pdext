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
import numpy as np

# get module constants
from .symbols import __pd_ext__, __df_ext__, __version__, __git_version__

# Configure the repository at the pandas level
from .repository import ExtensionRepository
setattr(pd, __pd_ext__, ExtensionRepository())

# configure extensions on dataframes
from .register_extensions import ExtensionManager

# configure the extension importer
from .extension_importer import ExtensionImporter
sys.meta_path.append(ExtensionImporter())

# The recommended way to call the package is 
#    from pdext import *
# Expose the following symbols when called this way
__all__ =  ['pd', 'np',]
