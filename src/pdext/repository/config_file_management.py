import os, yaml

from ..symbols import __installed_extensions__


class config_file_management_mixin(object):
    """
    All the extension repository information is stored in 
    a YAML file in the package folder for pdext
    """
    def _read_config_file(self):
        """
        Read in YAML config file and set up internal
        configuration for the class

        Example structure of YAML file:

            repositories:
            - name: user
            location: ~/.pdext
            - name: shared
            location: /opt/data/.pdext
            default_repository: user

        which parses into the following python object:
            {'repositories': 
                [{'name': 'user', 
                  'location': '~/.pdext'}, 
                 {'name': 'shared', 
                  'location': '/opt/data/.pdext'}], 
             'default_repository': 'user'}
        """
        try:
            no_config_file = False
            with open(__installed_extensions__, 'r') as stream:
                config = yaml.safe_load(stream)        

        except FileNotFoundError:
            # create a default configuration
            config =  {'repositories': 
                        [{'name': 'user', 
                          'location': '~/.pdext'}], 
                       'default_repository': 'user'} 
            no_config_file = True

        self.repositories = config['repositories']
        self.default_repository = config['default_repository']

        # ensure that all the locations exist and create if not
        for directory in self._search_path:
            self._create_directory(directory)
        if no_config_file:
            self._write_config_file()

    @staticmethod
    def _create_directory(directory):
        if not os.path.exists(directory):
            os.makedirs(directory)
    
    def _write_config_file(self):
        config = {'repositories': self.repositories,
                  'default_repository': self.default_repository}
        with open(__installed_extensions__, 'w') as outfile:
            yaml.dump(config, outfile, default_flow_style=False)
        self._build_extension_collections()
