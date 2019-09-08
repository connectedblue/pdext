import os
import pytest

from pdext import *
import pdext

from test_data import *


## NB: if the extension constants ever change, the hard-coded strings
## only need to be changed in this test file.  All other tests should
## use the convenience symbols imported directly from the package

__test_df_ext__ = 'ext'
__test_pd_ext__ = 'ext'

@pytest.mark.parametrize('namespace, does_exist',[
    (__test_df_ext__, True), ('no_ext', False),
])
def test_df_namespace(namespace, does_exist, df_A):
    if does_exist:
        getattr(df_A, namespace)
    else:
        with pytest.raises(AttributeError):
            getattr(df_A, namespace)

def test_import_namespaces():
    # test that pd and np namespaces are present
    pd.DataFrame
    np.where

def test_pd_namespace():
    getattr(pd, __test_pd_ext__)

def test_pdext_constants():
    assert pdext.__df_ext__ == __test_df_ext__
    assert pdext.__pd_ext__ == __test_pd_ext__
    

def test_installed_extension_dir_present():
    assert os.path.isdir(sym.__installed_extensions__)
        
        



