from .extension_properties import extension_properties
from .extension_management import extension_management
from .config_file_management import config_file_management
from .user_methods import user_methods

class ExtensionRepository(user_methods, 
                          extension_management,
                          config_file_management,
                          extension_properties):
    """
    Initialise the Extension Repository and pull in the functionality via
    Mix-in classes 
    """
    def __init__(self):
        self._build_extension_collections()

