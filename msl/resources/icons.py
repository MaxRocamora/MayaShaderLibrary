# ----------------------------------------------------------------------------------------
# Icon Qt Dict for the ui
#
# Icons Credits:
# - https://www.flaticon.com/authors/freepik
# - https://www.flaticon.com/authors/Andrean-Prabowo
# - https://www.flaticon.com/authors/juicy-fish
# - https://www.flaticon.com/authors/Fathema-Khanom
# - Small Menu Icons: https://p.yusukekamiyamane.com/
# ----------------------------------------------------------------------------------------
import os

try:
    from PySide2 import QtGui
except ImportError:
    from PySide6 import QtGui

# Main Icon store
ICONS = {}

# Load Icons from icons folder
path = os.path.join(os.path.dirname(__file__), 'icons')

for icon_filename in os.listdir(path):
    filename, _ = os.path.splitext(icon_filename)
    ICONS[filename.lower()] = QtGui.QIcon(os.path.join(path, icon_filename))


def get_icon(name: str) -> QtGui.QIcon:
    """Returns icon from ICONS."""
    return ICONS[name.lower()]
