"""
module level constants
"""
import os

# Get parameters generated when the package was built
from ._build_info import __version__
__pdext__ = 'pandex'

# Namespace at the pandas top level module where
# extensions are managed
__pd_ext__ = 'ext'

# Namespace at the dataframe level where the extension
# functions are called
__df_ext__ = 'ext'


# Name of collection that extensions are placed in if
# none specified by the user
__default_collection__ = '__no_collection'

# directory where extensions are stored is relative to the 
# location of this file
__installed_extensions__ = os.path.join(\
                                os.path.dirname(os.path.abspath(__file__)), 
                                'installed_extensions',
                                'locations.yml')

# Suffix for import extension files
__import_file_ext__ = '.pdext'
# seperator in import extension files
__import_file_sep__ = '->'
# extension spec line format
__import_file_line_spec__ = '{}{}{}'.format('{}',__import_file_sep__,'{}')

# format of install timestamp in __init__.py
__install_timestamp_fmt__ = '%Y-%m-%dT%H:%M:%SZ'


# return the pandas level reference where the repository is stored
def repository():
    import pandas as pd
    return getattr(pd, __pd_ext__)

# and an alternative name which is more intuitive
def pd_ext():
    return repository()

# return a dataframe level reference from where the extensions
# are executed
def df_ext(df=None):
    if df is None:
        import pandas as pd
        df=pd.DataFrame()
    return getattr(df, __df_ext__)