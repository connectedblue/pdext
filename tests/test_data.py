import pytest

from pdext import *

# pick out some useful constants from the package
# so that tests don't have to re-written if they change
import pdext.symbols as sym

def repository():
    """
    This is the location of the extension repository
    """
    return sym.repository()

def df_ext(df=None):
    """
    This is where the extension functions on a dataframe can be 
    found
    """     
    return sym.df_ext(df)      


def extension_function(df, value=0):
    """
    Extension function which adds a new column with constant
    value passed in.
    This is the format which a user will use
    """
    df['new_col'] = value

# Define some standard dataframe content that can
# be used across tests
@pytest.fixture
def df_A():
    data = {'letters': ['a', 'b', 'c'],
            'numbers': [ 1,   2,   3]}
    return pd.DataFrame(data)

@pytest.fixture
def df_X(scope='test'):
    data = {'letters': ['x', 'y', 'z'],
            'numbers': [ 7,   8,   9]}
    return pd.DataFrame(data)


