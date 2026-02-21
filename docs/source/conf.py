# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path('../../src').resolve()))

# Buscamos la versión en __about__.py
about = {}
with open(os.path.join(os.path.dirname(__file__), "../../src/mesomath/__about__.py")) as f:
    exec(f.read(), about)

project = 'MesoMath'
copyright = '2025, jccsvq'
author = 'jccsvq'
version = about["__version__"]


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'MesoMath'
copyright = '2025, jccsvq'
author = 'jccsvq'
release = version

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
   'sphinx.ext.duration',
   'sphinx.ext.doctest',
   'sphinx.ext.autodoc',
   'sphinx.ext.autosummary',
   'sphinx_book_theme',
   'myst_parser',
   'sphinx.ext.napoleon', 
   'sphinx.ext.mathjax',
   
]
myst_enable_extensions = ["substitution"]
myst_substitutions = {
    "release": release
}

templates_path = ['_templates']
exclude_patterns = []

source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'markdown',
    '.md': 'markdown',
}
# Permite que autodoc vea miembros privados
autodoc_default_options = {
    'private-members': True,
}


# Evita que se muestre el path completo (mesomath.npvs.Blen -> Blen)
add_module_names = False

# Ordena los métodos por tipo (clase, método, etc.) o por fuente
autodoc_member_order = 'bysource'

autoclass_content = 'both'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_book_theme"
html_static_path = ['_static']
html_logo = '_static/mesomath.png'
html_favicon = '_static/favicon.svg'

rst_epilog = f"""
.. |release| replace::  {release}
"""