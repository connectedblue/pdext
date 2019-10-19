# Define all fixtures to export in this dictionary
# They will also be automatically added to __all__

__exports = {
'.testrepos' : ['two_test_session_repos', 'no_repo_defined',
                'pdext_with_loaded_testpackages'],
'.testdataframes' : ['df_A', 'df_X'],
'.testextensions' : ['testpackage1', 'testpackage2', 'testpackage3'],
'.helpers' : ['temp_session_directory', 'temp_module_directory',
              'save_current_installed_extensions', 'make_test_repos'],
}

from importlib import import_module
__all__ = []

for mod, funcs in __exports.items():
    m = import_module(mod, package=__name__)
    for func in funcs:
        globals()[func] = getattr(m, func)
        __all__.append(func)
