"""
module level constants
"""

# Namespace at the pandas top level module where
# extensions are managed
__pd_ext__ = 'ext'

# Namespace at the dataframe level where the extension
# functions are called
__df_ext__ = 'ext'


# Set the current version number
from ._version import get_versions
v = get_versions()
__version__ = v.get("closest-tag", v["version"])
__git_version__ = v.get("full-revisionid")
del get_versions, v

# return the pandas level reference where the repository is stored
def repository():
    import pandas as pd
    return getattr(pd, __pd_ext__)

# return a dataframe level reference from where the extensions
# are executed
def df_ext(df=None):
    if df is None:
        import pandas as pd
        df=pd.DataFrame()
    return getattr(df, __df_ext__)