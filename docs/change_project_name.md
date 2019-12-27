# Steps for changing the name of the project

This is something that will have to be done rarely (if at all) going forward.  A use case might be
if there was a released version on pyPI that had different features, for example.

These steps ensure that the package compiles to the new name and also the
documentation auto generates.

1. Change `__pdext__` in the `symbols.py` file.
    * Documentation should auto generate after this step

2. A number of steps to get project to install and tests to pass
    * Change project directory name under `src`
    * change imports in `setup.py`
    * Update `MANIFEST.in`
    * Update bits of `Makefile`:
        * `PACKAGE`
        * `PKG_LIB`  (also `mkdir` the new tarball directory)
    * Update `testrepos.py`, `helpers.py`, `testdataframes.py`, `symbols.py` in `fixtures`
    * Update import in tests:
        * test_import_namespaces (in test_namespace.py)

3. Update imports in doc:
    * `conf.py` 
    * in the `autoclass` directives in `reference.rst`

4. Manually update main `README.md`

5. Decide whether to update the demo repo name or not.  If
   yes, then additional changes will be needed (document 
   below if and when this is done)

