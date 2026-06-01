# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
from pathlib import Path

# Insert the source path into the system path to allow autodoc to find mesomath/mesotimes
sys.path.insert(0, str(Path("../../src").resolve()))

# Detect if the building environment is the official Read the Docs cloud server
on_rtd = os.environ.get("READTHEDOCS") == "True"

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

about = {}
with open(
    os.path.join(os.path.dirname(__file__), "../../src/mesomath/__about__.py")
) as f:
    exec(f.read(), about)

project = "MesoMath"
copyright = "2025-2026, jccsvq"
author = "jccsvq"
version = about["__version__"]
release = version


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx_book_theme",
    "myst_parser",
    "sphinx.ext.napoleon",
    "sphinx.ext.mathjax",
    "sphinx_copybutton",
]

myst_enable_extensions = [
    "substitution",
    "dollarmath",
    "amsmath",
]
myst_substitutions = {"release": release}

templates_path = ["_templates"]
exclude_patterns = []

source_suffix = {
    ".rst": "restructuredtext",
    ".txt": "markdown",
    ".md": "markdown",
}

# Allow autodoc to process and document private internal members
autodoc_default_options = {
    "private-members": True,
}

# Do not show full package path prefixes (e.g., display 'Blen' instead of 'mesomath.npvs.Blen')
add_module_names = False

# Sort members by category grouping (classes, methods, attributes)
autodoc_member_order = "groupwise"

# Combine both class docstring and __init__ docstring in the documentation framework
autoclass_content = "both"


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_book_theme"
html_static_path = ["_static"]
html_logo = "_static/mesomath.svg"
html_favicon = "_static/favicon.svg"

rst_epilog = f"""
.. |release| replace::  {release}
"""

# -- sphinx-copybutton configuration for MesoMath custom CLI prompts --------
# Matches standard shell '$', academic '>>>', and scribal REPL '-->' prompts
copybutton_prompt_text = r"--> |\.\.\. |\$ "
copybutton_prompt_is_regexp = True

copybutton_only_copy_attr_src = False
copybutton_remove_prompts = True
copybutton_copy_empty_lines = False
copybutton_line_continuation_character = "\\"


# -- Font & Visual Settings for Cuneiform and Layout Subsystems ------------

html_css_files = [
    "https://fonts.googleapis.com/css2?family=Noto+Sans+Cuneiform&display=swap",
    "custom.css",
]

html_theme_options = {
    "show_toc_level": 2,  # Forces the right sidebar to display subsections up to h3/h4 depth
}

# Environmental tweak selector (Available for future execution routing overrides)
if on_rtd:
    # Specific Read the Docs server configuration overrides can be appended here
    pass
else:
    # Specific local machine compilation adjustments can be appended here
    pass