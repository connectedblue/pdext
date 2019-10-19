import os, shutil, tempfile
import pytest

from contextlib import contextmanager

# pick out some useful constants from the package
# so that tests don't have to re-written if they change
import pdext.symbols as sym

#### HELPER FUNCTIONS USED IN FIXTURES

# Create some temporary directories valid for a session and module
@pytest.fixture(scope='session')
def temp_session_directory():
    tmp_dir = tempfile.mkdtemp()
    yield tmp_dir
    shutil.rmtree(tmp_dir)

@pytest.fixture(scope='module')
def temp_module_directory():
    tmp_dir = tempfile.mkdtemp()
    yield tmp_dir
    shutil.rmtree(tmp_dir)



# A context manager that takes care of safely saving the current
# repository definition and restoring it when the test fixture
# is complete.  Enables test repos and extensions to be configured
# without polluting user or other shared repos 
@contextmanager
def save_current_installed_extensions():
    # save any existing config file to a temporary file
    if os.path.isfile(sym.__installed_extensions__):
        f, tmp_file = tempfile.mkstemp()
        shutil.move(sym.__installed_extensions__, tmp_file)
        yield 
        # restore original file and rebuild the collections
        shutil.move(tmp_file, sym.__installed_extensions__)
        sym.pd_ext()._build_extension_collections()
    else:
        # copy the backup version of the config file and try again
        shutil.copy(sym.__installed_extensions__+'.save', sym.__installed_extensions__)
        save_current_installed_extensions()


def make_test_repos(repo, root_dir):
    """
    Create two repositories which can be used to install extensions
    into during tests
    Name of repos are test1 and test2
    """
    # Create a number of test repos
    test_dirs = {'test1': \
                os.path.join(root_dir,'session_test_pdext1'),
                'test2': \
                os.path.join(root_dir,'session_test_pdext2'),
                }
    # Add them so that the initial default search path is 
    # in the order above
    test_dirs = {k:test_dirs[k] for k in reversed(list(test_dirs.keys()))}
    for name, dir in test_dirs.items():
        #adding a test location should recreate the directory
        repo.add_repository(name, dir)
    # make sure that the user directory is removed
    repo.default_repository = 'test1'
    repo.remove_repository('user')

    return test_dirs

