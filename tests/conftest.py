import os, shutil
import pytest

# pick out some useful constants from the package
# so that tests don't have to re-written if they change
import pdext.symbols as sym
from pdext import pd

@pytest.fixture(scope='session')
def sessionrepo():
    # pick out some useful constants from the package
    # so that tests don't have to re-written if they change
    
    # Create a test repo for the whole duration of tests
    tmp_file = None
    if os.path.isfile(sym.__installed_extensions__):
        tmp_file = sym.__installed_extensions__+ '.session_save'
        os.rename(sym.__installed_extensions__, tmp_file)
    from pdext.repository import extension_repository
    test_repo = extension_repository()
    # Create a number of test repos
    test_dirs = {'test1':'/tmp/session_test_pdext1',
                 'test2':'/tmp/session_test_pdext2'}
    for name, dir in test_dirs.items():
        if os.path.exists(dir):
            shutil.rmtree(dir)
        #adding a test location should recreate the directory
        test_repo.add_location(name, dir)
    # make sure that the user directory is removed
    test_repo.default_repository = 'test1'
    test_repo.remove_location('user')
    
    yield test_repo
    ### At the end of session
    # restore the previous yaml file
    if tmp_file is not None:
        os.rename(tmp_file, sym.__installed_extensions__)
    for name, dir in test_dirs.items():
        shutil.rmtree(dir)

@pytest.fixture
def testpackage1():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                'testpackages', 'package1')


@pytest.fixture(scope='module')
def testrepo():
    
    # save any existing config file to a temporary name
    tmp_file = None
    if os.path.isfile(sym.__installed_extensions__):
        tmp_file = sym.__installed_extensions__+ '.module_save'
        os.rename(sym.__installed_extensions__, tmp_file)
    from pdext.repository import extension_repository
    yield extension_repository
    if tmp_file is not None:
        os.rename(tmp_file, sym.__installed_extensions__)




def df_ext(df=None):
    """
    This is where the extension functions on a dataframe can be 
    found
    """     

    return getattr(df, sym.__df_ext__)      


# Define some standard dataframe content that can
# be used across tests

def test_dataframe(data):
    # Pick up currently defined extensions
    pd.ext.build_extension_collections()
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


