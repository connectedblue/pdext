"""
Expose pdext functionality to users

Standard way to enable extensions is by
    import pdext as pd

and extensions can then be accessed through a dataframe df by
    df.ext.some_extension(...)

A new extension function func can be added via
    pd.ext.import_extension('path/to/extension -> ext_name')
"""
# Import libraries as standard shortcuts
import sys
import pandas as pd

# get module constants
from .symbols import __pd_ext__, __pdext__

# Configure the repository at the pandas level
from .repository import ExtensionRepository
setattr(pd, __pd_ext__, ExtensionRepository())

# configure extensions on dataframes
from .extensions import ExtensionManager

# configure the extension importer
from .extensions import ExtensionImporter
sys.meta_path.append(ExtensionImporter())

# Add this module with an _ in front of the name
# (enables the test suite to access some functions in the module)
sys.modules['_'+__name__] = sys.modules[__name__]

# Substitute this module for the pandas module
# configured with extension capability
sys.modules[__name__] = pd

