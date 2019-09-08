import pytest

from pdext import *

from test_data import *


def test_register_single_extension():
    # register the extension function
    repository().add_extension(extension_function)
    # check function has been saved inside package
    extfile = repository()._extension_file_name('extension_function')
    with open(extfile, 'r') as test_contents:
        assert 'def extension_function(df, value=0):' in \
                    test_contents.read()


def test_single_extension_function(df_A):
    # call the extension function and check it has
    # done its job
    df_ext(df_A).extension_function(4)
    assert 'new_col' in df_A.columns
    assert df_A.new_col.sum() == 4*df_A.shape[0]

def test_extension_documentation(df_A):
    usage = 'USAGE: df.{}.extension_function(value)'.format(__df_ext__) 
    assert usage in df_ext(df_A).extension_function.__doc__

def test_remove_extension(df_A):
    # If the function is removed from the registry
    # then calling it again should raise an AttributeError
    repository().clear()
    with pytest.raises(AttributeError):
        df_ext(df_A).extension_function(4)

def test_load_extensions_from_package(df_A):
    # The extension function should still be saved in the package
    # try to load it after the clearing above
    repository().load_extensions()
    df_ext(df_A).extension_function(5)
    assert 'new_col' in df_A.columns
    assert df_A.new_col.sum() == 5*df_A.shape[0]



if __name__ == '__main__':
    repository().add_function(extension_function)            




