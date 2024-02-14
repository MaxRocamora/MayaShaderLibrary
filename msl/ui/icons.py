# ----------------------------------------------------------------------------------------
# Icon Qt Dict for the ui
# ----------------------------------------------------------------------------------------
import os

from PySide2 import QtGui

# Main Icon store
ICONS = {}

# Load Icons from icons folder
path = os.path.join(os.path.dirname(__file__), 'icons')

for icon_filename in os.listdir(path):
    filename, _ = os.path.splitext(icon_filename)
    ICONS[filename.lower()] = QtGui.QIcon(os.path.join(path, icon_filename))


def get_icon(name: str):
    """Returns icon from ICONS."""
    return ICONS[name.lower()]
