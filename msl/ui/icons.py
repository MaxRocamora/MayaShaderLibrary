# ----------------------------------------------------------------------------------------
# Icon Qt Dict for the ui
# ----------------------------------------------------------------------------------------
import os

from PySide2 import QtGui

path = os.path.join(os.path.dirname(__file__), 'icons')
ICONS = {}

for icon_filename in os.listdir(path):
    filename, _ = os.path.splitext(icon_filename)
    ICONS[filename.lower()] = QtGui.QIcon(os.path.join(path, icon_filename))


def get_icon(name):
    ''' returns icon from ICONS '''
    return ICONS[name.lower()]
