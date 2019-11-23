import os, hashlib
from datetime import datetime
from pathlib import Path

from ..symbols import __default_collection__, __install_timestamp_fmt__

class ExtensionInfo(object):
    """
    Holds various meta data about the extension,  It is either
    created during an install, or read from the __init__.py file
    in the installed extension module

    The __init__.py file is updated as values are changed if necessary
    as values are updated to this object
    """
    init_py = """\
from .{extension_file} import {extension_name}\n

enabled = {enabled}

init_values = {{
    'extension_file': '{extension_file}',
    'extension_name': '{extension_name}',
    'enabled': {enabled},
    'install_location': '{install_location}',
    'install_collection': '{install_collection}',
    'install_repository': '{install_repository}',
    'install_files': '{install_files}',
    'install_time': '{install_time}',
}}
"""
    def __init__(self, extension_path):
        """
        Input:
            extension_path -- string of the form:
                                /path/to/repo/collection/extension
        """
        self.path = extension_path
        #        if os.path.isdir(self.path):
        self.initialise_extension_layout()

    def create_extension_path(self):
        os.makedirs(self.path)
        self.initialise_extension_layout()
    
    def initialise_extension_layout(self):
        # extract the extension attributes from the path
        self.name = os.path.basename(self.path)
        self.collection = os.path.basename(os.path.split(self.path)[0])
        self.is_collection = (self.collection != __default_collection__)
        
        # The module is given a unique name to avoid import problems
        # if the same extension name exists in different collections
        self.module = hashlib.sha1(bytes(self.path, 'utf-8')).hexdigest()
        self.module_path = os.path.join(self.path, self.module)
        self.matched_file = None
        self.install_location = None
        self.install_repository = None
        self.install_files = None
        self._install_time = None

    def _create_init_py(self):
        """
        set up an __init__.py file to import the extension and 
        manage other settings
        """
        with open(self.init_py_location, 'w+') as f:
            f.write(self._rendered_init_py)

    @property
    def _rendered_init_py(self):
        return self.init_py.format(extension_file=self.matched_file, 
                              extension_name=self.name,
                              enabled=self.enabled,
                              install_location=self.install_location,
                              install_collection=self.collection,
                              install_repository=self.install_repository,
                              install_files=self.install_files,
                              install_time=self.install_time)

    @property
    def init_py_location(self):
        return os.path.join(self.module_path, '__init__.py')

    def initialise_from_imported_module(self, module):
        self._enabled = getattr(module, 'init_values')['enabled']
        self.matched_file = getattr(module, 'init_values')['extension_file']
        self.install_location = getattr(module, 'init_values')['install_location']
        self.install_repository = getattr(module, 'init_values')['install_repository']
        self.install_files = getattr(module, 'init_values')['install_files']
        self.install_time = getattr(module, 'init_values')['install_time']

    @property
    def enabled(self):
        return self._enabled
    
    @enabled.setter
    def enabled(self, value):
        self._enabled = value
        self._create_init_py()
    
    @property
    def install_time(self):
        if self._install_time is None:
            return datetime.now().strftime(__install_timestamp_fmt__)
        return self._install_time.strftime(__install_timestamp_fmt__)
    
    @install_time.setter
    def install_time(self, value):
        self._install_time = datetime.strptime(value, __install_timestamp_fmt__)

    def is_earlier_than(self, compare_to_date):
        return datetime.strptime(compare_to_date, __install_timestamp_fmt__) > self._install_time