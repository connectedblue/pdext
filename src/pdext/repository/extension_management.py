import os, sys

from ..symbols import __default_collection__
from ..extensions import Extension


class extension_management_mixin(object):
    """
    Builds the internal structures to allow extensions to 
    be retrieved by the ExtensionManager that is plugged
    into the pandas extension system
    """
    def _build_extension_collections(self):
        """
        Create a nested dictionary of function objects of the form
            self.extension_collections[collection_name][extension_name]=Extension
        """
        self._read_config_file()
        # Get all collection names from all the repositories
        # and initialise
        ext = {__default_collection__: {}}
        for path in self._search_path:
            for collection in next(os.walk(path))[1]:
                ext[collection] = {}
        
        # find the first occurence of each extension on the
        # search path of each collection
        for collection in ext:
            for path in self._search_path:
                extensions = os.path.join(path, collection)
                try:
                    for extension in next(os.walk(extensions))[1]:
                        if extension not in ext[collection]:
                            extension_location = os.path.join(extensions,
                                                              extension)
                            ext[collection][extension] = \
                                Extension(extension_location)
                except StopIteration:
                    # If there are no extensions in the collection,
                    # carry on
                    continue
        self.extension_collections = ext  

    def _get_extension_from_collection(self, name):
        collection, name=self._parse_extension_name(name)
        ext = self._get_extension_object(name, collection)
        return ext.get_extension()

    @staticmethod
    def _parse_extension_name(name):
        name = name.split('.')
        num_levels = len(name)
        if num_levels>2:
            raise IndexError("Extensions can't be nested {} levels"\
                                .format(num_levels))
        if num_levels==2:
            collection = name[0]
            extension_name = name[1]
        else:
            collection = __default_collection__
            extension_name = name[0]
        return collection, extension_name

    def _get_extension_object(self, name, collection):
        try:
            ext = self.extension_collections[collection][name]
            # Make sure it's imported from disk
            ext.reload()
        except KeyError:
            if collection == __default_collection__:
                collection = ''
            else:
                collection = collection + '.'
            raise KeyError('Extension {}{} - doesnt exist'\
                            .format(collection, name))
        return ext

