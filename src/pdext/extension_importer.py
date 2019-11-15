import os, sys, types

from .symbols import __import_file_ext__, repository

class ExtensionImporter(object):
    """
    Allows extensions to be defined in a text file and imported 
    using the import statement.

    The text file must be have a suffix of .pdext.  
    Format of text file:
        # Can contain comment lines beginning with #
        # Blank lines are ignored
        /path/to/extension/files   extension_function1
        /path/to/extension/files   collection.extension_function2
        github:username/repo       extension_function3
    """

    def find_module(self, fullname, path=None):
        """
        If an extension file is found, then the extensions are loaded 
        at this point
        """
        self.import_file = os.path.join(*(fullname.split('.'))) + __import_file_ext__
        if os.path.exists(self.import_file):
            pd_ext = repository()
            for extension_location, name in self.parse_import_file():
                pd_ext.import_extension(extension_location, name)
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

            m = types.ModuleType(fullname, 'pdext extension import')
            m.__file__ = '<pdext import>'
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

    def parse_import_file(self):
        with open(self.import_file) as stream:
            lines = stream.readlines()
            # remove comments and return only lines with two arguments
            lines = [l for l in lines if not l.startswith('#')]
            lines = [l.split() for l in lines if len(l.split())==2]
            for l in lines:
                yield l[0], l[1]


