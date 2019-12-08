from setuptools import setup, find_packages
import versioneer

# package name
from src.pandex.symbols import __pdext__

# Write the version into the package directory 
# before building
__version__ = versioneer.get_version() 
__version__ =__version__.split('+')[0]

generated_build_content = """\
__version__ = '{version}'
""".format(version=__version__)
with open('src/pandex/_build_info.py', 'w') as f:
    f.write(generated_build_content)

# read the contents of README file
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()


setup(
    name=__pdext__,
    version=__version__,
    
    description= 'Extension framework for pandas',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Chris Shaw',
    author_email='chris@connectedblue.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'pandas', 'pyyaml', 
    ],
    include_package_data=True,
    url='http://github.com/connectedblue/pdext',
    keywords=['pandas', 'extensions'],
    tests_require=[
        'pytest',
        'pytest-cov',
        'pytest-sugar'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Natural Language :: English",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries",
    ],
    python_requires='>=3',
    )
