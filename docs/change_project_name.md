# Steps for changing the name of the project

This is something that will have to be done rarely (if at all) going forward.  A use case might be
if there was a released version on pyPI that had different features, for example.

These steps ensure that the package compiles to the new name and also the
documentation auto generates.

1. Change `__pdext__` in the `symbols.py` file.
    * Documentation should auto generate after this step


2. A number of steps to get project to install and tests to pass
    * Change project directory name under `src`
    * change imports and version location in `setup.py`
    * change `setup.cfg` and re-run `versioneer`
    * remove stuff added to `__init__.py` by `versioneer`
    * Update `MANIFEST.in`
    * Update bits of `Makefile`:
        * `PACKAGE`
        * `PKG_LIB`  (also `mkdir` the new tarball directory)
    * Update `testrepos.py`, `helpers.py`, `testdataframes.py` in `fixtures`
    * Update imports on following tests:
        * `test_import_extension.py`
        * `test_install_from_github.py`
        * `test_multi_collections.py`
        * `test_pdext_install_extension.py`
        * `test_remove_enable_disable_extensions.py`
        * `test_repo_install_extension.py`
        * `test_show_extension.py`
        * `test_repository_location.py`
    * Update import in tests:
        * test_import_namespaces (in test_namespace.py)

3. Update imports in doc:
    * `conf.py` 
    * in the `autoclass` directives in `reference.rst`

4. Manually update main `README.md`

5. Decide whether to update the demo repo name or not.  If
   yes, then additional changes will be needed (document 
   below if and when this is done)

