# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
import django

sys.path.insert(0, os.path.abspath('..'))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../_ext")))
os.environ['DJANGO_SETTINGS_MODULE'] = 'itracker.settings.environments.docs'
django.setup()

project = 'itracker'
copyright = '2022, Martin Harrison, et al'
author = 'Martin Harrison, et al'
release = '5.5'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'djangodocs',
    'sphinx.ext.intersphinx',
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx_rtd_theme',
    'sphinx_rtd_size',
    'sphinx.ext.todo',
]

templates_path = ['_templates']
exclude_patterns = ['media/website/js']

intersphinx_mapping = {'python': ('https://docs.python.org/3', None)}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
sphinx_rtd_size_width = '100%'
todo_include_todos = True
#html_static_path = ['_static']
