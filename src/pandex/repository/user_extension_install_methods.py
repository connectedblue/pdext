import os
import logging

from ..symbols import __default_collection__, __import_file_sep__
from ..extensions import Extension
from .extension_spec import ExtensionSpecification

class user_extension_install_methods_mixin(object):
    """
    All the methods which a user can call to manipulate 
    extensions.

    Extensions can then be installed into the correct location
    so they can be found by the pandas extension class.  Any 
    namespace clashes are resolved using the repository search order
    which can also be specified by the user.
    """
    def import_extension(self, extension_spec):
        """
        Imports extensions that don't already exist into the default repo
        
        *Input Parameters:*

            **extension_spec:**
    
                A string with one or more lines of format::

                    extension_location -> name

                where:
                    ``extension_location:``
                        location of all the files needed
                        for that extension.  There must be a function
                        with the extension name in one of the ``.py``
                        files at that location
                        
                        Format options:
                            *   ``<directory name on local file system>``
                            *   ``<.py file  name on local file system>``
                            *   Files on GitHub are referenced::
                            
                                    github:username/repo[@branch/tag][/path/to/directory]
                                
                                where ``repo`` is a public repo on github for ``username``.
                                The latest commit on `master` is the default unless a
                                specific ``branch`` or ``tag`` is optionally provided.

                    ``name:``
                        string name of extension 
                        (including collection if required)
                        to be installed              
        """
        repo = os.path.join(self._repository_path(self.default_repository))
        parsed_spec = ExtensionSpecification(extension_spec, repo)

        for line in parsed_spec.get_lines():
            try:
                # if it doesn't exist in the default repo then install
                ext_path = os.path.join(repo, line.collection, line.ext_name)
                if not os.path.isdir(ext_path):
                    raise KeyError
                # check if it imports cleanly
                ext = self._get_extension_object(line.ext_name, line.collection)
            except KeyError:
                # Now we know we need to install
                line.install()
                self._build_extension_collections()
                # check if there are any dependency warnings by importing again
                self.import_extension(line.ext_spec)
            
            # Check if there are any dependencies in the extension
            # code and warn the user if so
            except ModuleNotFoundError as e:
                logging.warning(getattr(e, 'pdext_err')) 
        
        parsed_spec.import_completed()
            
    def reinstall_extension(self, name):
        """
        Re-install an extension from the original source

        *Input Parameters:*

            **name:** 
                string name of extension (including collection if there is one)
        """
        # locate extension to be removed
        collection, name=self._parse_extension_name(name)
        ext = self._get_extension_object(name, collection)
        install_args = ext.install_args
        self.remove_extension(name)
        self.import_extension(**install_args)
            
