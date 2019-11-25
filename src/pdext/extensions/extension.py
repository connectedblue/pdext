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

from ..symbols import __df_ext__, __pdext__
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
        self._enabled = None
        self._func_doc = None
        self._extension_signature = None
    
    def remove(self):
        shutil.rmtree(self.ext_info.path)

    @property
    def enabled(self):
        return self.ext_info.enabled
    
    @enabled.setter
    def enabled(self, value):
        self.ext_info.enabled = value

    def remove_module_path(self):
        if os.path.exists(self.ext_info.module_path):
            shutil.rmtree(self.ext_info.module_path)

    def find_extension_file(self):
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
        try:
            func = getattr(self.imported_module, self.ext_info.name)
            self.extension_signature = func
            self.imported_ok = True

        except ModuleNotFoundError as e:
            # Create a dummy extension
            class pdext_extension(object): 
                """
                EXTENSION CANNOT BE LOADED

                There is a import module dependency within the
                extension code that will need to be installed
                before this extension can be imported correctly:

                """
                def __call__(self, *args):
                    import logging
                    logging.warning(self.__pdext_err__)
            
            func = pdext_extension()
            func.__name__ = self.ext_info.name
            self.pdext_fix_advice = 'module:  ' + e.name + '  needs to be installed\n'
            func.__doc__ = getattr(func, '__doc__') + self.pdext_fix_advice
            func.__pdext_err__ = getattr(e, 'pdext_err')

            # set parameters to enable extension to be called
            # like a normally imported one
            self.ext_info._enabled = True
            self.extension_signature = func
            self.imported_ok = False
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
            except AttributeError:
                raise AttributeError('Extension {} not installed'.format(self.ext_info.name))
            except ModuleNotFoundError as e:
                e.pdext_err = "{} extension {} requires library {} which is not installed"\
                                .format(__pdext__, self._full_extension_name(), e.name)
                e.args += (getattr(e, 'pdext_err'),)
                raise e
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
    
    def _initialise_from_imported_module(self):
        self._enabled = getattr(self.imported_module, 'init_values')['enabled']
        self.matched_file = getattr(self.imported_module, 'init_values')['extension_file']

    def _update_func_doc(self, func):
        """
        Additional text is added to the documentation of the
        extension to show how the user should call it
        """
        if self._func_doc is None:
            self._func_doc = func.__doc__

            self._func_doc += '\nUSAGE: {}'\
                                .format(self.extension_signature)
        func.__doc__ = self._func_doc

    @property
    def install_args(self):
        return {
            'extension_spec': self.ext_info.install_location,
        }
    
    @property
    def extension_signature(self):
        return self._extension_signature

    @extension_signature.setter
    def extension_signature(self,func):
        sig = inspect.signature(func)
        params = list(sig.parameters)
        other_args = ', '.join(params[1:])
        
        self._extension_signature = 'df.{ext_name}({other_args})'\
                .format(ext_name=self._full_extension_name(include_ext=True),
                        other_args=other_args)
        self._update_func_doc(func)
    
    def _full_extension_name(self, include_ext=False):
        name = ''
        if include_ext:
            name += '{ext}.'.format(ext=__df_ext__)
        if self.ext_info.is_collection:
            name += '{collection}.'.format(collection=self.ext_info.collection)
        return name + '{func_name}'.format(func_name=self.ext_info.name)

