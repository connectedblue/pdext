# Define some standard dataframe content that can
# be used across tests
import pytest, importlib
from pandex.symbols import pd_ext, __pdext__
pd = importlib.import_module(__pdext__)

def test_dataframe(data):
    # Pick up currently defined extensions

    pd_ext()._build_extension_collections()
    return pd.DataFrame(data)

@pytest.fixture
def df_A():
    data = {'letters': ['a', 'b', 'c'],
            'numbers': [ 1,   2,   3]}
    return test_dataframe(data)

@pytest.fixture
def df_X():
    data = {'letters': ['x', 'y', 'z'],
            'numbers': [ 7,   8,   9]}
    return test_dataframe(data)


