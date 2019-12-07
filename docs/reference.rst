Reference Guide
===============

Extensions can be managed directly from within the
|``pd.ext``| namespace.  This page describes the
functions available.


Repository Management
---------------------

.. autoclass:: pandex.ext.ExtensionRepository
   :members:  import_extension,
              show_extensions, enable_extension, 
              reinstall_extension, remove_extension

   .. automethod:: disable_extension(name)



``import`` statement
--------------------

An alternative way is provided to install and manage multiple extensions
in one go.  This is useful, for example, to minimise the number of downloads
when extensions are hosted on remote sites like GitHub.

.. autoclass:: pandex.ext.ExtensionImporter
