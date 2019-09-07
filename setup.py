from setuptools import setup, find_packages
import versioneer

setup(
    name='pdext',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description= 'Extension framework for pandas',
    author='Chris Shaw',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'pandas', 
        'numpy', 
    ],
    )
