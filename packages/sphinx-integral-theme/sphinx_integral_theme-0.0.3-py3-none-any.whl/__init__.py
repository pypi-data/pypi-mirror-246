import os

__version_info__ = (0, 0, 3)
__version__ = "0.0.3"

def setup(app):
    app.require_sphinx("1.6")
    theme_path = os.path.abspath(os.path.dirname(__file__))
    app.add_html_theme("integral_sphinx_theme", theme_path)