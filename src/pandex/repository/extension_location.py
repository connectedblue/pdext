import os, re, urllib, shutil, tempfile, logging
from zipfile import ZipFile

class ExtensionLocation(object):
    """
    Provides a temporary place on the filesystem where the
    relevant extension files can be copied from during an import

    Exposes methods and attributes to the 
    ExtensionSpecificationLine object
        install_from_dir -- path where extension files can be found
        .remove_install_from_dir()  -- removes this temporary directory
                                       when called
    """
    def __init__(self, extension_location):
        self.extension_location = extension_location
        self._install_from_dir = None
        self.tmp_install_root = None

    def remove_install_from_dir(self):
        """
        Called at the end of the import process to clean up
        """
        if self.tmp_install_root is not None:
            shutil.rmtree(self.tmp_install_root)
    
    @property
    def install_from_dir(self):
        # returns a local directory containing the files
        if self._install_from_dir is None:
            self.tmp_install_root = tempfile.mkdtemp()
            tmp_install_dir = os.path.join(self.tmp_install_root, 'files')

            location = self.extension_location
            location_type = 'local_directory'
            
            if location.startswith('github:'):
                extension_files = self.get_files_from_github(self.tmp_install_root)
            else:
                # location is on the filesystem
                extension_files = os.path.expanduser(location)
                if os.path.exists(extension_files) and extension_files.endswith('.py'):
                    location_type = 'single_py_file'
                if not os.path.exists(extension_files):
                    location_type = 'unsupported' 

            if location_type == 'local_directory':
                shutil.copytree(extension_files, tmp_install_dir) 
            if location_type == 'single_py_file':
                os.makedirs(tmp_install_dir)
                shutil.copy(extension_files, tmp_install_dir)
            if location_type == 'unsupported':
                raise ValueError('Invalid location of extension files: {}'\
                                .format(extension_files))

            self._install_from_dir = tmp_install_dir

        return self._install_from_dir

    def get_files_from_github(self,temp_dir):
        # location format: github:username/repo[@branch/tag][/path/to/directory]
        try:
            location = self.extension_location
            username, repo, path = re.match('^github:([^/]+)/([^/]+)(.*)',
                                            location).groups()
        except AttributeError:
            raise ValueError('Unable to parse github location: {}'.format(location))
        
        github_root = os.path.join(temp_dir, 'github')
        os.makedirs(github_root)
        zip_file = os.path.join(github_root, 'download.zip')
        extract_dir = os.path.join(github_root, 'extract')
        repo = repo.split('@')
        if len(repo)==1:
            repo = repo[0]
            branch = 'master'
        else:
            branch = repo[1]
            repo = repo[0]

        # bug #75 from windows user - this path needs to be in
        # unix form in order for ZipFile to extract properly
        path = '{repo}-{branch}'.format(repo=repo, branch=branch) +'/' + path[1:]
        url='https://github.com/{username}/{repo}/archive/{branch}.zip'\
                .format(username=username, repo=repo, branch=branch)
        urllib.request.urlretrieve(url, zip_file)
        logging.info('Extension repo {username}/{repo} downloaded from {url}'\
                .format(username=username, repo=repo, url=url))

        with ZipFile(zip_file) as zip:
            for f in zip.namelist():
                if path in f:
                    zip.extract(f, extract_dir)
        return os.path.join(extract_dir, path)