import os, shutil

from ..extensions import Extension
from ..symbols import __import_file_sep__, __import_file_line_spec__
from .extension_location import ExtensionLocation
# This is a bit messy, but the parse function is embedded into 
# the repository class, so just extract this function out
from .extension_management import extension_management_mixin
_parse_extension_name = extension_management_mixin._parse_extension_name

class ExtensionSpecification(object):
    """
    Exposes methods and attributes to the 
    ExtensionRepository.import_extension() method:

        .get_lines()  -- returns an ExtensionSpecificationLine() instance
                         for each valid line of the spec
        .import_completed() -- signals the end of the import process
                               so that temporary install directorys can
                               be deleted
    """
    def __init__(self, spec, repo):
        """
        Creates individual ExtensionSpecificationLine instances for
        each line in the extension spec.
        Input:
            spec -- string specifying which extensions should be 
                    installed as specified by the import_extension()
                    method of the ExtensionRepository instance
            repo -- the path name of the repository where the
                    extensions should be installed into

        """
        self.spec = spec
        self.repo = repo

        self.extension_locations = {}
        self._parse_extension_spec()

    def get_lines(self):
        for line in self.lines:
            yield line

    def import_completed(self):
        for line in self.extension_locations.values():
            line.remove_install_from_dir()
    
    def _parse_extension_spec(self):
        lines = self.spec.splitlines()
        # remove comments and return only lines with two arguments
        lines = [l for l in lines if not l.startswith('#')]
        lines = [l.split(__import_file_sep__)\
                     for l in lines if len(l.split(__import_file_sep__))==2]
        self.lines = []
        for line in lines:
            # Get or create the ExtensionLocation object from the first
            # item in the line
            loc = line[0].strip()
            if loc in self.extension_locations:
                extension_location = self.extension_locations[loc]
            else:
                extension_location = ExtensionLocation(loc)
                self.extension_locations[loc] = extension_location 
            
            # Create the Extension object from the second item in the line
            name = line[1].strip()
            collection, ext_name=_parse_extension_name(name)
            extension_path = os.path.join(self.repo,collection,ext_name)
            extension = Extension(extension_path)

            self.lines.append(ExtensionSpecificationLine(extension_location, extension))

            # Save the spec as extension_info
            extension.ext_info.install_location = __import_file_line_spec__.format(loc,name)

class ExtensionSpecificationLine(object):
    """
    Exposes methods and attributes to the 
    ExtensionRepository.import_extension() method:

        .install()  -- installs the specified extension 
        .ext_name -- name of extension
        .collection -- name of collection
        .ext_spec -- original spec entered by user
    """
    def __init__(self, extension_location, extension):
        """
        Handles 
        Input:
            extension_location -- an instance of ExtensionLocation
            extension -- an instance of Extension
        """
        self.extension_location = extension_location
        self.extension = extension

    @property
    def ext_name(self):
        return self.extension.ext_info.name
    
    @property
    def collection(self):
        return self.extension.ext_info.collection

    @property
    def ext_spec(self):
        return self.extension.ext_info.install_location
    
    def install(self):
        # remove any old extension files and copy new ones in
        self.extension.remove_module_path()
        extension_files = self.extension_location.install_from_dir
        shutil.copytree(extension_files, self.extension.ext_info.module_path)
        try:
            self.extension.find_extension_file()
            # setting the enabled property causes the __init__.py
            # to be created
            self.extension.enabled=True
        except:
            self.extension.remove_module_path()
            raise