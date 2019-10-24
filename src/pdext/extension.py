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

from importlib import import_module, invalidate_caches

from .symbols import __df_ext__, __default_collection__

class Extension(object):

    def __init__(self, extension_path):
        self.path = extension_path

        if not os.path.isdir(self.path):
            os.makedirs(self.path)

        self.name = os.path.basename(self.path)
        self.collection = os.path.basename(os.path.split(self.path)[0])
        self.is_collection = (self.collection != __default_collection__)
        self._module = hashlib.sha1(bytes(self.path, 'utf-8')).hexdigest()
        self._module_path = os.path.join(self.path, self._module)
        
    def install(self, extension_files):
        # remove any old extension files and copy new ones in
        self._remove_module_path()
        shutil.copytree(extension_files, self._module_path)
        try:
            self._create_init_py()
        except:
            self._remove_module_path()
            raise
    
    def _remove_module_path(self):
        if os.path.exists(self._module_path):
            shutil.rmtree(self._module_path)

    def _create_init_py(self):
        """
        Looks for a py file with that contains a function name the
        same as the extension name and set up an __init__.py file 
        to import that function
        """
        search_string = 'def {}'.format(self.name)
        matched_file = None
        search_files = Path(self._module_path).rglob('*.py')
        # if self.name == 'calculate_circumference_from_radius_nested':
        #     breakpoint()
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
        
        # Create the init.py to import the function from the correct file
        init_py = os.path.join(self._module_path, '__init__.py')
        init_py_content = 'from .{} import {}\n'.format(matched_file, self.name)
        with open(init_py, 'w+') as f:
            f.write(init_py_content)

    def get_extension(self):
        sys_path = sys.path
        sys.path.append(self.path)
        # need to invalidate the import cache 
        # when dynamically creating new modules since
        # the interpreter started
        invalidate_caches()

        try:
            ext = getattr(import_module(self._module), self.name)
        except (AttributeError, ModuleNotFoundError) as e:
            raise ('Extension {} not installed'.format(self.name))
        finally:
            sys.path = sys_path
        
        self._set_extension_signature(ext)
        self._update_func_doc(ext)
        return ext

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
