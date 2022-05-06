# --------------------------------------------------------------------------------------------
# Icon Qt Dict for interfaces
# --------------------------------------------------------------------------------------------
import os
from PySide2 import QtGui

iconPath = os.path.join(os.path.dirname(__file__), 'icons')
ICONS = {}

for icon in os.listdir(iconPath):
    iconName, ext = os.path.splitext(icon)
    ICONS[iconName.lower()] = QtGui.QIcon(os.path.join(iconPath, icon))


def get_icon(name):
    ''' returns icon from ICONS '''
    return ICONS[name.lower()]
