# noqa: D100
from atsphinx.color_text import __version__ as version

# -- Project information
project = "atsphinx-color-text"
copyright = "2023, Kazuya Takei"
author = "Kazuya Takei"
release = version

# -- General configuration
extensions = [
    "atsphinx.color_text",
    "sphinx.ext.githubpages",
    "sphinx.ext.todo",
]
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

rst_prolog = """
.. |THIS| replace:: ``atsphinx-color-text``
"""

# -- Options for HTML output
html_theme = "alabaster"
html_static_path = ["_static"]
