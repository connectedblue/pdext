from setuptools import setup, find_packages
import versioneer

# package name
from src.pdext.symbols import __pdext__

# Write the version into the package directory 
# before building
__version__ = versioneer.get_version() 
generated_build_content = """\
__version__ = '{version}'
""".format(version=__version__)
with open('src/pdext/_build_info.py', 'w') as f:
    f.write(generated_build_content)


setup(
    name=__pdext__,
    version=__version__,
    cmdclass=versioneer.get_cmdclass(),
    description= 'Extension framework for pandas',
    author='Chris Shaw',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'pandas', 
    ],
    include_package_data=True
    )
