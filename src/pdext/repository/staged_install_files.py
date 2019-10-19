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
import os, shutil, tempfile
from contextlib import contextmanager
 
 
@contextmanager
def staged_install_files(extension_files_location):
    """
    Take the extension_files specified by the user and copy
    them to a temporary directory for installation. Delete the
    temp directory after
    Input:
        extension_files_location -- string of the form:
                                        <directory name>
                                        <single .py file>
    Yields:
        tmp_install_dir -- temporary directory with extension files
    
    Output:
        None -- temp directory deleted
    """
    tmp_install_root = tempfile.mkdtemp()
    tmp_install_dir = os.path.join(tmp_install_root, 'files')
    extension_files = os.path.expanduser(extension_files_location)

    # check if location is directory
    location_type = _get_location_type(extension_files)
    if location_type == 'local_directory':
        shutil.copytree(extension_files, tmp_install_dir) 
    if location_type == 'single_py_file':
        os.makedirs(tmp_install_dir)
        shutil.copy(extension_files, tmp_install_dir)
    if location_type == 'unsupported':
        raise ValueError('Invalid location of extension files: {}'\
                         .format(extension_files))
    
    yield tmp_install_dir
    shutil.rmtree(tmp_install_root)

def _get_location_type(location):
    if os.path.isdir(location):
        return 'local_directory'
    if os.path.exists(location) and location.endswith('.py'):
        return 'single_py_file'
    return 'unsupported'