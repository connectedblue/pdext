import pytest

from pdext import *

from test_data import *


def test_register_single_extension():
    # register the extension function
    repository().add_extension(extension_function)


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



if __name__ == '__main__':
    repository().add_function(extension_function)            




