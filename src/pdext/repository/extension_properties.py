import os

class extension_properties_mixin(object):
    """
    Some common class attributes used by the various
    class methods
    """
    @property
    def _search_path(self):
        return [self._repository_path(name) \
                    for name in self._search_order]

    @property
    def _search_order(self):
        return self._repository_elements('name')
    
    def _repository_elements(self,by):
        return [c[by] for c in self.repositories]

    @property
    def _repositories_by_name(self):
        return {n['name']:n for n in self.repositories}

    def _repository_path(self, name):
        """
        Returns the path for a particular name
        """
        return os.path.expanduser(self._repositories_by_name[name]['location'])

    # Ensure that the default repository exists
    @property
    def default_repository(self):
        return self._default_repository

    @default_repository.setter
    def default_repository(self, value):
        if value not in self._search_order:
            raise KeyError('{} is not a repository name'.format(value))
        self._default_repository = value
        
