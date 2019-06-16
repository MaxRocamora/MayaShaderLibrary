# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------------------------
# Icon Qt Dict for interfaces
# --------------------------------------------------------------------------------------------

# IMPORTS
import os
from PySide2 import QtGui
iconPath = os.path.join(os.path.dirname(__file__), 'icons')
IconLib = {}

for icon in os.listdir(iconPath):
    iconName, ext = os.path.splitext(icon)
    IconLib[iconName.lower()] = QtGui.QIcon(os.path.join(iconPath, icon))


def getIcon(name):
    ''' returns icon from iconlib '''
    return IconLib[name.lower()]
