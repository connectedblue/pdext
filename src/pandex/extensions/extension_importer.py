import os, sys, types

from ..symbols import __import_file_ext__, repository, __pdext__

class ExtensionImporter(object):
    """
    Extensions may also be to be defined in a text file and imported 
    using the standard python ``import`` statement.

    The text file must be have a file extension of |``import.ext``| and be 
    located in the same directory as the file where the ``import`` is
    called from.

    Format of text file::

        # Can contain comment lines beginning with #

        # Blank lines are ignored

        # one extension specification per line
        /path/to/extension/files  -> extension_function1
        /path/to/extension/files  -> collection.extension_function2
        github:username/repo      -> extension_function3

    As an example, if a file named ``my_extensions`` |``import.ext``| is created
    with the extensions above, then a file named ``analysis.py``
    can begin:

    .. parsed-literal::

        import |pandex| as pd
        import my_extensions

        df = pd.DataFrame({'x': [1,2,3,4]})

        # call the extension
        |df.ext|.extension_function1()


    """

    def find_module(self, fullname, path=None):
        """
        If an extension file is found, then the extensions are loaded 
        at this point
        """
        import_file = os.path.join(*(fullname.split('.'))) + __import_file_ext__
        if os.path.exists(import_file):
            with open(import_file) as stream:
                import_content = stream.read()
                pd_ext = repository()
                pd_ext.import_extension(import_content)
            return self

    def load_module(self, fullname):
        """
        Create an empty module in sys modules to comply with
        the import protocol

        Credit to Anhad Jai Singh blog post:
             https://blog.ffledgling.com/python-imports-i.html
        """

        # If the module already exists in `sys.modules` we *must* use that
        # module, it's a mandatory part of the importer protcol
        if fullname in sys.modules:
            return
        
        try:
            # The importer protocol requires the loader create a new module
            # object, set certain attributes on it, then add it to
            # `sys.modules` before executing the code inside the module (which
            # is when the "module" actually gets code inside it)

            m = types.ModuleType(fullname, '{} extension import'.format(__pdext__))
            m.__file__ = '<{} import>'.format(__pdext__)
            m.__name__ = fullname
            m.__loader__ = self
            sys.modules[fullname] = m

            # Return empty module
            return m

        except Exception as e:
            # If it fails, we need to reset sys.modules to it's old state. This
            # is good practice in general, but also a mandatory part of the
            # spec, likely to keep the import statement idempotent and free of
            # side-effects across imports.

            # Delete the entry we might've created; use LBYL to avoid nested
            # exception handling
            if sys.modules.get(fullname):
                del sys.modules[fullname]
            raise e
        return None



