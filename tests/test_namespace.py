import os
import pytest

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
    # test that pd namespace is present and it is pandas!
    from pdext import pd
    assert 'pd' in locals()
    assert hasattr(pd, 'DataFrame') == True

    # and also the extension namespace is configured
    assert hasattr(pd, __test_pd_ext__) == True

    # Check key constants available in package
    import pdext
    assert hasattr(pdext, '__df_ext__') == True
    assert hasattr(pdext, '__pd_ext__') == True
    assert pdext.__df_ext__ == __test_df_ext__
    assert pdext.__pd_ext__ == __test_pd_ext__   
        



