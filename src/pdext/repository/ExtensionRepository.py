from .extension_properties import extension_properties_mixin
from .extension_management import extension_management_mixin
from .config_file_management import config_file_management_mixin
from .user_repository_methods import user_repository_methods_mixin
from .user_extension_control_methods import user_extension_control_methods_mixin
from .user_extension_install_methods import user_extension_install_methods_mixin

class ExtensionRepository(user_repository_methods_mixin,
                          user_extension_install_methods_mixin,
                          user_extension_control_methods_mixin,
                          extension_management_mixin,
                          config_file_management_mixin,
                          extension_properties_mixin):
    """
    Initialise the Extension Repository and pull in the functionality via
    Mix-in classes 
    """
    def __init__(self):
        self._build_extension_collections()

    @property
    def __version__(self):
        from ..symbols import __version__
        return __version__

