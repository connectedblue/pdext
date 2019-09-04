import pytest

from pdext import *

from test_data import A_test_df


@pytest.mark.parametrize('namespace, does_exist',[
    ('meta', True), ('pplab', True), ('_pdwrapper', True), ('not_ext', False)
])
def test_builtin_namespace(namespace, does_exist):
    df = A_test_df()
    assert hasattr(df,namespace) == does_exist



