"""
Manage the installation and execution of a single extension located 
on a filesystem path:

/some/path/to/repository/collection/extension

Assume that the basename of the path is the extension name 

This class does not need to know about the repository or collection
organisation inherent in the path above that.  However, to prevent 
namespace clashes when importing the extension, it creates a structure
below to store the extension

extension/
          <hash of extension path>/
                                    __init__.py
                                    extension_file_1.py
                                    extension_file_2.py
                                    etc .....

The __init__.py is auto generated to find the correct function 
call, for example:
    from .extension_file_2 import extension

The extension can then be imported from module <hash of extension path>
and the sys.path needs to be aware of the original filesystem path

No object outside this class needs to be concerned with this internal
layout and access mechanism
"""
import os, shutil, sys, inspect
from pathlib import Path

from importlib import import_module, invalidate_caches, reload

from .symbols import __df_ext__
from .extension_info import ExtensionInfo

class Extension(object):

    def __init__(self, extension_path):
        """
        Input:
            extension_path -- string of the form:
                                /path/to/repo/collection/extension
        """
        self.ext_info = ExtensionInfo(extension_path)

        # These attributes are not set until import
        self._imported_module = None
        self._extension_signature = None
        
    def install(self, extension_files, extension_location, repository_name, enabled=True):
        # remove any old extension files and copy new ones in
        self.ext_info.install_location = extension_location
        self.ext_info.install_repository = repository_name
        self.ext_info.install_files = extension_files
        self._remove_module_path()
        shutil.copytree(extension_files, self.ext_info.module_path)
        try:
            self._find_extension_file()
            self.enabled=enabled
        except:
            self._remove_module_path()
            raise
    
    def remove(self):
        shutil.rmtree(self.ext_info.path)

    @property
    def enabled(self):
        return self.ext_info.enabled
    
    @enabled.setter
    def enabled(self, value):
        self.ext_info.enabled = value

    def _remove_module_path(self):
        if os.path.exists(self.ext_info.module_path):
            shutil.rmtree(self.ext_info.module_path)

    def _find_extension_file(self):
        """
        Looks for a py file with that contains a function name the
        same as the extension name
        """
        search_string = 'def {}'.format(self.ext_info.name)
        matched_file = None
        search_files = Path(self.ext_info.module_path).rglob('*.py')
        for file in search_files:
            with open(file, 'r') as f:
                if search_string in f.read():
                    # Need to get the parts of the filename that are
                    # relative to the module directory (ie after the
                    # module path)
                    d = list(file.parts[len(Path(self.ext_info.module_path).parts):])
                    d = d[:-1] + [os.path.splitext(os.path.basename(d[-1]))[0]]
                    matched_file = '.'.join(d)
                    break
        if matched_file is None:
            raise ValueError('{} is not defined in extension files')
        self.ext_info.matched_file = matched_file
    
    def get_extension(self):
        func = getattr(self.imported_module, self.ext_info.name)
        self.extension_signature = func
        return func
    
    @property
    def imported_module(self):
        if self._imported_module is None:
            sys_path = sys.path
            sys.path.append(self.ext_info.path)
            # need to invalidate the import cache 
            # when dynamically creating new modules since
            # the interpreter started
            invalidate_caches()
            try:
                self._imported_module = import_module(self.ext_info.module)
            except (AttributeError, ModuleNotFoundError) as e:
                raise AttributeError('Extension {} not installed'.format(self.ext_info.name))
            finally:
                sys.path = sys_path
            self.ext_info.initialise_from_imported_module(self._imported_module)
        return self._imported_module

    def reload(self):
        if self._imported_module is None:
            self.imported_module
        else:
            reload(self._imported_module)
            self.ext_info.initialise_from_imported_module(self._imported_module)
        
    # Some properties required outside the class
    @property
    def extension_name(self):
        return self.ext_info.name
    
    @property
    def install_args(self):
        return {
            'name': self.ext_info.name, 
            'extension_location': self.ext_info.install_location,
            'collection': self.ext_info.collection,
            'repository_name': self.ext_info.install_repository,
        }
    
    @property
    def extension_signature(self):
        return self._extension_signature

    @extension_signature.setter
    def extension_signature(self,func):
        func_name = func.__name__
        sig = inspect.signature(func)
        params = list(sig.parameters)
        first_arg = params[0]
        other_args = ', '.join(params[1:])
        args = first_arg + other_args
        collection = ''
        if self.ext_info.is_collection:
            collection = '.{}'.format(self.ext_info.collection)
        self._extension_signature = 'df.{ext}{collection}.{func_name}({other_args})'\
                .format(ext=__df_ext__,
                        collection=collection,
                        func_name=func_name,
                        other_args=other_args)
        self._update_func_doc(func)

    def _update_func_doc(self, func):
        """
        Additional text is added to the documentation of the
        extension to show how the user should call it
        """
        doc = func.__doc__

        doc += '\nUSAGE: {}'\
                .format(self.extension_signature)
        func.__doc__ = doc
