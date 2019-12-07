# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

pdext_location = os.path.join('..', 'src')
sys.path.insert(0, os.path.abspath(pdext_location))

# Get some constants needed for the documentation
# This will need altering if the package name changes
import pandex
doc = pandex.ext.doc

project_name = doc.__pdext__

# -- Project information -----------------------------------------------------

project = project_name
copyright = '2019, Chris Shaw'
author = 'Chris Shaw'

# The full version, including alpha/beta/rc tags
release = 'v1.0'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['m2r', 'sphinx.ext.autodoc',
]


# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', 
                    'change_project_name.md',]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# make a whole suite of allowable formats for substitions because
# Sphinx doesn't allow to have in-line formatting on substitutions
#   e.g. if |name| is a substitution, then |**name**| is the bold
#        version
# New formats can be added to the template if required
def generate_substitutions(subs):
    output = ''
    template = """
.. |{symbol}| replace:: {replacement}
.. |*{symbol}*| replace:: *{replacement}*
.. |**{symbol}**| replace:: **{replacement}**
.. |`{symbol}`| replace:: `{replacement}`
.. |``{symbol}``| replace:: ``{replacement}``
"""
    for s, r in subs.items():
        output += template.format(symbol=s, replacement=r)
    return output

# substitutions used in rst files and doc strings
# are defined here
ext = doc.__pd_ext__
rst_prolog = generate_substitutions({\
                'pandex': project_name,
                'demo_repo': 'connectedblue/pdext_collection',
                'ext': ext,
                'pd.ext': 'pd.{}'.format(ext),
                'df.ext': 'df.{}'.format(ext),
                'import.ext': doc.__import_file_ext__,
})