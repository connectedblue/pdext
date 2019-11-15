"""
Extension Files specified by the user can be in various forms specified
by the user (single file, directory, github etc).  New ways could be
added in the future.

So the process for uploading will be common:
- create a temporary directory
- determine the type of extension_files_location
- determine where all the files are 
- copy them into the temporary directory
- return that directory to the installation process
- after installation delete the temporary directory

So to extend the locations supported, only steps two and three need
to be altered
"""
import os, shutil, tempfile, re, urllib
from contextlib import contextmanager
from zipfile import ZipFile
 
 
@contextmanager
def staged_install_files(extension_files_location):
    """
    Take the extension_files specified by the user and copy
    them to a temporary directory for installation. Delete the
    temp directory after
    Input:
        extension_files_location -- in format specifed in install_extension()
    Yields:
        tmp_install_dir -- temporary directory with extension files
    
    Output:
        None -- temp directory deleted
    """
    tmp_install_root = tempfile.mkdtemp()
    tmp_install_dir = os.path.join(tmp_install_root, 'files')

    # check if location is directory
    try:
        location_type, extension_files = _parse_location(extension_files_location, 
                                                        tmp_install_root)
        if location_type == 'local_directory':
            shutil.copytree(extension_files, tmp_install_dir) 
        if location_type == 'single_py_file':
            os.makedirs(tmp_install_dir)
            shutil.copy(extension_files, tmp_install_dir)
        if location_type == 'unsupported':
            raise ValueError('Invalid location of extension files: {}'\
                            .format(extension_files))
        
        yield tmp_install_dir
    finally:
        shutil.rmtree(tmp_install_root)

def _parse_location(location, temp_dir):
    """
    Format for the location type is specified in the
    install_extension doc string

    """
    location_type = 'local_directory'
    
    if location.startswith('github:'):
        extension_files = _get_files_from_github(location, temp_dir)
    else:
        # location is on the filesystem
        extension_files = os.path.expanduser(location)
        if os.path.exists(extension_files) and extension_files.endswith('.py'):
            location_type = 'single_py_file'
        if not os.path.exists(extension_files):
            location_type = 'unsupported'
    
    return location_type, extension_files

def _get_files_from_github(location, temp_dir):
    # location format: github:username/repo[@branch/tag][/path/to/directory]
    try:
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

    path = os.path.join('{repo}-{branch}'.format(repo=repo, branch=branch),
                        path[1:])
    url='https://github.com/{username}/{repo}/archive/{branch}.zip'\
            .format(username=username, repo=repo, branch=branch)
    urllib.request.urlretrieve(url, zip_file)

    with ZipFile(zip_file) as zip:
        for f in zip.namelist():
            if path in f:
                zip.extract(f, extract_dir)
    return os.path.join(extract_dir, path)
