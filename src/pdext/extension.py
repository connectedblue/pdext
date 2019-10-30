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
import os, hashlib, shutil, sys, inspect
from pathlib import Path

from importlib import import_module, invalidate_caches, reload

from .symbols import __df_ext__, __default_collection__

init_py = """\
from .{extension_file} import {extension_name}\n

enabled = {enabled}

init_values = {{
    'extension_file': '{extension_file}',
    'extension_name': '{extension_name}',
    'enabled': {enabled},
}}
"""
class Extension(object):

    def __init__(self, extension_path):
        """
        Input:
            extension_path -- string of the form:
                                /path/to/repo/collection/extension
        """
        self.path = extension_path
        if not os.path.isdir(self.path):
            os.makedirs(self.path)

        # extract the extension attributes from the path
        self.name = os.path.basename(self.path)
        self.collection = os.path.basename(os.path.split(self.path)[0])
        self.is_collection = (self.collection != __default_collection__)
        
        # The module is given a unique name to avoid import problems
        # if the same extension name exists in different collections
        self._module = hashlib.sha1(bytes(self.path, 'utf-8')).hexdigest()
        self._module_path = os.path.join(self.path, self._module)

        # These attributes are not set until import
        self._imported_module = None
        self._enabled = None
        
    def install(self, extension_files, enabled=True):
        # remove any old extension files and copy new ones in
        self._remove_module_path()
        shutil.copytree(extension_files, self._module_path)
        try:
            self._find_extension_file()
            self.enabled=enabled
        except:
            self._remove_module_path()
            raise
    
    def remove(self):
        shutil.rmtree(self.path)

    @property
    def enabled(self):
        return self._enabled
    
    @enabled.setter
    def enabled(self, value):
        self._enabled = value
        self._create_init_py()


    def _remove_module_path(self):
        if os.path.exists(self._module_path):
            shutil.rmtree(self._module_path)

    def _find_extension_file(self):
        """
        Looks for a py file with that contains a function name the
        same as the extension name
        """
        search_string = 'def {}'.format(self.name)
        matched_file = None
        search_files = Path(self._module_path).rglob('*.py')
        for file in search_files:
            with open(file, 'r') as f:
                if search_string in f.read():
                    d = [i for i in file.parts \
                            if i not in Path(self._module_path).parts]
                    d = d[:-1] + [os.path.splitext(os.path.basename(d[-1]))[0]]
                    matched_file = '.'.join(d)
                    break
        if matched_file is None:
            raise ValueError('{} is not defined in extension files')
        self.matched_file = matched_file
    
    def _create_init_py(self):
        """
        set up an __init__.py file to import the extension and 
        manage other settings
        """
        with open(self.init_py_location, 'w+') as f:
            f.write(self._rendered_init_py)

    @property
    def _rendered_init_py(self):
        return init_py.format(extension_file=self.matched_file, 
                              extension_name=self.name,
                              enabled=self.enabled)

    @property
    def init_py_location(self):
        return os.path.join(self._module_path, '__init__.py')

    def get_extension(self):
        ext = getattr(self.imported_module, self.name)
        self._set_extension_signature(ext)
        self._update_func_doc(ext)
        return ext
    
    @property
    def imported_module(self):
        if self._imported_module is None:
            sys_path = sys.path
            sys.path.append(self.path)
            # need to invalidate the import cache 
            # when dynamically creating new modules since
            # the interpreter started
            invalidate_caches()
            try:
                self._imported_module = import_module(self._module)
            except (AttributeError, ModuleNotFoundError) as e:
                raise AttributeError('Extension {} not installed'.format(self.name))
            finally:
                sys.path = sys_path
            self._initialise_from_imported_module()
        return self._imported_module

    def reload(self):
        if self._imported_module is None:
            self.imported_module
        else:
            reload(self._imported_module)
            self._initialise_from_imported_module()
    
    def _initialise_from_imported_module(self):
        self._enabled = getattr(self.imported_module, 'init_values')['enabled']
        self.matched_file = getattr(self.imported_module, 'init_values')['extension_file']

    def _update_func_doc(self, func):
        """
        Additional text is added to the documentation of the
        extension to show how the user should call it
        """
        doc = func.__doc__

        doc += '\nUSAGE: {}'\
                .format(self.extension_signature)
        func.__doc__ = doc
    
    def _set_extension_signature(self,func):
        func_name = func.__name__
        sig = inspect.signature(func)
        params = list(sig.parameters)
        first_arg = params[0]
        other_args = ', '.join(params[1:])
        args = first_arg + other_args
        collection = ''
        if self.is_collection:
            collection = '.{}'.format(self.collection)
        self.extension_signature = 'df.{ext}{collection}.{func_name}({other_args})'\
                .format(ext=__df_ext__,
                        collection=collection,
                        func_name=func_name,
                        other_args=other_args)
