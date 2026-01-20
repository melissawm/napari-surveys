# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os

project = 'napari surveys'
html_title = 'napari surveys'
copyright = '2026, napari team'
author = 'napari team'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["myst_nb"]
exclude_patterns = ['*.ipynb']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'napari_sphinx_theme'
# sidebar content
html_sidebars = {
    "**": ["navbar-nav"],
}

html_theme_options = {
    "navbar_center": [],
    "navbar_persistent": [],
    "secondary_sidebar_items": ["page-toc"],
}

# use an env var to control whether notebooks are executed
nb_execution_mode = os.environ.get("NB_EXECUTION_MODE", "force")
nb_output_stderr = "show"
