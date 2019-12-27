import importlib
import pytest

# pick out some useful constants from the package
# so that tests don't have to re-written if they change
_sym = importlib.import_module('_pandex.symbols')

@pytest.fixture
def sym():
    class symbols:
        pd_ext = _sym.pd_ext
        df_ext = _sym.df_ext
        repository =  _sym.repository
        __import_file_ext__ = _sym.__import_file_ext__
        __import_file_sep__ = _sym.__import_file_sep__
        __import_file_line_spec__ = _sym.__import_file_line_spec__
        __install_timestamp_fmt__ = _sym.__install_timestamp_fmt__

        __pdext__ = _sym.__pdext__
        __version__ = _sym.__version__
        __pd_ext__ = _sym.__pd_ext__
        __df_ext__ = _sym.__df_ext__
        __default_collection__ = _sym.__default_collection__
        __installed_extensions__ = _sym.__installed_extensions__
    
    yield symbols
        