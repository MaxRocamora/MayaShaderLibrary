
# -*- coding: utf-8 -*-
'''
# Style QT Methods for Arcane Interfaces
'''
import os
from PySide2 import QtCore, QtGui
appPath = os.path.dirname(__file__)
from ... import sshFile, arcaneIcon


def cssMainWindow(appPath, mainWidget, objName, windowTitle):
    '''
    Set QT CSS Stylesheet for QMainWindow
    Sets App Icon
    Args:
            appPath (string) path of python app
            mainWidget (widget) main class (passed as self)
            objName (string) Name of the qt object for window detection/destroy.
            windowTitle (string) Set the name of the main window
    '''
    mainWidget.setWindowIcon(QtGui.QIcon(arcaneIcon))
    mainWidget.setObjectName(objName)
    mainWidget.setWindowTitle(windowTitle)
    mainWidget.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
    with open(sshFile, "r") as fh:
        mainWidget.setStyleSheet(fh.read())
